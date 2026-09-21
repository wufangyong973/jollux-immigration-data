# Jollux Immigration Data

Reusable Python tools for reading and normalizing public U.S. Department of Labor employment immigration disclosure data.

Version 0.1.0 supports a focused subset of Prevailing Wage Determination (PWD) and PERM disclosure fields. This repository contains data-processing utilities and synthetic tests. It does not contain the Jollux Labs website, production datasets, analytics, deployment configuration, feedback storage, or database code.

## Features

- Read `.xlsx` files in read-only mode and basic UTF-8 `.csv` files
- Ingest selected PWD and PERM disclosure fields
- Preserve source employer names while producing normalized matching keys
- Normalize U.S. state and territory names
- Normalize common wage-level representations
- Convert Excel serial dates and common date values to ISO dates
- Summarize the interval from recruitment start to PERM filing
- Report potential employer-normalization collisions

## Installation

Install the package from a local checkout:

```bash
python -m pip install -e .
```

Python 3.10 or newer is required.

## Development

Install the test dependencies and run the test suite:

```bash
python -m pip install -e '.[test]'
pytest
```

Tests use invented records only. Do not add downloaded disclosure files, production exports, or records copied from a production system as fixtures.

## Usage

Use the ingestion functions from Python:

```python
from jollux_immigration_data import ingest_perm, ingest_pwd

pwd_records = list(ingest_pwd("PW_Disclosure_Data.xlsx"))
perm_records = list(ingest_perm("PERM_Disclosure_Data.xlsx"))
```

The small command-line interface can write normalized JSON Lines or CSV:

```bash
jollux-immigration-data pwd input.xlsx --output pwd.jsonl
jollux-immigration-data perm input.csv --output perm.csv --format csv
```

The package does not download source files or make network requests.

## Documentation

- [Supported PWD and PERM fields](docs/supported-fields.md)
- [Quarterly DOL disclosure-data update checklist](docs/quarterly-update-checklist.md)

## Official data sources

The U.S. Department of Labor's Office of Foreign Labor Certification (OFLC) publishes disclosure files and record layouts on its official [Performance Data](https://www.dol.gov/agencies/eta/foreign-labor/performance) page.

Relevant sections on that page include:

- PERM Program Disclosure Files and Program Record Layouts
- Prevailing Wage Program Disclosure Files and Program Record Layouts

Background information about OFLC programs is available from the Department of Labor's [Foreign Labor Certification](https://www.dol.gov/agencies/eta/foreign-labor) page. Prevailing wage program information is available from its [Prevailing Wage Information and Resources](https://www.dol.gov/agencies/eta/foreign-labor/wages) page.

Disclosure schemas and filenames can change between fiscal years or form versions. Consult the record layout published alongside the file being processed. Data obtained from these sources remains subject to the source's terms and documentation.

## Supported schema

The initial release recognizes the column names listed in `pwd.py` and `perm.py`. Header matching is case-insensitive and ignores surrounding whitespace. Ingestion stops with a clear error when a required column is absent.

PWD ingestion currently:

- Keeps records whose visa class is `PERM`
- Excludes records with a `Withdrawn` status
- Requires an employer name and wage-expiration date
- Deduplicates records by case number
- Emits a selected set of case, employer, job, worksite, wage, and date fields

PERM ingestion currently:

- Requires a case number and employer name
- Emits a selected set of case, employer, job, worksite, wage, decision, filing, and recruitment-date fields

Broader historical schema adapters and automatic source downloading are outside the scope of version 0.1.0.

## Data and privacy

This repository contains only small synthetic fixtures. It does not include DOL disclosure workbooks, derived bulk datasets, production exports, private records, credentials, or application data.

Public disclosure records can still contain linkable case, employer, wage, job, and location information. Preserve source provenance and publish only the fields and records needed for a defined use case. Employer-normalized values should remain paired with their original source values.

## Recruitment statistic

`recruitment_statistics` calculates calendar days from `recruitment_start_date` to `received_date` for records with usable dates. By default, negative intervals and intervals longer than 366 days are excluded. The result reports total, included, and excluded record counts along with minimum, maximum, and median days.

This interval is a derived descriptive measure. It is **not an official PERM processing time**, does not measure government adjudication time, and should not be presented as a processing-time estimate. Missing or inconsistent source dates can affect the result.

## Limitations

- XLSX ingestion reads the active worksheet with `openpyxl` in read-only mode.
- CSV ingestion expects a header row and UTF-8 input, with an optional byte-order mark.
- Version 0.1.0 supports a limited set of current column names rather than every historical disclosure schema.
- Employer normalization can group distinct legal entities under the same key. Use the collision report and retain source names.
- The CLI collects normalized records before writing output and may not be suitable for very large files.
- Input-size and row-count limits are not currently enforced. Process untrusted workbooks in a constrained environment.

## License

The source code is available under the MIT License. See `LICENSE`.

Third-party data is not covered by the software license and remains subject to its source terms.
