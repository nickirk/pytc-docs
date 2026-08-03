# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os

# The standalone docs build installs the public pytc-qc distribution.
# Skip heavy startup logging (JAX device detection, etc.) during autodoc.
os.environ["SPHINX_AUTODOC_BUILD"] = "1"

# Speed up JAX initialisation – CPU-only, no GPU search, no XLA cache
os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_FLAGS", "--xla_force_host_platform_device_count=1")
os.environ.setdefault("JAX_ENABLE_X64", "1")

# -- Project information -----------------------------------------------------
project = "PyTC"
copyright = "2025, Ke Liao"
author = "Ke Liao"


def _pytc_version():
    # Version comes from the installed distribution, never hardcoded.
    # The build must install pytc-qc from the repo (see docs.yml); PyPI is
    # always one release behind.  PYTC_DOCS_EXPECT_VERSION makes deploys
    # fail loudly if the resolved version is not the one being announced.
    from importlib.metadata import PackageNotFoundError, version
    try:
        resolved = version("pytc-qc")
    except PackageNotFoundError:
        resolved = "0.0.0+dev"
    expected = os.environ.get("PYTC_DOCS_EXPECT_VERSION")
    if expected and resolved != expected:
        raise RuntimeError(
            f"docs build resolved pytc-qc {resolved!r}, expected {expected!r} "
            "-- install pytc-qc from the repo ref being documented")
    return resolved


release = _pytc_version()

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "myst_parser",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    ".venv",
    "README.md",
    "Thumbs.db",
    ".DS_Store",
]

# Suppress harmless duplicate-object warnings from @dataclass inheritance
# (child classes re-document parent attributes in their docstrings)
suppress_warnings = ["app.add_object"]

# -- autodoc configuration ---------------------------------------------------
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_default_options = {
    "undoc-members": False,
    "show-inheritance": True,
}

# Mock heavy runtime dependencies when they are not installed (e.g. in CI).
# Sphinx creates lightweight stand-ins so autodoc can still introspect the
# source code and extract docstrings.  Locally (where JAX/PySCF are
# installed) the real packages are used for a more accurate build.
_mock_candidates = [
    "jax",
    "jaxlib",
    "flax",
    "optax",
    "folx",
    "pyscf",
    "scipy",
    "numpy",
    "h5py",
    "basis_set_exchange",
    "line_profiler",
    "psutil",
]

import importlib
autodoc_mock_imports = []
for _pkg in _mock_candidates:
    try:
        importlib.import_module(_pkg)
    except ImportError:
        autodoc_mock_imports.append(_pkg)

# -- autosummary configuration -----------------------------------------------
autosummary_generate = True  # Auto-generate stub pages for all discovered modules

# Skip test, legacy, examples, and internal subpackages during autosummary
def skip_submodules(app, what, name, obj, skip, options):
    # Skip private modules, test directories, legacy code, examples
    skip_patterns = [".test", ".tests", ".legacy", ".examples", "__pycache__"]
    if any(pat in name for pat in skip_patterns):
        return True
    return skip

def setup(app):
    app.connect("autodoc-skip-member", skip_submodules)

# MyST Markdown configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
]

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_title = "PyTC"
html_logo = "_static/pytc-logo.svg"
html_static_path = ["_static"]
html_baseurl = "https://nickirk.github.io/pytc-docs/"

html_theme_options = {
    "source_repository": "https://github.com/nickirk/pytc-docs",
    "source_branch": "main",
    "source_directory": "",
}
