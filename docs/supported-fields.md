# Supported PWD and PERM Fields

This reference describes the input columns and normalized records supported by the current `ingest_pwd` and `ingest_perm` implementations. It documents the package as it exists; it is not a complete reference for every Department of Labor disclosure schema.

Both ingestors accept `.xlsx` and `.csv` files. XLSX input uses the active worksheet in read-only, data-only mode. CSV input uses UTF-8 with an optional byte-order mark. Header matching removes surrounding whitespace and converts headers to uppercase. If any required header is absent, ingestion raises `ValueError` before yielding records.

A required input field means that its column must exist in the header. Individual values may still be empty unless the row-level behavior below requires a value.

## PWD required input fields

The PWD ingestor requires these columns:

| Input column | Current use |
| --- | --- |
| `CASE_NUMBER` | Identifies a record and supports first-qualifying-record deduplication. |
| `CASE_STATUS` | Emitted as case status; rows with status `Withdrawn`, compared case-insensitively, are excluded. |
| `RECEIVED_DATE` | Converted to `received_date`. |
| `VISA_CLASS` | Rows are retained only when the trimmed, uppercased value is `PERM`. |
| `EMPLOYER_LEGAL_BUSINESS_NAME` | Emitted as `employer_name` and used to produce `employer_normalized`; a nonempty value is required for the row. |
| `JOB_TITLE` | Emitted as `job_title`. |
| `PRIMARY_WORKSITE_CITY` | Emitted as `worksite_city` and used in `worksite_location`. |
| `PRIMARY_WORKSITE_STATE` | Normalized into `worksite_state` and used in `worksite_location`. |
| `PWD_SOC_TITLE` | Emitted as `soc_title`. |
| `PWD_WAGE_RATE` | Emitted as `wage_rate` without numeric conversion. |
| `PWD_UNIT_OF_PAY` | Emitted as `wage_unit`. |
| `PWD_OES_WAGE_LEVEL` | Normalized into `wage_level`. |
| `PREVAIL_WAGE_DETERM_DATE` | Converted to `determination_date`. |
| `PWD_WAGE_EXPIRATION_DATE` | Converted to `wage_expiration_date`; a nonempty converted value is required for the row. |

## PWD normalized output fields

Each retained PWD row produces a dictionary with these fields:

| Output field | Source or derivation | Value behavior |
| --- | --- | --- |
| `case_number` | `CASE_NUMBER` | Trimmed string; always nonempty for an emitted record. |
| `case_status` | `CASE_STATUS` | Trimmed string, or `None` when empty. |
| `received_date` | `RECEIVED_DATE` | Date conversion described below; may be `None`. |
| `employer_name` | `EMPLOYER_LEGAL_BUSINESS_NAME` | Trimmed source name; always nonempty for an emitted record. |
| `employer_normalized` | `employer_name` | Normalized matching key described below. |
| `job_title` | `JOB_TITLE` | Cleaned source value; may be `None`. |
| `worksite_city` | `PRIMARY_WORKSITE_CITY` | Cleaned source value; may be `None`. |
| `worksite_state` | `PRIMARY_WORKSITE_STATE` | State normalization described below; may be `None`. |
| `worksite_location` | City and state | Available parts joined as `City, ST`; may be `None`. |
| `soc_title` | `PWD_SOC_TITLE` | Cleaned source value; may be `None`. |
| `wage_rate` | `PWD_WAGE_RATE` | Cleaned source value; no numeric conversion is applied. |
| `wage_unit` | `PWD_UNIT_OF_PAY` | Cleaned source value; may be `None`. |
| `wage_level` | `PWD_OES_WAGE_LEVEL` | Wage-level normalization described below; may be `None`. |
| `determination_date` | `PREVAIL_WAGE_DETERM_DATE` | Date conversion described below; may be `None`. |
| `wage_expiration_date` | `PWD_WAGE_EXPIRATION_DATE` | Converted date value; nonempty for an emitted record. |

## PERM required input fields

The PERM ingestor requires these columns:

| Input column | Current use |
| --- | --- |
| `CASE_NUMBER` | Emitted as `case_number`; a nonempty value is required for the row. |
| `CASE_STATUS` | Emitted as `case_status`. |
| `RECEIVED_DATE` | Converted to `received_date`. |
| `DECISION_DATE` | Converted to `decision_date`. |
| `EMP_BUSINESS_NAME` | Emitted as `employer_name` and used to produce `employer_normalized`; a nonempty value is required for the row. |
| `PWD_SOC_TITLE` | Emitted as `soc_title`. |
| `JOB_TITLE` | Emitted as `job_title`. |
| `JOB_OPP_WAGE_FROM` | Emitted as `wage_from` without numeric conversion. |
| `JOB_OPP_WAGE_TO` | Emitted as `wage_to` without numeric conversion. |
| `JOB_OPP_WAGE_PER` | Emitted as `wage_unit`. |
| `PRIMARY_WORKSITE_CITY` | Emitted as `worksite_city` and used in `worksite_location`. |
| `PRIMARY_WORKSITE_STATE` | Normalized into `worksite_state` and used in `worksite_location`. |
| `RECR_INFO_JOB_START_DATE` | Converted to `recruitment_start_date`. |
| `RECR_INFO_JOB_END_DATE` | Converted to `recruitment_end_date`. |

## PERM normalized output fields

Each retained PERM row produces a dictionary with these fields:

| Output field | Source or derivation | Value behavior |
| --- | --- | --- |
| `case_number` | `CASE_NUMBER` | Trimmed string; always nonempty for an emitted record. |
| `case_status` | `CASE_STATUS` | Cleaned source value; may be `None`. |
| `received_date` | `RECEIVED_DATE` | Date conversion described below; may be `None`. |
| `decision_date` | `DECISION_DATE` | Date conversion described below; may be `None`. |
| `employer_name` | `EMP_BUSINESS_NAME` | Trimmed source name; always nonempty for an emitted record. |
| `employer_normalized` | `employer_name` | Normalized matching key described below. |
| `job_title` | `JOB_TITLE` | Cleaned source value; may be `None`. |
| `soc_title` | `PWD_SOC_TITLE` | Cleaned source value; may be `None`. |
| `wage_from` | `JOB_OPP_WAGE_FROM` | Cleaned source value; no numeric conversion is applied. |
| `wage_to` | `JOB_OPP_WAGE_TO` | Cleaned source value; no numeric conversion is applied and it may be `None`. |
| `wage_unit` | `JOB_OPP_WAGE_PER` | Cleaned source value; may be `None`. |
| `worksite_city` | `PRIMARY_WORKSITE_CITY` | Cleaned source value; may be `None`. |
| `worksite_state` | `PRIMARY_WORKSITE_STATE` | State normalization described below; may be `None`. |
| `worksite_location` | City and state | Available parts joined as `City, ST`; may be `None`. |
| `recruitment_start_date` | `RECR_INFO_JOB_START_DATE` | Date conversion described below; may be `None`. |
| `recruitment_end_date` | `RECR_INFO_JOB_END_DATE` | Date conversion described below; may be `None`. |

The current PERM ingestor does not filter by case status and does not deduplicate case numbers.

## Date formatting and null behavior

Date fields pass through `excel_date`:

- Python `date` and `datetime` values become ISO `YYYY-MM-DD` strings.
- Numeric spreadsheet serial values use the Excel-compatible base date `1899-12-30` and become ISO date strings.
- Strings in `YYYY-MM-DD`, `MM/DD/YYYY`, or `MM/DD/YY` format become ISO date strings.
- A time suffix following `T` or a space is removed before string parsing.
- `None`, empty strings, and whitespace-only strings become `None`.
- An unrecognized nonempty date string is returned as its trimmed date candidate; the current implementation does not reject it.

For non-date fields, input strings have internal whitespace collapsed and surrounding whitespace removed. Empty strings become `None`. Non-string values are retained as read, so values such as wages may be strings when read from CSV and numeric types when read from XLSX.

## Employer normalization

Both ingestors preserve the trimmed source employer name and add an `employer_normalized` matching key. Normalization currently:

1. Applies Unicode NFKD decomposition and removes non-ASCII characters.
2. Converts text to lowercase using `casefold`.
3. Replaces `&` with `and`.
4. Replaces other non-alphanumeric runs with spaces.
5. Removes repeated trailing legal suffixes from this set: `co`, `company`, `corp`, `corporation`, `inc`, `incorporated`, `limited`, `llc`, `llp`, `lp`, `ltd`, `na`, and `plc`.
6. Joins the remaining tokens with single spaces.

For example, `Café Data & Research, Inc.` normalizes to `cafe data and research`.

Normalization is a matching aid and can group distinct legal entities under the same key. The package provides `employer_collision_report` to identify normalized keys associated with multiple distinct source names.

## Location and state normalization

`normalize_state`:

- Returns `None` for missing or whitespace-only input.
- Uppercases the value, removes periods, and collapses whitespace.
- Converts recognized full U.S. state and supported territory names to their two-letter codes.
- Keeps recognized two-letter codes as codes.
- Returns an unrecognized value in its cleaned uppercase form rather than guessing a mapping.

The supported territory mappings currently include the District of Columbia, Puerto Rico, Guam, American Samoa, the Northern Mariana Islands, and the U.S. Virgin Islands.

`worksite_location` combines the cleaned city and normalized state with a comma. If only one part is present, it returns that part. If neither part is present, it returns `None`.

## Wage-level normalization

Wage-level normalization is used by PWD ingestion for `PWD_OES_WAGE_LEVEL`. It recognizes Arabic and Roman values from one through four, including forms such as `2`, `II`, `Level 2`, and `Wage Level IV`. These become `Level I`, `Level II`, `Level III`, or `Level IV`.

Missing values and the strings `N/A`, `NA`, `NONE`, and `NULL`, compared after uppercasing and whitespace cleanup, become `None`. An unrecognized nonempty value is returned in its original trimmed form rather than being assigned a level.

PERM ingestion does not currently emit or normalize a wage-level field.

## PWD filtering and deduplication

PWD records are processed in input order. A row is emitted only when:

- `CASE_NUMBER` is nonempty.
- `VISA_CLASS`, after trimming and uppercasing, is `PERM`.
- `CASE_STATUS` is not `Withdrawn`, compared case-insensitively.
- `EMPLOYER_LEGAL_BUSINESS_NAME` is nonempty.
- `PWD_WAGE_EXPIRATION_DATE` produces a nonempty converted value.
- The case number has not already been emitted.

The first qualifying row for a case number is retained. Later qualifying rows with the same case number are skipped. Rows excluded before qualification do not reserve that case number.

PERM ingestion currently requires a nonempty case number and employer name but applies no corresponding status filter or case-number deduplication.

## Schema versions and compatibility

DOL disclosure schemas can vary by fiscal year, quarter, program, and form version. A file appearing on the official OFLC disclosure page is not automatically supported by this package. Compare its published record layout with the required columns above before processing it.

The current implementation uses one focused PWD mapping and one focused PERM mapping. It does not contain historical or quarter-specific schema adapters. See the [quarterly update checklist](quarterly-update-checklist.md) when evaluating another disclosure release.
