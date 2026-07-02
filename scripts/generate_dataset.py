import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


OLLAMA_URL = "http://localhost:11434/api/generate"


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def call_ollama(model_name, prompt, options):
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": options,
    }
    data = json.dumps(payload).encode("utf-8")
    request = Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=600) as response:
        body = response.read().decode("utf-8")
    return json.loads(body)["response"]


def extract_json_array(text):
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?", "", stripped, flags=re.IGNORECASE).strip()
        stripped = re.sub(r"```$", "", stripped).strip()

    try:
        value = json.loads(stripped)
        if isinstance(value, list):
            return value
    except json.JSONDecodeError:
        pass

    match = re.search(r"\[[\s\S]*\]", stripped)
    if not match:
        raise ValueError("No JSON array found in model response")
    value = json.loads(match.group(0))
    if not isinstance(value, list):
        raise ValueError("Extracted JSON is not an array")
    return value


def normalize_record(record, model_id, model_family, prompt_id):
    intencion = record.get("intencion", record.get("intención", ""))
    return {
        "source_model": model_id,
        "model_family": model_family,
        "prompt_id": prompt_id,
        "id": str(record.get("id", "")).strip(),
        "texto": str(record.get("texto", "")).strip(),
        "intencion": str(intencion).strip().lower(),
        "urgencia": str(record.get("urgencia", "")).strip().lower(),
    }


def expected_ids(prompt_id, num_examples):
    return {f"{prompt_id}_{index:03d}" for index in range(1, num_examples + 1)}


def build_repair_prompt(original_prompt, missing_ids):
    ids = ", ".join(sorted(missing_ids))
    return (
        f"{original_prompt}\n\n"
        "La respuesta anterior quedo incompleta. Genera solamente los registros "
        f"faltantes con estos ids exactos: {ids}. Devuelve exclusivamente un arreglo "
        "JSON valido, sin Markdown ni explicaciones."
    )


def merge_unique(records, new_records):
    by_id = {record["id"]: record for record in records if record.get("id")}
    for record in new_records:
        record_id = record.get("id")
        if record_id and record_id not in by_id:
            by_id[record_id] = record
    return list(by_id.values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", default="config/models.json")
    parser.add_argument("--prompts", default="prompts/prompts.json")
    parser.add_argument("--output", default="data/generated")
    parser.add_argument("--raw-output", default="data/raw")
    parser.add_argument("--limit-prompts", type=int, default=None)
    parser.add_argument("--only-model", default=None)
    args = parser.parse_args()

    model_config = load_json(args.models)
    prompt_config = load_json(args.prompts)
    prompts = prompt_config["prompts"]
    if args.limit_prompts is not None:
        prompts = prompts[: args.limit_prompts]

    output_dir = Path(args.output)
    raw_dir = Path(args.raw_output)
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    options = model_config.get("generation_options", {})

    models = model_config["models"]
    if args.only_model:
        models = [model for model in models if model["id"] == args.only_model]
        if not models:
            raise ValueError(f"No model found with id {args.only_model}")

    for model in models:
        model_id = model["id"]
        model_name = model["ollama_name"]
        family = model["family"]
        all_records = []
        errors = []

        print(f"Generating with {family} ({model_name})")
        for item in prompts:
            prompt_id = item["id"]
            target_ids = expected_ids(prompt_id, item["num_examples"])
            prompt_records = []
            started = time.time()
            current_prompt = item["prompt"]

            for attempt in range(1, 4):
                try:
                    response_text = call_ollama(model_name, current_prompt, options)
                    raw_path = raw_dir / f"{model_id}_{prompt_id}_attempt{attempt}.txt"
                    raw_path.write_text(response_text, encoding="utf-8")
                    parsed = extract_json_array(response_text)
                    normalized = [
                        normalize_record(record, model_id, family, prompt_id)
                        for record in parsed
                    ]
                    prompt_records = merge_unique(prompt_records, normalized)
                    found_ids = {record["id"] for record in prompt_records}
                    missing_ids = target_ids - found_ids
                    if not missing_ids:
                        break
                    current_prompt = build_repair_prompt(item["prompt"], missing_ids)
                except (URLError, TimeoutError) as exc:
                    message = (
                        f"{model_id}/{prompt_id}: could not reach Ollama. "
                        f"Is Ollama running and is {model_name} pulled? {exc}"
                    )
                    print(message, file=sys.stderr)
                    errors.append(message)
                    break
                except Exception as exc:
                    message = f"{model_id}/{prompt_id}/attempt{attempt}: {exc}"
                    print(message, file=sys.stderr)
                    errors.append(message)
                    current_prompt = build_repair_prompt(
                        item["prompt"],
                        target_ids
                        - {record["id"] for record in prompt_records if record.get("id")},
                    )

            found_ids = {record["id"] for record in prompt_records}
            missing_ids = target_ids - found_ids
            extra_records = [record for record in prompt_records if record["id"] not in target_ids]
            selected_records = [record for record in prompt_records if record["id"] in target_ids]
            all_records.extend(sorted(selected_records, key=lambda record: record["id"]))
            elapsed = time.time() - started
            print(
                f"  {prompt_id}: {len(selected_records)}/{item['num_examples']} records "
                f"in {elapsed:.1f}s"
            )
            if missing_ids:
                errors.append(f"{model_id}/{prompt_id}: missing ids {sorted(missing_ids)}")
            if extra_records:
                errors.append(f"{model_id}/{prompt_id}: ignored {len(extra_records)} extra records")

        output_path = output_dir / f"{model_id}.jsonl"
        with open(output_path, "w", encoding="utf-8") as fh:
            for record in all_records:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"Saved {len(all_records)} records to {output_path}")

        if errors:
            error_path = raw_dir / f"{model_id}_errors.log"
            error_path.write_text("\n".join(errors), encoding="utf-8")
            print(f"Saved {len(errors)} errors to {error_path}")


if __name__ == "__main__":
    main()
