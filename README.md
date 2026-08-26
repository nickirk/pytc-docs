# PyTC documentation

This repository contains the Sphinx source for the
[PyTC documentation](https://nickirk.github.io/pytc-docs/). The PyTC package
itself is developed in [`nickirk/pytc`](https://github.com/nickirk/pytc) and
published on PyPI as [`pytc-qc`](https://pypi.org/project/pytc-qc/).

The documentation history was extracted from the original `docs/` directory
with `git subtree split`, preserving the commits that built the site before it
became an independent repository.

## Build locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps "git+https://github.com/nickirk/pytc.git@v0.2.1"
PYTC_DOCS_EXPECT_VERSION=0.2.1 sphinx-build -b html . _build/html
```

Open `_build/html/index.html` after the build completes.
