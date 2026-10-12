"""Generate the committed sample outputs under examples/.

Run with the project venv:
    .venv/Scripts/python examples/generate_samples.py

The samples are produced from the two synthetic test fixtures using the
package's public ingestion API (``ingest_pwd`` / ``ingest_perm``) and are
written with an explicit Unix line terminator so the committed bytes are
identical on every platform. Re-running produces byte-identical files.

The equivalent one-shot CLI commands are documented in ``examples/README.md``.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from jollux_immigration_data import ingest_perm, ingest_pwd

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = Path(__file__).resolve().parent
PWD_FIXTURE = ROOT / "tests" / "fixtures" / "pwd.csv"
PERM_FIXTURE = ROOT / "tests" / "fixtures" / "perm.csv"


def write_jsonl(records: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def write_csv(records: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        if records:
            writer = csv.DictWriter(handle, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)


def main() -> None:
    pwd_records = list(ingest_pwd(PWD_FIXTURE))
    perm_records = list(ingest_perm(PERM_FIXTURE))

    write_jsonl(pwd_records, EXAMPLES / "sample_pwd_output.jsonl")
    write_csv(pwd_records, EXAMPLES / "sample_pwd_output.csv")
    write_jsonl(perm_records, EXAMPLES / "sample_perm_output.jsonl")
    write_csv(perm_records, EXAMPLES / "sample_perm_output.csv")

    print(f"PWD records: {len(pwd_records)}")
    print(f"PERM records: {len(perm_records)}")


if __name__ == "__main__":
    main()
