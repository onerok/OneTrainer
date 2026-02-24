---
name: new-lora
description: Create a new LoRA training configuration for OneTrainer. Helps the user pick a training preset, configure their dataset, set a trigger word, and generates a ready-to-use training config JSON. Use when users ask to "train a lora", "new lora", "create a lora config", "set up lora training", or want to start training a LoRA adapter.
---

# New LoRA Training Config

Guide the user through creating a complete LoRA training configuration for OneTrainer.

## Workflow

### Step 1: Choose a Training Preset

Present the available LoRA presets from `training_presets/` grouped by model family. Use AskUserQuestion to let them pick. Include VRAM requirements where noted in the filename.

**Available LoRA Presets (grouped by model):**

| Model Family | Preset File | Base Model | Notes |
|---|---|---|---|
| **SD 1.5** | `#sd 1.5 LoRA.json` | stable-diffusion-v1-5 | Classic, low VRAM |
| **SD 2.0** | `#sd 2.0 inpaint LoRA.json` | SD 2.0 inpainting | Inpainting only |
| **SD 2.1** | `#sd 2.1 LoRA.json` | stabilityai/sd-2-1 | |
| **SD 3** | `#sd 3 LoRA.json` | stabilityai/sd-3-medium | |
| **SDXL** | `#sdxl 1.0 LoRA.json` | stabilityai/sdxl-base-1.0 | |
| **SDXL Inpaint** | `#sdxl 1.0 inpaint LoRA.json` | SDXL inpainting | |
| **FLUX.1** | `#flux LoRA.json` | black-forest-labs/FLUX.1-dev | |
| **FLUX.2** | `#flux2 LoRA 8GB.json` | FLUX.2-klein-base-9B | 8GB VRAM |
| **FLUX.2** | `#flux2 LoRA 16GB.json` | FLUX.2-klein-base-9B | 16GB VRAM |
| **PixArt Sigma** | `#pixart sigma 1.0 LoRA.json` | PixArt Sigma | |
| **Chroma** | `#chroma LoRA 8GB.json` | lodestones/Chroma1-HD | 8GB VRAM |
| **Chroma** | `#chroma LoRA 16GB.json` | lodestones/Chroma1-HD | 16GB VRAM |
| **Chroma** | `#chroma LoRA 24GB.json` | lodestones/Chroma1-HD | 24GB VRAM |
| **HiDream** | `#hidream LoRA.json` | HiDream | |
| **Hunyuan Video** | `#hunyuan video LoRA.json` | Hunyuan Video | Video model |
| **Wuerstchen** | `#wuerstchen 2.0 LoRA.json` | Wuerstchen 2.0 | |
| **Qwen** | `#qwen LoRA 16GB.json` | Qwen | 16GB VRAM |
| **Qwen** | `#qwen LoRA 24GB.json` | Qwen | 24GB VRAM |
| **Z-Image** | `#z-image LoRA 8GB.json` | Tongyi-MAI/Z-Image | 8GB VRAM |
| **Z-Image** | `#z-image LoRA 16GB.json` | Tongyi-MAI/Z-Image | 16GB VRAM |
| **Z-Image DeTurbo** | `#z-image DeTurbo LoRA 8GB.json` | Z-Image DeTurbo | 8GB VRAM |
| **Z-Image DeTurbo** | `#z-image DeTurbo LoRA 16GB.json` | Z-Image DeTurbo | 16GB VRAM |

Group the options for the user by popularity/relevance. The most commonly used are FLUX.1, FLUX.2, SDXL, Z-Image, Chroma, and SD 1.5.

### Step 2: Ask for Dataset Details

Use AskUserQuestion or direct conversation to gather:

1. **Dataset path** (required): Absolute path to the directory containing training images. Each image should have a corresponding `.txt` caption file with the same name.
2. **Trigger word** (required): A unique token that activates the LoRA concept (e.g., "ohwx", "sks", a made-up word). This should appear in captions and sample prompts.
3. **Project name** (required): A short name for this training run (used for workspace dir, cache dir, and output filename). Example: "my-character-lora"

### Step 3: Read the Chosen Preset

Read the selected preset JSON file from `training_presets/`. This provides the base configuration with model-appropriate defaults for:
- `model_type`, `training_method`, `base_model_name`
- `batch_size`, `learning_rate`, `resolution`
- Component configs (transformer/unet, text_encoder, vae dtypes)
- Quantization, layer filtering, timestep distribution

### Step 4: Generate the Training Config

Create a complete training config JSON that merges the preset with user-specific settings. The output file goes in `training_configs/<project-name>.json`.

**Structure of the generated config:**

Start with ALL fields from the preset, then add/override these:

```json
{
    // ... all preset fields preserved exactly ...

    "epochs": 9999,
    "output_model_format": "SAFETENSORS",
    "output_model_destination": "models/<project-name>-lora.safetensors",

    "workspace_dir": "workspace/<project-name>",
    "cache_dir": "workspace-cache/<project-name>",

    "optimizer": {
        "optimizer": "ADAMW_8BIT",
        "weight_decay": 0.00001,
        "stochastic_rounding": true
    },

    "backup_after": 250,
    "backup_after_unit": "STEP",
    "rolling_backup": true,
    "rolling_backup_count": 3,

    "sample_after": 250,
    "sample_after_unit": "STEP",

    "concepts": [
        {
            "name": "<trigger-word>",
            "path": "<dataset-path>",
            "enabled": true,
            "balancing": 1.0,
            "loss_weight": 1.0,
            "image": {
                "enable_crop_jitter": true,
                "enable_random_flip": false,
                "enable_fixed_flip": false
            },
            "text": {
                "prompt_source": "sample"
            }
        }
    ],

    "samples": [
        {
            "enabled": true,
            "prompt": "a photo of <trigger-word>",
            "negative_prompt": "",
            "height": <resolution-from-preset>,
            "width": <resolution-from-preset>,
            "seed": 42,
            "random_seed": false,
            "diffusion_steps": 30,
            "cfg_scale": 4.0,
            "noise_scheduler": "EULER"
        }
    ]
}
```

**Resolution mapping for samples:** Use the `resolution` field from the preset for both height and width. Common values: SD1.5=512, SDXL/SD3/Z-Image=1024, FLUX=768.

**cfg_scale for samples:** Use 4.0 for flow-matching models (FLUX, SD3, Z-Image, Chroma, Qwen) and 7.0 for non-flow-matching models (SD1.5, SD2.x, SDXL, PixArt, Wuerstchen).

**noise_scheduler for samples:** Use "EULER" as a safe default for all models.

### Step 5: Confirm and Save

1. Write the config to `training_configs/<project-name>.json`
2. Show the user the generated config
3. Tell them how to start training:
   ```
   ./run-cmd.sh train --config-path training_configs/<project-name>.json
   ```

## Important Notes

- Always read the actual preset file before generating the config — do not hardcode preset values
- Preserve all preset fields exactly as-is; only add the concept/sample/workspace/backup/optimizer fields
- The `concepts` array replaces the `concept_file_name` field (inline concepts take precedence)
- `prompt_source: "sample"` means captions are loaded from `.txt` files alongside images
- If the user wants to customize learning rate, LoRA rank, epochs, or other parameters, incorporate those overrides
- The `training_configs/` directory may need to be created if it doesn't exist
- Do NOT include fields that are already at their default values unless they came from the preset
