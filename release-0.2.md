# Release 0.2.0

## Added

- **Factorized ISDF xTC-CCSD solver** (`pytc.solver.isdf_xtc_ccsd`): a JAX
  RCCSD path that never materializes the full four-virtual tile. The large X
  factor is streamed one rank panel at a time through a three-tier residency
  gate — device lift, host-resident, or store stream — chosen from measured
  free device and host memory (cgroup-aware, reclaimable-cache accounting,
  fail-closed when memory is unmeasurable). Working-set panels with
  double-buffered prefetch and a halving retry on device out-of-memory.
- **`pytc.df` package**: the previous `pytc.df` module is now a package with
  the same public API. `pytc.df.thc` adds the panelled NumPy and JAX robust
  DF-THC fits and sandwiches, plus X-store layout helpers: stores can carry
  an optional rank-major twin dataset (`X_rm`) giving contiguous panel reads;
  twins are provenance-stamped and rebuilt when their source changes.
- **Strictly opt-in per-term timers** (`pytc.utils.tile_timers`): per-term
  wall timers and counters for the solver. Zero accumulation and zero
  behavior change when disabled (the default).
- Converged 1200-orbital on-the-fly xTC-CCSD on a single B200-class GPU:
  the factorized solver completes a 1200-orbital benzene (cc-pCV5Z/cc-pV5Z)
  calculation in about 9 hours on one GPU, versus about 29 hours on 8 GPUs
  with the previous route, at FP64 precision.

## Removed

- `pytc.optimize` (broken; clean removal).
- `pytc.utils.perf_baseline`.
- Example scripts: `Be_vmc_ref_opt_xtc_ccsd.py`,
  `benchmark_isdf_xtc_kdx.py`, `co2_simple_jastrow_xtc_ccsd.py`,
  `h2o_jastrow_xtc_isdf_ccsd.py`, `h2o_jax_isdf_xtc.py`.

## Notes

- The tier gate and timers are off by default; behavior is unchanged unless
  the corresponding environment pins are set at call time.
- Stores without an `X_rm` twin behave exactly as before; the twin is an
  optional conversion produced by the layout helpers in `pytc.df.thc`.
- `psutil` is optional: the memory gate falls back to cgroup-only
  measurement when it is absent.
