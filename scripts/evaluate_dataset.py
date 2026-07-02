import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


VALID_INTENCIONES = {"matricula", "pagos", "horarios", "plataforma", "becas", "certificado"}
VALID_URGENCIAS = {"baja", "media", "alta"}
TOPIC_TERMS = {
    "universidad",
    "universitario",
    "estudiante",
    "matricula",
    "pago",
    "pagos",
    "horario",
    "horarios",
    "plataforma",
    "beca",
    "becas",
    "certificado",
    "clase",
    "ramo",
    "curso",
    "soporte",
    "portal",
    "academico",
}


def read_jsonl(path):
    records = []
    invalid_lines = 0
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                invalid_lines += 1
    return records, invalid_lines


def tokens(text):
    return re.findall(r"[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+", text.lower())


def normalized_text(text):
    return " ".join(tokens(text))


def distinct_n(token_lists, n):
    grams = []
    total = 0
    for item in token_lists:
        if len(item) < n:
            continue
        total += len(item) - n + 1
        grams.extend(tuple(item[i : i + n]) for i in range(len(item) - n + 1))
    if total == 0:
        return 0.0
    return len(set(grams)) / total


def entropy(counter):
    total = sum(counter.values())
    if total == 0:
        return 0.0
    value = 0.0
    for count in counter.values():
        p = count / total
        value -= p * math.log2(p)
    return value


def evaluate_records(records, invalid_lines):
    issues = []
    valid_schema = 0
    valid_length = 0
    relevant = 0
    text_counter = Counter()
    intenciones = Counter()
    urgencias = Counter()
    token_lists = []

    for idx, record in enumerate(records, 1):
        texto = str(record.get("texto", "")).strip()
        intencion = str(record.get("intencion", "")).strip().lower()
        urgencia = str(record.get("urgencia", "")).strip().lower()
        words = tokens(texto)
        token_lists.append(words)
        text_counter[normalized_text(texto)] += 1
        intenciones[intencion] += 1
        urgencias[urgencia] += 1

        schema_ok = bool(texto) and intencion in VALID_INTENCIONES and urgencia in VALID_URGENCIAS
        if schema_ok:
            valid_schema += 1
        else:
            issues.append({"row": idx, "type": "schema", "record": record})

        if 12 <= len(words) <= 35:
            valid_length += 1
        else:
            issues.append({"row": idx, "type": "length", "word_count": len(words), "record": record})

        text_norm = normalized_text(texto)
        if TOPIC_TERMS.intersection(set(words)) or (intencion and intencion in text_norm):
            relevant += 1
        else:
            issues.append({"row": idx, "type": "relevance", "record": record})

    total = len(records)
    duplicate_count = sum(count - 1 for count in text_counter.values() if count > 1)
    unique_text_rate = (len(text_counter) / total) if total else 0.0

    return {
        "total_records": total,
        "invalid_jsonl_lines": invalid_lines,
        "schema_valid_rate": rate(valid_schema, total),
        "length_valid_rate": rate(valid_length, total),
        "topic_relevance_rate": rate(relevant, total),
        "unique_text_rate": unique_text_rate,
        "duplicate_count": duplicate_count,
        "distinct_1": distinct_n(token_lists, 1),
        "distinct_2": distinct_n(token_lists, 2),
        "intencion_entropy": entropy(intenciones),
        "urgencia_entropy": entropy(urgencias),
        "intencion_distribution": dict(intenciones),
        "urgencia_distribution": dict(urgencias),
        "issues": issues[:50],
    }


def rate(value, total):
    return value / total if total else 0.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/generated")
    parser.add_argument("--output", default="reports")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    detailed = {}
    for path in sorted(input_dir.glob("*.jsonl")):
        records, invalid_lines = read_jsonl(path)
        metrics = evaluate_records(records, invalid_lines)
        model_id = path.stem
        detailed[model_id] = metrics
        rows.append(
            {
                "model": model_id,
                "total_records": metrics["total_records"],
                "schema_valid_rate": f"{metrics['schema_valid_rate']:.4f}",
                "length_valid_rate": f"{metrics['length_valid_rate']:.4f}",
                "topic_relevance_rate": f"{metrics['topic_relevance_rate']:.4f}",
                "unique_text_rate": f"{metrics['unique_text_rate']:.4f}",
                "duplicate_count": metrics["duplicate_count"],
                "distinct_1": f"{metrics['distinct_1']:.4f}",
                "distinct_2": f"{metrics['distinct_2']:.4f}",
                "intencion_entropy": f"{metrics['intencion_entropy']:.4f}",
                "urgencia_entropy": f"{metrics['urgencia_entropy']:.4f}",
            }
        )

    csv_path = output_dir / "metrics_summary.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["model"])
        writer.writeheader()
        writer.writerows(rows)

    json_path = output_dir / "metrics_detailed.json"
    json_path.write_text(json.dumps(detailed, indent=2, ensure_ascii=False), encoding="utf-8")

    md_path = output_dir / "analysis_template.md"
    md_path.write_text(build_analysis_template(rows), encoding="utf-8")

    print(f"Saved summary to {csv_path}")
    print(f"Saved detailed metrics to {json_path}")
    print(f"Saved analysis template to {md_path}")


def build_analysis_template(rows):
    lines = [
        "# Analisis de resultados",
        "",
        "## Resultados cuantitativos",
        "",
        "| Modelo | Registros | Formato valido | Longitud valida | Relevancia | Unique text | Distinct-1 | Distinct-2 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['model']} | {row['total_records']} | {row['schema_valid_rate']} | "
            f"{row['length_valid_rate']} | {row['topic_relevance_rate']} | "
            f"{row['unique_text_rate']} | {row['distinct_1']} | {row['distinct_2']} |"
        )
    lines.extend(
        [
            "",
            "## Analisis cualitativo",
            "",
            "- Coherencia: describir si los mensajes son comprensibles y naturales.",
            "- Relevancia: describir si se mantienen dentro del contexto universitario.",
            "- Diversidad: comparar repeticion de frases, intenciones y urgencias.",
            "- Cumplimiento de formato: mencionar errores de JSON, campos ausentes o etiquetas invalidas.",
            "",
            "## Conclusion",
            "",
            "Indicar que modelo genero el dataset mas util y justificarlo con metricas y ejemplos.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
