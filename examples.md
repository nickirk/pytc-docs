# Examples

PyTC 0.2.1 ships six numbered examples in the
[`pytc/examples`](https://github.com/nickirk/pytc/tree/v0.2.1/pytc/examples)
directory. They are small, executable demonstrations rather than production
benchmarks.

## Get and run the examples

Clone the matching release and install it in editable mode:

```bash
git clone --branch v0.2.1 https://github.com/nickirk/pytc.git
cd pytc
python -m pip install -e .
```

Run an example from the repository root, for example:

```bash
python pytc/examples/03_dense_xtc_ccsd.py
python pytc/examples/06_rank_m_x_factor_direct_ccsd.py
```

Each script is runnable on its own unless the table notes a dependency. The
scripts print a small expected-value or structural self-check and fail if that
check does not pass.

## Numbered walkthrough

| Script | What it demonstrates | Dependency |
|---|---|---|
| [`01_vmc_optimize_jastrow.py`](https://github.com/nickirk/pytc/blob/v0.2.1/pytc/examples/01_vmc_optimize_jastrow.py) | Two-phase reference-variance VMC optimization of a Jastrow factor | Writes `h2o_phase_b_hist.h5` |
| [`02_load_and_average_jastrow_params.py`](https://github.com/nickirk/pytc/blob/v0.2.1/pytc/examples/02_load_and_average_jastrow_params.py) | Polyak–Ruppert averaging of the phase-B trajectory | Reads the file written by 01 |
| [`03_dense_xtc_ccsd.py`](https://github.com/nickirk/pytc/blob/v0.2.1/pytc/examples/03_dense_xtc_ccsd.py) | Exact dense, non-ISDF xTC-CCSD | Standalone |
| [`04_isdf_xtc_ccsd.py`](https://github.com/nickirk/pytc/blob/v0.2.1/pytc/examples/04_isdf_xtc_ccsd.py) | ISDF xTC-CCSD compared with the dense reference | Standalone |
| [`05_make_fno_xtc_ccsd.py`](https://github.com/nickirk/pytc/blob/v0.2.1/pytc/examples/05_make_fno_xtc_ccsd.py) | FNO virtual-space truncation scan through ISDF | Standalone |
| [`06_rank_m_x_factor_direct_ccsd.py`](https://github.com/nickirk/pytc/blob/v0.2.1/pytc/examples/06_rank_m_x_factor_direct_ccsd.py) | Rank-$M$ orbital X and direct T2-U-Z factorized ISDF xTC-CCSD | Standalone; PyTC 0.2.1+ |

## Two separate workflows

Examples 01 and 02 show how to optimize and average a flexible
`CompositeJastrow([NuclearCusp, BoysHandy])`. Examples 03–05 instead use a
fixed, inexpensive `REXP` correlator so that the dense reference remains
practical on a small machine. They do not consume the optimized parameters
from 01/02.

Example 06 is a separate H4/STO-3G API demonstration. It confirms that the
rank-$M$ build contains `X_tucker = {U, Z}` instead of dense X and then runs
the dedicated factor-direct solver. See [ISDF Efficiency Paths](isdf-efficiency.md)
before using that approximation for a new production system.

## Choosing a starting point

- Start with 03 when validating integral conventions on a small molecule.
- Compare 03 and 04 before relying on an ISDF rank for a new system.
- Use 05 to study the additional FNO truncation error.
- Use 06 only after the full-X ISDF calculation is understood and validated;
  rank-$M$ X is an explicit approximation, not the default.
