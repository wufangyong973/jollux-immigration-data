"""Regression tests for the committed sample outputs in examples/.

These lock the two acceptance criteria the samples are expected to meet:
re-running the documented commands reproduces equivalent bytes, and the
samples carry no machine-specific paths or notebook metadata.
"""
import csv
import io
import json
import re
from pathlib import Path

from jollux_immigration_data import ingest_perm, ingest_pwd

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
PWD_FIXTURE = ROOT / "tests" / "fixtures" / "pwd.csv"
PERM_FIXTURE = ROOT / "tests" / "fixtures" / "perm.csv"

# Windows drive paths, POSIX home dirs, backslash separators: none may leak in.
MACHINE_SPECIFIC = re.compile(r"[A-Za-z]:[\\/]|\\\\|/home/|/Users/|C:\\\\")


def jsonl_bytes(records: list[dict]) -> bytes:
    return "".join(json.dumps(record, ensure_ascii=False, default=str) + "\n" for record in records).encode("utf-8")


def csv_bytes(records: list[dict]) -> bytes:
    if not records:
        return b""
    handle = io.StringIO()
    writer = csv.DictWriter(handle, fieldnames=list(records[0].keys()))
    writer.writeheader()
    writer.writerows(records)
    return handle.getvalue().encode("utf-8")


def test_committed_jsonl_samples_are_reproducible():
    pwd_records = list(ingest_pwd(PWD_FIXTURE))
    perm_records = list(ingest_perm(PERM_FIXTURE))
    assert (EXAMPLES / "sample_pwd_output.jsonl").read_bytes() == jsonl_bytes(pwd_records)
    assert (EXAMPLES / "sample_perm_output.jsonl").read_bytes() == jsonl_bytes(perm_records)


def test_committed_csv_samples_are_reproducible():
    pwd_records = list(ingest_pwd(PWD_FIXTURE))
    perm_records = list(ingest_perm(PERM_FIXTURE))
    assert (EXAMPLES / "sample_pwd_output.csv").read_bytes() == csv_bytes(pwd_records)
    assert (EXAMPLES / "sample_perm_output.csv").read_bytes() == csv_bytes(perm_records)


def test_sample_records_match_ingestion_schemas():
    pwd_fields = list(list(ingest_pwd(PWD_FIXTURE))[0].keys())
    perm_fields = list(list(ingest_perm(PERM_FIXTURE))[0].keys())
    with (EXAMPLES / "sample_pwd_output.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            assert list(json.loads(line).keys()) == pwd_fields
    with (EXAMPLES / "sample_perm_output.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            assert list(json.loads(line).keys()) == perm_fields
    with (EXAMPLES / "sample_perm_output.csv").open(encoding="utf-8") as handle:
        assert handle.readline().rstrip("\r\n") == ",".join(perm_fields)


def test_samples_carry_no_machine_specific_paths():
    for name in ("sample_pwd_output.jsonl", "sample_perm_output.jsonl",
                 "sample_pwd_output.csv", "sample_perm_output.csv"):
        text = (EXAMPLES / name).read_text(encoding="utf-8")
        assert not MACHINE_SPECIFIC.search(text), name
