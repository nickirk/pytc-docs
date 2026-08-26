# Release 0.2.1

PyTC 0.2.1 adds validated efficiency paths for constructing and consuming
ISDF xTC intermediates.

## Added

- Deterministic blocked pivot selection for molecular ISDF.
- Exact auxiliary recovery of K1 and K3, including streamed out-of-core
  construction with cache provenance.
- An opt-in rank-$M$ orbital Tucker representation of X and direct T2-U-Z
  contraction in the factorized ISDF xTC-CCSD solver.
- An opt-in persistent XLA compilation cache.
- A standalone rank-$M$ / factor-direct example:
  `06_rank_m_x_factor_direct_ccsd.py`.

## Changed and fixed

- Accelerator-memory probes fail closed when capacity cannot be measured
  reliably.
- Disk-backed X panels remain bounded during the JAX CCSD direct-tile path.
- Delta-U dispatch sizing no longer double-counts an already resident D
  kernel.
- Rank-major X-store conversion retains the source layout and adds a
  provenance-stamped twin for legacy compatibility.

## Validation scope

On H10/R=1.6/cc-pVTZ/grid2, exact auxiliary recovery reduced K1/K3
construction from 324.90 s to 89.62 s on one V100, with K1/K3 relative errors
below $1.2\times10^{-15}$.

On the corresponding one-A100 gate, blocked pivot selection was 9.515 times
faster in the relaxed-energy run and changed the full-X total energy by
+0.000267 mHa. The opt-in $M=80$ orbital-X approximation changed the
exact-pivot total energy by -0.844607 mHa. Transfer beyond this H10 gate and a
matched rank-$M$ construction speedup have not been established.

See [ISDF Efficiency Paths](isdf-efficiency.md) for API usage and validation
guidance.
