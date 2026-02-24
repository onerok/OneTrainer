# Z-Image LoRA Training Guide for OneTrainer

> Community-aggregated guide for training LoRAs on Z-Image Base (ZiB) and Z-Image Turbo (ZiT).
> Compiled February 2026 from community sources listed in [Sources](#sources).
>
> **This repo note**: Several features originally from the [gesen2egee fork](https://github.com/gesen2egee/OneTrainer) have been cherry-picked into this repo (see [docs/gesen2egee-fork-cherry-picks.md](gesen2egee-fork-cherry-picks.md)). Where this guide says "fork only", those features are now available here too. Credit for these features belongs entirely to gesen2egee — we are consumers, not maintainers, of that code. If the cherry-picks fall behind or break, the gesen2egee fork remains the authoritative source.

---

## Table of Contents

- [Understanding Z-Image Base vs Turbo](#understanding-z-image-base-vs-turbo)
- [Z-Image Base LoRA Training](#z-image-base-lora-training)
  - [The Two Critical Fixes](#the-two-critical-fixes)
  - [Mainline-Compatible Config (Adafactor)](#mainline-compatible-config-adafactor)
  - [Recommended Fork Config (Prodigy_ADV)](#recommended-fork-config-prodigy_adv)
  - [Alternative Fork Config (automagic_sinkgd + LoKR)](#alternative-fork-config-automagic_sinkgd--lokr)
- [Z-Image Turbo LoRA Training](#z-image-turbo-lora-training)
  - [The Distillation Problem](#the-distillation-problem)
  - [Four Training Schemes](#four-training-schemes)
  - [Recommended: Standard SFT + DistillPatch (Scheme 4)](#recommended-standard-sft--distillpatch-scheme-4)
- [Inference / Generation](#inference--generation)
  - [Using ZiB LoRAs at Inference Time](#using-zib-loras-at-inference-time)
  - [ZiB LoRAs on ZiT](#zib-loras-on-zit)
- [Dataset Preparation](#dataset-preparation)
- [Tuning Guide for Subsequent Runs](#tuning-guide-for-subsequent-runs)
- [VRAM Optimization](#vram-optimization)
- [Troubleshooting](#troubleshooting)
- [Sources](#sources)

---

## Understanding Z-Image Base vs Turbo

| Aspect | Z-Image Base (ZiB) | Z-Image Turbo (ZiT) |
| --- | --- | --- |
| Model ID | `Tongyi-MAI/Z-Image` | `Tongyi-MAI/Z-Image-Turbo` |
| Inference steps | 30-50 | 8 |
| CFG scale | 2-7 | 1 |
| Architecture | Flow matching (Logit Normal + Dynamic Timestep Shift) | Step-distilled from ZiB |
| Text encoder | Single Qwen3 (Qwen3ForCausalLM) | Single Qwen3 (Qwen3ForCausalLM) |
| LoRA training | Supported (with caveats below) | Supported (with training adapter or DistillPatch) |

**Critical fact**: ZiB was updated *after* ZiT was released. This means the two models have diverged and **ZiB-trained LoRAs do not work cleanly on ZiT's base weights** (though many users report success with adjustments -- see [ZiB LoRAs on ZiT](#zib-loras-on-zit)).

> **Codebase note**: Z-Image uses flow-matching losses internally (`_flow_matching_losses`) but `ModelType.Z_IMAGE.is_flow_matching()` returns `False` in the OneTrainer enum. This classification inconsistency affects which UI options are shown. On upstream mainline, MIN_SNR_GAMMA appears selectable but crashes at runtime with `NotImplementedError`. This repo includes the gesen2egee fix (see [The Two Critical Fixes](#the-two-critical-fixes)).

---

## Z-Image Base LoRA Training

### The Two Critical Fixes

Z-Image Base has two well-documented training problems. Both must be addressed:

#### 1. Convergence / Loss Spikes → Min SNR Gamma = 5

ZiB exhibits abnormal loss spikes at low timesteps (0-50) and high timesteps (950-1000). The Logit Normal timestep distribution used by Z-Image creates sparse sampling at these extremes, causing instability -- especially at small batch sizes. [[1]](#sources)

**Fix**: Set `loss_weight_fn = MIN_SNR_GAMMA` with `loss_weight_strength = 5.0`.

> **Note**: Some users question whether Min SNR Gamma makes theoretical sense for flow-matching architectures, since it was originally proposed for epsilon-prediction diffusion models [[2]](#sources). However, empirical results across multiple users confirm it dramatically improves training stability for ZiB. [[1]](#sources) [[3]](#sources)

**Availability**: MIN_SNR_GAMMA exists in the upstream OneTrainer `LossWeight` enum, and the UI will show it as an option for Z-Image. However, **upstream mainline's `_flow_matching_losses()` does NOT implement it** -- selecting it will crash with `NotImplementedError` at runtime.

This repo includes the [gesen2egee](https://github.com/gesen2egee/OneTrainer) fix for MIN_SNR_GAMMA on flow matching models (cherry-picked from `4119608`). **If you are running upstream mainline, you must use the gesen2egee fork instead.**

What is available in this repo (cherry-picked from gesen2egee):

- `MIN_SNR_GAMMA`, `P2`, and `DEBIASED_ESTIMATION` loss weighting for flow matching models
- `LoKR` PEFT type
- Progressive timestep distribution
- `NEG_SQUARE` timestep distribution
- `random_noise_shift` and `random_noise_multiplier` noise augmentation

What is available in upstream mainline (no fork needed):

- `PRODIGY_ADV` optimizer with stochastic rounding
- `FLOAT_32_STOCHASTIC` gradient reduce precision
- `LOGIT_NORMAL` timestep distribution
- Other `_adv` optimizer variants

What still requires the [gesen2egee fork](https://github.com/gesen2egee/OneTrainer) directly:

- `AUTOMAGIC_SINKGD` optimizer
- `allora` and `use_kahan` optimizer parameters
- MeanCache sampling acceleration

#### 2. Precision Sensitivity → Stochastic Rounding

ZiB is extremely sensitive to precision loss from quantization and rounding. Standard fp8 quantization degrades training quality significantly. [[1]](#sources) [[3]](#sources)

**Fix**: Use an optimizer with **stochastic rounding** enabled:

- `PRODIGY_ADV` (stochastic rounding enabled by default) -- available in mainline
- `AUTOMAGIC_SINKGD` (includes Kahan summation, similar effect) -- fork only
- Any `_adv` optimizer variant in OneTrainer (stochastic rounding on by default) -- available in mainline

Additionally, set `gradient_reduce_precision = FLOAT_32_STOCHASTIC` and keep the transformer in `BFLOAT_16` (not quantized lower).

> **Note on official presets**: The official OneTrainer Z-Image LoRA presets (`#z-image LoRA 16GB.json`, `#z-image LoRA 8GB.json`) use `FLOAT_8` for the transformer to save VRAM. This works but the community consensus [[1]](#sources) [[2]](#sources) is that avoiding quantization below BF16 produces noticeably better training quality. The presets prioritize broad hardware support over maximum quality.

---

### Mainline-Compatible Config (Adafactor)

From u/FennelFetish on the OneTrainer GitHub Discussion #1281 [[5]](#sources). This works on **mainline OneTrainer without any fork** and has produced good character LoRAs. This is the recommended starting point if you do not want to use the gesen2egee fork.

| Parameter | Value | Notes |
| --- | --- | --- |
| **Base model** | `Tongyi-MAI/Z-Image` | Must be HuggingFace diffusers format |
| **Training method** | LORA | |
| **LoRA rank** | 16 | |
| **LoRA alpha** | 1 | |
| **Layer preset** | Full (attn-mlp also works) | |
| **Optimizer** | Adafactor | Available in mainline |
| **Learning rate** | 1e-4 | |
| **Scheduler** | Constant | |
| **Precision** | BF16, NO quantization | Keep transformer at BFLOAT_16 |
| **Batch size** | 2 | |
| **Resolution** | Mixed 1024-1536 | |
| **Offset noise** | 0.02 | |
| **Perturbation noise** | 0.01 | |
| **Timestep shift** | 1.33 | |
| **Timestep distribution** | LOGIT_NORMAL | |
| **VRAM** | ~20GB | |

**Text encoder**: Z-Image has a single Qwen3 text encoder. This config does not train it. Set `text_encoder.train = false`.

Good likeness achieved at step ~2000 with 400 images. Works in ComfyUI with ZiT at LoRA strength 1.75.

**Trade-off**: This approach does not use Min SNR Gamma (which is available in this repo but not upstream mainline) and may be less consistent with smaller datasets (under 50 images). For small datasets, consider the Prodigy_ADV config below which uses MIN_SNR_GAMMA. [[6]](#sources) Some users report AdamW8bit also works acceptably with a cosine scheduler (not constant LR), though this is debated.

---

### Recommended Fork Config (Prodigy_ADV)

**Originally requires the [gesen2egee fork](https://github.com/gesen2egee/OneTrainer)** for MIN_SNR_GAMMA support. This repo includes the cherry-picked fix, so this config works here. On upstream mainline, MIN_SNR_GAMMA will crash.

This is the most widely tested and confirmed working configuration, from u/EribusYT [[2]](#sources). Multiple community members have verified it produces good character and style LoRAs.

| Parameter | Value | Notes |
| --- | --- | --- |
| **Base model** | `Tongyi-MAI/Z-Image` | Must be HuggingFace diffusers format |
| **Training method** | LORA | |
| **LoRA rank** | 64 | |
| **LoRA alpha** | 64 | Rank = alpha (ratio of 1) |
| **LoRA weight dtype** | FLOAT_32 | |
| **Layer filter preset** | attn-mlp | Attention + feed_forward layers only |
| **Optimizer** | PRODIGY_ADV | |
| **Learning rate** | 1.0 | Prodigy auto-adjusts; set LR to 1.0 |
| **Scheduler** | CONSTANT | |
| **Warmup steps** | 50 | |
| **Stochastic rounding** | true | Critical for ZiB |
| **Loss weight function** | MIN_SNR_GAMMA | Available here; crashes on upstream mainline |
| **Loss weight strength** | 5.0 | |
| **Epochs** | 120 | For 30-60 image datasets |
| **Batch size** | 1 | |
| **Gradient accumulation** | 4 | Effective batch size of 4 |
| **Resolution** | 1024 | |
| **Train dtype** | BFLOAT_16 | |
| **Transformer weight dtype** | BFLOAT_16 | Do NOT quantize lower |
| **Gradient checkpointing** | ON | |
| **Gradient reduce precision** | FLOAT_32_STOCHASTIC | |
| **Timestep distribution** | LOGIT_NORMAL | Matches ZiB's training distribution |
| **`dynamic_timestep_shifting`** | true | Note the field name ends in `ing` |
| **Clip grad norm** | 1.0 | |
| **Aspect ratio bucketing** | true | |
| **Latent caching** | true | |
| **Compile** | true | |

#### Prodigy_ADV Optimizer Settings

Parameters available in mainline:

| Parameter | Value | Mainline |
| --- | --- | --- |
| beta1 | 0.9 | Yes |
| beta2 | 0.99 | Yes |
| d0 | 1e-06 | Yes |
| eps | 1e-08 | Yes |
| stochastic_rounding | true | Yes |
| use_stableadamw | true | Yes |
| use_schedulefree | true | Yes |
| factored | true | Yes |
| factored_fp32 | true | Yes |
| split_groups | true | Yes |
| split_groups_mean | true | Yes |
| rms_rescaling | true | Yes |
| weight_decay | 0.0 | Yes |
| weight_decay_by_lr | true | Yes |
| allora | true | **gesen2egee fork only** |
| use_kahan | true | **gesen2egee fork only** |

`allora` and `use_kahan` are only functional on the gesen2egee fork. They are not included in this repo's cherry-picks and will be ignored on upstream mainline. The config still works without them — they are optimizations, not requirements.

#### Text Encoder Settings

Z-Image has a **single** Qwen3 text encoder (not multiple like SD3 or HiDream):

| Component | Weight dtype | Train |
| --- | --- | --- |
| text_encoder (Qwen3) | FLOAT_8 | false |
| transformer | BFLOAT_16 | true |
| vae | FLOAT_32 | false |

> **Note**: The source config [[2]](#sources) lists four text encoders (TE1-TE4), which appears to be from a multi-encoder model template. Z-Image's `ZImageModel` class only defines a single `text_encoder: Qwen3ForCausalLM`. The mainline UI also disables text encoder training for Z-Image (`supports_training=False`). If the fork enables TE training, consult the fork documentation.

#### Dataset / Caption Settings

| Parameter | Value |
| --- | --- |
| Tag dropout mode | RANDOM WEIGHTED |
| Tag dropout probability | 0.05 |
| Text variations | 12 (increase for larger datasets) |
| Keep tags count | 1 |
| Enable crop jitter | true |
| Enable random flip | false (for characters; true OK for styles) |

**Training time**: ~8 hours on an RTX 3090 with 40-80 images at 1024 resolution. [[2]](#sources)

**Full config**: [pastebin.com/XCJmutM0](https://pastebin.com/XCJmutM0) -- MIN_SNR_GAMMA works in this repo. `allora` and `use_kahan` require the [gesen2egee fork](https://github.com/gesen2egee/OneTrainer) but are optional. [[2]](#sources)

---

### Alternative Fork Config (automagic_sinkgd + LoKR)

**Originally requires the [gesen2egee fork](https://github.com/gesen2egee/OneTrainer)** for AUTOMAGIC_SINKGD, LoKR, and MIN_SNR_GAMMA. This repo includes cherry-picked LoKR and MIN_SNR_GAMMA support, but **AUTOMAGIC_SINKGD still requires the fork**.

From u/Personal_Speed2326 [[1]](#sources), the original researcher who identified the Min SNR Gamma and precision fixes. This approach uses LoKR instead of LoRA and a custom optimizer.

| Parameter | Value | Notes |
| --- | --- | --- |
| **PEFT type** | LoKR | Full rank LoKR (available here) |
| **LoKR factor** | 8-12 | OP recommends 10 |
| **LoKR rank** | Very high | Set extremely high for full rank |
| **Optimizer** | AUTOMAGIC_SINKGD | Includes Kahan summation (**gesen2egee fork only**) |
| **Learning rate** | 0.0003 | Like AdamW-scale LR |
| **Scheduler** | REX or Cosine | With 100 warmup steps |
| **Resolution** | 512 | Enables 12GB VRAM training |
| **Epochs** | 100 | |
| **Loss weight function** | MIN_SNR_GAMMA | Strength = 5 (available here) |
| **SVD Quant** | BF16, Rank 16 | Memory optimization |

A user (u/RetroGazzaSpurs) [[1]](#sources) reported their best-ever ZiB LoRA with a variant:

- LoKR rank 16, factor 1, alpha 1
- automagic_sinkgd, constant scheduler, LR 0.0003
- Min SNR Gamma = 5
- Pre-cropped images to training resolution

**Full config**: [pastebin.com/TracMG7Z](https://pastebin.com/TracMG7Z) (requires [gesen2egee fork](https://github.com/gesen2egee/OneTrainer)) [[1]](#sources)

---

## Z-Image Turbo LoRA Training

### The Distillation Problem

Z-Image Turbo is a step-distilled model optimized for 8-step generation. Standard LoRA fine-tuning **disrupts the distillation trajectory** [[4]](#sources):

- Quality degrades at 8 steps (the whole point of Turbo)
- Quality only recovers at 30+ steps (defeating the purpose)
- The model effectively becomes a worse version of ZiB

### Four Training Schemes

From the [HuggingFace blog by kelseye](https://huggingface.co/blog/kelseye/training-strategies-of-z-image-turbo) [[4]](#sources):

| Scheme | Training | Inference | Speed | Quality | Complexity |
| --- | --- | --- | --- | --- | --- |
| **1. Standard SFT** | Normal LoRA training | 30 steps, cfg=2 | Slow | High | Low |
| **2. Differential LoRA** | Train with ostris adapter | 8 steps, cfg=1 | Fast | Moderate | Low |
| **3. SFT + Distillation** | Two-stage training | 8 steps, cfg=1 | Fast | High | High |
| **4. SFT + DistillPatch** | Normal LoRA training | 8 steps + DistillPatch LoRA | Fast | High | Low |

### Recommended: Standard SFT + DistillPatch (Scheme 4)

This is the recommended approach for most users:

1. **Train** using standard SFT on ZiT (same parameters as Scheme 1)
2. **At inference**, load both your LoRA AND the [DistillPatch LoRA](https://www.modelscope.cn/models/DiffSynth-Studio/Z-Image-Turbo-DistillPatch) to restore 8-step acceleration

#### Training Parameters for ZiT

These parameters are from the HuggingFace blog [[4]](#sources), which uses DiffSynth-Studio. The equivalent OneTrainer layer filter preset for these target modules is `attn-mlp`.

| Parameter | Value | Notes |
| --- | --- | --- |
| Base model | `Tongyi-MAI/Z-Image-Turbo` | |
| Learning rate | 1e-4 | |
| LoRA rank | 32 | |
| LoRA target layers | `attn-mlp` preset | Equivalent to `to_q, to_k, to_v, to_out.0, w1, w2, w3` in diffusers |
| Gradient checkpointing | Enabled | |
| Max pixels | 1,048,576 (e.g. 1024x1024) | |

#### Using the ostris Training Adapter (Scheme 2)

If you prefer staying at 8 steps without the DistillPatch:

1. Load [`ostris/zimage_turbo_training_adapter`](https://huggingface.co/ostris/zimage_turbo_training_adapter) during training
2. This adapter "un-distills" the model so your LoRA doesn't break the acceleration
3. **Remove the adapter at inference** -- keep only your LoRA
4. Best for short training runs (styles, concepts, characters)
5. Long training runs will still degrade distillation

> The adapter was originally made for AI Toolkit but the concept works in any trainer.

---

## Inference / Generation

### Using ZiB LoRAs at Inference Time

**The key discovery** [[2]](#sources): ZiB LoRAs do NOT work well when applied directly to the Z-Image Base model. You need a **distilled checkpoint** derived from ZiB.

| Setting | Recommended Value |
| --- | --- |
| **Checkpoint** | A ZiB-derived distill (e.g., [RedCraft ZiB Distill](https://civitai.com/models/958009)) |
| **Scheduler** | Euler Simple |
| **Shift** | 7 |
| **CFG scale** | 1.5 |
| **Resolution** | 2048x2048 (noticeably better) or 1024x1024 |
| **Steps** | 5-20 (depends on distill) |

**Alternative**: A distill LoRA applied to the base model also works, as long as the distill LoRA is compatible with the checkpoint.

### ZiB LoRAs on ZiT

Community reports are mixed but lean positive:

- **u/Wild-Perspective-582** [[2]](#sources): "I have trained 100s of character LoRAs using ZIB. And then I use them in ZIT and they look great." (LoRA strength at 1.0)
- **u/sirdrak** [[3]](#sources): OneTrainer + Prodigy_ADV LoRAs work on ZiT at normal strength 1 (key: must use proper optimizer with stochastic rounding)
- **u/FennelFetish** [[5]](#sources): Works in ComfyUI with ZiT at LoRA strength 1.75
- **Some users** [[3]](#sources) report needing strength 1.5-2.0+, with inconsistent results

**The reverse does NOT work**: ZiT-trained LoRAs on ZiB produce garbled output. [[2]](#sources) [[3]](#sources)

**Recommendation**: Train on ZiB, test on both a ZiB distill and ZiT. Adjust LoRA strength as needed for ZiT (try 1.0 first, increase to 1.5-1.75 if likeness is weak).

---

## Dataset Preparation

| Aspect | Recommendation |
| --- | --- |
| **Image count** | 30-60 for characters/styles; 20 works for simple concepts |
| **Captioning** | Don't over-describe inherent features of the subject. DO describe distractions/elements to separate from subject [[1]](#sources) |
| **Caption length** | Long captions preferred. Short tags can cause structural instability. Mix of long/short wildcards is acceptable [[1]](#sources) |
| **Trigger word** | If the character name appears in every caption, it acts as the trigger word |
| **Pre-cropping** | Pre-crop to training resolution using [Malcolm's dataset tool](https://huggingface.co/spaces/malcolmrey/dataset-preparation) for better results [[1]](#sources) |
| **Text variations** | 12 minimum, increase for larger datasets. Generates multiple caption permutations per image to improve generalization |
| **Tag dropout** | Random Weighted, probability 0.05 |
| **Flipping** | Disable for characters (asymmetric features); OK for styles |

---

## Tuning Guide for Subsequent Runs

### Reading Your Training Samples

Sample every 5 epochs (or every 250-500 steps). Look for:

| Symptom | Diagnosis | Fix |
| --- | --- | --- |
| Samples look like random noise | Training hasn't converged | Continue training; if still noise after 30+ epochs, check Min SNR Gamma is enabled (fork) or increase gradient accumulation |
| Subject appears but blurry/unstable | Underbaked | Continue training; check precision settings |
| Perfect likeness but artifacts | Slightly overbaked | Use an earlier checkpoint (backup every 5 epochs) |
| Colors/contrast look washed out | Precision issue | Verify stochastic rounding is on; check transformer is BF16 not quantized |
| Style but no character likeness | LoRA not learning identity | Increase rank; increase epochs; improve captions |
| Good character but wrong style | Over-training | Reduce epochs; try a lower rank |
| Loss oscillates wildly | Timestep instability | Enable Min SNR Gamma = 5 (available here; fork or upstream will crash); increase gradient accumulation |
| Loss flatlines early | Learning rate too low or optimizer stuck | For Prodigy, verify LR is 1.0; for others, try increasing LR |

### Parameter Tuning Priority

When adjusting between runs, change **one thing at a time** in this priority order:

1. **Epochs** (most impactful): Start at 120 for 30-60 images. Reduce if overbaking, increase if underbaked
2. **LoRA rank**: 64 is a good default. Try 32 if overfitting, 128 if underfitting complex styles
3. **Gradient accumulation**: Increase from 4 to 8 if training is unstable; acts like a larger batch size
4. **Text variations**: Increase from 12 to 20+ for diverse datasets
5. **Resolution**: Train at 1024 if VRAM allows; 512 works but produces lower quality

### Estimating Training Duration

**Rule of thumb**: ~100 epochs for 30-60 images (each epoch shows every image once at batch_size=1).

| Images | Epochs | Approximate time (3090, 1024px) |
| --- | --- | --- |
| 30 | 120 | ~6 hours |
| 50 | 100 | ~8 hours |
| 80 | 80 | ~10 hours |
| 400 | 15-20 | Varies by batch size |

### A/B Testing Tips

- Save backups every 5 epochs. Your best checkpoint is rarely the last one
- Compare outputs at the same seed and prompt across checkpoints
- Test with both simple prompts ("a photo of [trigger]") and complex prompts ("a photo of [trigger] standing on a beach at sunset, wearing a red jacket")
- Generate at 2048x2048 when evaluating -- ZiB excels at high resolution

---

## VRAM Optimization

| VRAM | What to change |
| --- | --- |
| **24GB** | Use recommended config as-is |
| **16GB** | Reduce resolution to 768 or 512; reduce batch size to 1; enable CPU offloading |
| **12GB** | Use LoKR at 512 (available here) + automagic_sinkgd (fork only) or substitute another optimizer; SVD Quant BF16 rank 16; enable all offloading |
| **8GB** | Very difficult. Try 512 resolution + maximum offloading. May not work |

**Important**: The community recommends keeping the transformer at BFLOAT_16 for best quality [[1]](#sources) [[2]](#sources). The official OneTrainer presets use FLOAT_8 to fit in less VRAM -- this works but may reduce training quality. Reduce resolution or batch size before resorting to quantization.

Other memory-saving options:

- `enable_async_offloading: true`
- `enable_activation_offloading: true`
- `gradient_checkpointing: ON`
- `latent_caching: true`
- `compile: true`

---

## Troubleshooting

### "LoRA produces garbled output"

Two different scenarios:

- **ZiB LoRA on ZiT**: Try increasing LoRA strength to 1.5-1.75. Verify you trained with stochastic rounding enabled. Many users report ZiB LoRAs work on ZiT at strength 1.0, so garbled output may indicate a training issue rather than incompatibility. [[2]](#sources) [[3]](#sources)
- **ZiT LoRA on ZiB**: This genuinely does not work. The model weight spaces have diverged. Use a ZiB distill for inference instead. [[2]](#sources) [[3]](#sources)

### "Loss spikes wildly during training"

- Enable Min SNR Gamma = 5 (available in this repo; crashes on upstream mainline)
- Increase gradient accumulation steps
- Verify Logit Normal timestep distribution and `dynamic_timestep_shifting` are enabled

### "Training converges but outputs look washed out"

- Check that transformer is BFLOAT_16 (not fp8 quantized)
- Verify stochastic rounding or Kahan summation is enabled
- Avoid AdamW8bit -- use Prodigy_ADV, automagic_sinkgd, or Adafactor [[6]](#sources)

### "ComfyUI shows only noise"

- ComfyUI may use a different model format. Use the [conversion script](https://huggingface.co/Comfy-Org/z_image_turbo/blob/main/z_image_convert_original_to_comfy.py)
- Ensure output format is SAFETENSORS

### "RuntimeError: negative dimension with LoKR"

- LoKR factor/rank combination is incompatible. Use factor 8-12 with a very high rank for full rank LoKR. LoKR is available in this repo (cherry-picked from gesen2egee).

### "NotImplementedError: Loss weight function MIN_SNR_GAMMA not implemented for flow matching models"

- You are running upstream mainline OneTrainer, which does not support MIN_SNR_GAMMA for flow matching models. This repo includes the fix (cherry-picked from gesen2egee). If you see this error, you're likely on upstream mainline — switch to this repo, the [gesen2egee fork](https://github.com/gesen2egee/OneTrainer), or use the [Mainline-Compatible Config (Adafactor)](#mainline-compatible-config-adafactor) instead.

### "8GB VRAM OOM even at 512"

- The gesen2egee fork may be less VRAM-optimized than main OneTrainer
- Try the main branch with Adafactor instead

### "How do I verify I have the fork features?"

- If MIN_SNR_GAMMA doesn't crash on Z-Image training, the flow matching fix is present (this repo or gesen2egee fork).
- If `LoKR` appears in the PEFT type dropdown, LoKR support is present.
- If `automagic_sinkgd` appears in the optimizer list, you're on the full gesen2egee fork (not cherry-picked into this repo).

---

## Sources

Numbered references cited throughout the guide with `[[N]]` notation.

1. **u/Personal_Speed2326** -- ["Thoughts and Solutions on Z-IMAGE Training Issues"](https://www.reddit.com/r/StableDiffusion/comments/1qwc4t0/) -- r/StableDiffusion, ~June 2025. Original research identifying the Min SNR Gamma fix, precision sensitivity, and timestep distribution problems. Creator of the [gesen2egee OneTrainer fork](https://github.com/gesen2egee/OneTrainer).

2. **u/EribusYT** -- ["Providing a Working Solution to Z-Image Base Training"](https://www.reddit.com/r/StableDiffusion/comments/1r9r9qb/) -- r/StableDiffusion, ~Feb 20, 2026. Community-verified Prodigy_ADV config, ZiB distill inference discovery, and the most widely adopted training recipe. [Config: pastebin.com/XCJmutM0](https://pastebin.com/XCJmutM0). [Companion Civitai article](https://civitai.com/articles/26358).

3. **u/orangeflyingmonkey_ et al.** -- ["Is it recommended to train LoRA on ZiB even if I plan to use it on ZiT?"](https://www.reddit.com/r/StableDiffusion/comments/1r9upvn/) -- r/StableDiffusion, ~Feb 2026. Community discussion on ZiB-to-ZiT LoRA compatibility, AI Toolkit configs, and optimizer comparisons. Notable contributions from u/sirdrak (Prodigy_ADV on ZiT), u/an80sPWNstar ([AI Toolkit configs](https://pastebin.com/u/an80sPWNstar/1/dVknBYSB)), u/Sufficient-Maize-687 (dataset guidance), u/siegekeebsofficial (weight decay testing).

4. **kelseye** -- ["Training Strategies of Z-Image-Turbo"](https://huggingface.co/blog/kelseye/training-strategies-of-z-image-turbo) -- HuggingFace Blog. Comprehensive comparison of four ZiT training schemes. Source for the DistillPatch approach (Scheme 4) and the [ostris training adapter](https://huggingface.co/ostris/zimage_turbo_training_adapter) documentation.

5. **OneTrainer GitHub Discussion #1281** -- ["Z-Image non-Turbo"](https://github.com/Nerogar/OneTrainer/discussions/1281). Community troubleshooting and alternative configs, including u/FennelFetish's Adafactor approach and dxqb (OneTrainer collaborator) notes on quantization and format support.

6. **u/mangoking1997** [[2]](#sources) -- Dissenting view that AI Toolkit works fine with AdamW8bit for ZiB, but recommends cosine scheduler (not constant LR). Corroborated by u/PineAmbassador who confirmed Adafactor works in AI Toolkit (40 images, batch 8, 690 steps).

### Additional Resources

| Resource | Link |
| --- | --- |
| gesen2egee OneTrainer fork (authoritative source for all fork features) | [github.com/gesen2egee/OneTrainer](https://github.com/gesen2egee/OneTrainer) |
| Cherry-pick details (what we took, what we didn't, why) | [docs/gesen2egee-fork-cherry-picks.md](gesen2egee-fork-cherry-picks.md) |
| RedCraft ZiB Distill (for inference) | [civitai.com/models/958009](https://civitai.com/models/958009) |
| ostris ZiT Training Adapter | [huggingface.co/ostris/zimage_turbo_training_adapter](https://huggingface.co/ostris/zimage_turbo_training_adapter) |
| Z-Image-Turbo DistillPatch | [modelscope.cn/.../Z-Image-Turbo-DistillPatch](https://www.modelscope.cn/models/DiffSynth-Studio/Z-Image-Turbo-DistillPatch) |
| Malcolm's Dataset Preparation | [huggingface.co/spaces/malcolmrey/dataset-preparation](https://huggingface.co/spaces/malcolmrey/dataset-preparation) |
| ComfyUI Conversion Script | [huggingface.co/Comfy-Org/z_image_turbo](https://huggingface.co/Comfy-Org/z_image_turbo/blob/main/z_image_convert_original_to_comfy.py) |
| r/ZImageAI subreddit | [reddit.com/r/ZImageAI](https://www.reddit.com/r/ZImageAI/) |
| EribusYT's Civitai Profile (example results) | [civitai.com/user/Erebussy/models](https://civitai.com/user/Erebussy/models) |
| EribusYT's config (Prodigy_ADV) | [pastebin.com/XCJmutM0](https://pastebin.com/XCJmutM0) |
| Personal_Speed2326's config (LoKR) | [pastebin.com/TracMG7Z](https://pastebin.com/TracMG7Z) |

---

*This guide reflects community knowledge as of February 2026. Z-Image tooling is evolving rapidly -- check the linked discussions and the [gesen2egee fork](https://github.com/gesen2egee/OneTrainer) for the latest features. Features cherry-picked into this repo may fall behind the fork over time.*
