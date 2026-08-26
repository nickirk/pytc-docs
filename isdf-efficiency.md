# ISDF Efficiency Paths

PyTC 0.2.1 adds three complementary ISDF construction controls and an
optional compilation cache. The exact full-X path remains the default. The
rank-$M$ orbital-X approximation is opt-in and must be validated for each new
system.

| Control | Where to set it | Default | Effect |
|---|---|---|---|
| Blocked pivots | `ISDFXTC.from_xtc(..., batch_size=...)` | `batch_size=1` | Selects several exact columns per blocked update |
| Exact auxiliary K1/K3 recovery | `ISDFXTC.isdf(..., reuse_aux_kernels=...)` | Enabled when in-core or when a persistent output path is available | Reuses L/H auxiliary objects to recover exact K1/K3 |
| Rank-$M$ orbital X | `ISDFXTC.isdf(..., n_factor=M)` | `None` | Stores `U` and `Z` instead of dense X |
| Persistent GPU compilation cache | `PYTC_XLA_CACHE_DIR` | Disabled | Reuses compiled XLA programs across runs |

## Blocked deterministic pivot selection

`batch_size=1` preserves the historical exact-greedy selector. A value larger
than one enables blocked selection; `candidate_oversampling` controls the
candidate pool that is exactly re-pivoted within each round, and `n_topup`
reserves final singleton greedy pivots.

```python
isdf_xtc = xtc.ISDFXTC.from_xtc(
    xtc_obj,
    n_rank=n_rank,
    is_incore=True,
    batch_size=32,
    candidate_oversampling=2,
    n_topup=0,
)
```

The pivot controls are recorded in persistent ISDF caches. Reopening a cache
with different controls fails instead of silently reusing incompatible
pivots. Compare the resulting energy with `batch_size=1` when qualifying a
new system.

## Exact auxiliary recovery of K1 and K3

The auxiliary-recovery path is exact: it changes how K1 and K3 are
constructed, not their mathematical definition. PyTC enables it by default
for in-core calculations and for out-of-core calculations that have a
persistent output path.

```python
isdf_xtc = isdf_xtc.isdf(
    jastrow_params,
    reuse_aux_kernels=True,
)
```

An explicit `True` on an out-of-core object requires `save_path`, because the
L/H auxiliary datasets must be streamed from persistent storage:

```python
isdf_xtc = xtc.ISDFXTC.from_xtc(
    xtc_obj,
    n_rank=n_rank,
    is_incore=False,
    save_path="isdf_intermediates.h5",
)
isdf_xtc = isdf_xtc.isdf(jastrow_params, reuse_aux_kernels=True)
```

## Rank-$M$ orbital X and factor-direct CCSD

Passing `n_factor=M` replaces dense `X[r,s,c]` with orbital Tucker factors
`U[r,a]` and `Z[a,b,c]`. The dedicated factorized solver contracts T2
directly with U/Z and avoids reconstructing dense X or a four-virtual tile.

```python
from pytc.solver import isdf_xtc_ccsd

isdf_xtc = xtc.ISDFXTC.from_xtc(
    xtc_obj,
    n_rank=n_rank,
    is_incore=True,
)
isdf_xtc = isdf_xtc.isdf(
    jastrow_params,
    n_factor=80,
    batch_size=64,
)

assert "X" not in isdf_xtc.isdf_kernels
assert "X_tucker" in isdf_xtc.isdf_kernels

mycc = isdf_xtc_ccsd.RCCSD(
    mf,
    isdf_xtc,
    jastrow_params,
    on_the_fly_vvvv=True,
)
eris = mycc.ao2mo()
try:
    e_corr, t1, t2 = mycc.kernel(eris=eris)
finally:
    eris.close()
```

The complete small-system version is
[`06_rank_m_x_factor_direct_ccsd.py`](https://github.com/nickirk/pytc/blob/v0.2.1/pytc/examples/06_rank_m_x_factor_direct_ccsd.py).

### Validation requirement

Rank-$M$ X is an approximation. Version 0.2.1 validates $M=80$ only on the
reported H10/cc-pVTZ/grid2 gate, where it changed the exact-pivot total energy
by -0.844607 mHa. That result is not a transferable error bound. For each new
system, converge $M$ against the full-X result and report the total-energy
difference before using the approximation in production.

## Persistent XLA compilation cache

Set an approved absolute path before starting Python:

```bash
export PYTC_XLA_CACHE_DIR=/project/my-group/pytc-xla-cache
python my_xtc_ccsd_calculation.py
```

The ISDF xTC-CCSD solver enables the cache when this variable is present.
Without it, caching is disabled. See [GPU Memory Management](gpu-memory.md)
for the other runtime controls.
