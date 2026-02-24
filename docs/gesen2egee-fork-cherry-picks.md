# gesen2egee Fork Cherry-Picks

Summary of features cherry-picked from [gesen2egee/OneTrainer](https://github.com/gesen2egee/OneTrainer) and what was left behind.

Source: `gesen2egee/master` as of 2026-02-24 (14 unique commits ahead of upstream).

---

## Merged

### 1. Flow Matching Loss Weight Functions
**Source:** `4119608` | **Local:** `587746f`

Extends `ModelSetupDiffusionLossMixin._flow_matching_losses()` to support MIN_SNR_GAMMA, P2, and Debiased Estimation loss weighting for flow matching models. Previously these raised `NotImplementedError`. The implementation simulates SNR from sigma (`SNR = 1/sigma^2`) and applies the standard weighting formulas adapted for v-prediction.

Single file, 42 lines. Cleanest commit in the fork.

### 2. LoKr (Low-Rank Kronecker Product) PEFT
**Source:** `c61108a` + cleanup from `48b2fd7` | **Local:** `b6e3ea9`

Adds `LokrModule` with Kronecker product decomposition for Linear and Conv2d layers, following the existing `LoHaModule` pattern. Includes `LOKR` PeftType enum, `lokr_factor` config parameter (-1 for automatic), and LoraTab UI integration.

The `lycoris-lora` dependency (`016ec95`) was intentionally skipped -- the `LokrModule` is a custom reimplementation that does not use the lycoris library. The `inspect_lokr.py` debug script from the original commit was excluded.

### 3. Progressive Timestep Distribution + NEG_SQUARE
**Source:** `793c214` | **Local:** `bcac933`

Two features in one commit:

- **Progressive timestep distribution:** Gradually transitions from uniform to the target timestep distribution over training epochs. Controlled by a `progressive_timestep_distribution` toggle. Helps stabilize early training by avoiding aggressive distributions before the model has warmed up. Works for both continuous and discrete timestep sampling.
- **NEG_SQUARE distribution:** A `-x^2` distribution that emphasizes middle timesteps (~0.5) and de-emphasizes extremes (~0, ~1), useful for preventing loss spikes.

Currently only wired through `BaseZImageSetup.py` (passes `train_progress` to the noise mixin). Other flow matching model setups (Flux, SD3, Chroma, etc.) would need the same one-line addition to benefit.

### 4. Random Noise Shift and Multiplier
**Source:** `4c3d8e5` | **Local:** `9cadf69`

Adds two noise augmentation parameters to `ModelSetupNoiseMixin`:

- `random_noise_shift`: Per-channel additive Gaussian shift noise (similar to offset noise but random per sample). Set to 0 to disable.
- `random_noise_multiplier`: Per-channel multiplicative noise via `exp(randn * sigma)`. Set to 0 to disable.

Includes TrainingTab UI entries with tooltips. The original commit's `.vscode/settings.json` and `.pyc` binary file were excluded.

---

## Not Merged

### AutomagicSinkGD Optimizer
**Commits:** `bab3376` + `48b2fd7` + `d4eb9ee`

A custom optimizer combining SinkGD matrix normalization, Allora row-scaling, Orthograd projection, per-parameter adaptive LR masking, EMA momentum, and Kahan summation. Evolved through three commits (Automagic -> AutomagicSinkGD -> Automagic_Sinkgd) with significant API changes between each.

**Why not:** Experimental -- went through multiple incompatible rewrites. Class naming is inconsistent (mixed snake_case). Some community members reported success on Z-Image LoRA training, but the optimizer lacks upstream review and the three commits need squashing and cleanup before use. Could be revisited if it gains more community traction.

### MeanCache Sampling Acceleration
**Commits:** `d9d6e9f` + `b070dbd` + `00568c8` + `e3e3acc`

Training-free inference acceleration for Flow Matching sampling using JVP-based velocity correction and pre-computed skip schedules (PSSP). Offers quality/balanced/speed/turbo presets targeting 1.3x-2.2x speedup.

**Why not:** Too experimental. Four commits of rewrites within two days indicates instability. Only supports Z-Image (not Flux, SD3, etc.). Includes dead code (`meancache_wrapper.py` base class is unused) and a Chinese-language README. Quality impact has not been validated. Could be revisited once the approach stabilizes.

### AI Agent Working Notes
**Commit:** `c92e677`

Four metadata files (`.agent/conflict_report.md`, `.agent/upstream_conflict_report.md`, `local_changes.txt`, `upstream_changes.txt`) that appear to be AI-generated analysis accidentally committed.

**Why not:** Not code -- working notes that don't belong in the repo.

### Lycoris-lora Dependency
**Commit:** `016ec95`

Adds `lycoris-lora==3.4.0` to requirements.

**Why not:** The LoKr implementation we merged is a custom reimplementation that doesn't depend on the lycoris library. The only code that used lycoris was the `inspect_lokr.py` debug script, which was excluded. Adding an unused dependency would be unnecessary bloat.

### Merge Commit
**Commit:** `663ad6a`

Merge from upstream Nerogar/OneTrainer master.

**Why not:** Merge commit with no unique content.
