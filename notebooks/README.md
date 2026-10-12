# Introductory notebooks

Two short, self-contained notebooks that walk through the package's public API on the two synthetic fixtures in `tests/fixtures/`:

- `pwd-intro.ipynb` — load a PWD fixture, run `ingest_pwd`, and inspect normalized employer, location, and wage-level fields.
- `perm-intro.ipynb` — load a PERM fixture, run `ingest_perm`, and compute the recruitment-start-to-filing interval with `recruitment_statistics`.

## Environment

Both notebooks run from a fresh, fully offline environment. From the repository root:

```bash
python -m pip install -e .
```

Install the notebook runtime as an optional dependency. Any Jupyter-compatible front end works (Jupyter Notebook, JupyterLab, or VS Code); the only optional dependency needed to *run* the notebooks is the front end itself, for example:

```bash
python -m pip install "jupyter>=1,<2"
```

No network access, credentials, database, or production data is required or used at runtime. The notebooks open only `tests/fixtures/pwd.csv` and `tests/fixtures/perm.csv`, which ship in the repository. Run them from the repository root so the relative fixture paths resolve.

## Outputs

The embedded cell outputs are committed and use only synthetic values with no machine-specific paths or notebook metadata. The two `print` cells write plain standard output; there are no image, HTML, or rich outputs. To reproduce the outputs you do not need a notebook front end:

```bash
python -c "
import json, contextlib, io, sys
sys.path.insert(0, 'src')
for name in ('pwd-intro.ipynb', 'perm-intro.ipynb'):
    for cell in json.load(open('notebooks/' + name, encoding='utf-8'))['cells']:
        if cell['cell_type'] == 'code':
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exec(''.join(cell['source']), globals())
            print(buf.getvalue())
"
```

The PERM notebook's interval is a derived descriptive measure and is **not** official PERM processing time — see the notebook's own caveat cell and the [Recruitment statistic](../README.md#recruitment-statistic) section of the main README.
