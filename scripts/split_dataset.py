import argparse
import json
import random
from pathlib import Path


def read_all_jsonl(input_dir):
    records = []
    for path in sorted(Path(input_dir).glob("*.jsonl")):
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    return records


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/generated")
    parser.add_argument("--output", default="data/final")
    parser.add_argument("--train", type=float, default=0.70)
    parser.add_argument("--validation", type=float, default=0.15)
    parser.add_argument("--test", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=3360)
    args = parser.parse_args()

    total_ratio = args.train + args.validation + args.test
    if abs(total_ratio - 1.0) > 1e-6:
        raise ValueError("train + validation + test must equal 1.0")

    records = read_all_jsonl(args.input)
    random.Random(args.seed).shuffle(records)

    total = len(records)
    train_end = int(total * args.train)
    validation_end = train_end + int(total * args.validation)

    splits = {
        "train": records[:train_end],
        "validation": records[train_end:validation_end],
        "test": records[validation_end:],
    }

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, split_records in splits.items():
        write_jsonl(output_dir / f"{name}.jsonl", split_records)

    manifest = {
        "total": total,
        "seed": args.seed,
        "ratios": {
            "train": args.train,
            "validation": args.validation,
            "test": args.test,
        },
        "counts": {name: len(items) for name, items in splits.items()},
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

