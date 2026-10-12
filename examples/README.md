# Sample outputs

Small, deterministic samples of the normalized JSON Lines and CSV that the CLI writes, generated from the synthetic fixtures in `tests/fixtures/`. No downloaded DOL records, production exports, or private data are used or included.

## Files

| File | Source fixture | Records |
| ---- | -------------- | ------- |
| `sample_pwd_output.jsonl` / `sample_pwd_output.csv` | `tests/fixtures/pwd.csv` | 1 (P-100) |
| `sample_perm_output.jsonl` / `sample_perm_output.csv` | `tests/fixtures/perm.csv` | 2 (A-100, A-101) |

The PWD fixture contains three rows, but only one is emitted: P-101 has a `Withdrawn` status and P-102 is an `H-1B` visa class, both excluded by PWD ingestion (see [the `PWD` section of the main README](../README.md#supported-schema)).

## Reproduce

The samples are written by calling the CLI entry point (`jollux_immigration_data.cli.main`, the same function the `jollux-immigration-data` console script runs) against the two fixtures. `examples/generate_samples.py` wraps those calls so the output stays byte-identical:

```bash
python -m pip install -e .
python examples/generate_samples.py
```

Equivalent one-shot CLI invocations, one per file:

```bash
jollux-immigration-data pwd tests/fixtures/pwd.csv  --output examples/sample_pwd_output.jsonl
jollux-immigration-data pwd tests/fixtures/pwd.csv  --output examples/sample_pwd_output.csv --format csv
jollux-immigration-data perm tests/fixtures/perm.csv --output examples/sample_perm_output.jsonl
jollux-immigration-data perm tests/fixtures/perm.csv --output examples/sample_perm_output.csv --format csv
```

Re-running any of these (or `generate_samples.py`) produces the same bytes every time; the only input is the two committed fixtures.

## What the samples show

- **Employer normalization** — `employer_name` is preserved verbatim (`Example Analytics Inc.` / `Example Analytics Incorporated`) while `employer_normalized` reduces both to the same matching key `example analytics`. Keep the source name next to the key.
- **State/location normalization** — raw `TEXAS` / `Texas` / `WA` all come out as `TX` / `WA` in `worksite_state` and as a `city, ST` form in `worksite_location`.
- **Wage-level normalization** — PWD `Level 2` comes out as `Level II`.
- **Dates** — ISO `YYYY-MM-DD`; the CLI serializes with `json.dumps(..., default=str)`, so values already come out as ISO strings.
- **CSV vs JSONL** — the field order is the ingestion record's key order; CSV cells containing a comma are quoted by `csv.DictWriter`.
