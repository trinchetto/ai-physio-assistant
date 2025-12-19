# Image Generation Guide

This guide describes how to generate exercise illustrations using the integrated SDXL-based image generation service.

## Overview

The AI Physio Assistant includes a built-in image generation service that uses **Stable Diffusion XL (SDXL)** with medical/anatomical prompting to create consistent, accurate exercise illustrations.

### Why SDXL?

- **Anatomical accuracy**: Medical-style prompts produce better anatomical illustrations
- **Consistency**: Same model + seed = reproducible results across exercises
- **Local control**: Run on your own hardware, no API costs
- **Fine-tuning**: Can use medical/anatomy LoRAs for better results

## Prerequisites

### Hardware Requirements

| Configuration | VRAM | Notes |
|---------------|------|-------|
| **Recommended** | 12GB+ GPU | Full quality, fast generation |
| **Minimum** | 8GB GPU | Use `low_vram` preset |
| **Apple Silicon** | 16GB+ RAM | Works with MPS backend |
| **CPU-only** | 32GB+ RAM | Very slow, not recommended |

### Software Setup

```bash
# 1. Install PyTorch for your hardware
# NVIDIA GPU (CUDA 12.1):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Apple Silicon:
pip install torch torchvision

# 2. Install image generation dependencies
pip install -r requirements-image-gen.txt
```

## Usage

### Command-Line Interface

```bash
# List available exercises
python scripts/generate_images.py --list

# Generate images for a specific exercise
python scripts/generate_images.py --exercise chin_tuck

# Generate all seed exercises
python scripts/generate_images.py --all

# Use quality preset (slower, better results)
python scripts/generate_images.py --all --preset quality

# Use low VRAM preset (for 8GB GPUs)
python scripts/generate_images.py --all --preset low_vram

# Dry run (show prompts without generating)
python scripts/generate_images.py --all --dry-run
```

### Python API

```python
from src.image_generation.config import ImageGenerationConfig
from src.image_generation.service import ImageGenerationService

# Create service with default config
config = ImageGenerationConfig()
service = ImageGenerationService(config)

# Load model (downloads on first run, ~6GB)
service.load_model()

# Generate images for an exercise
results = service.generate_exercise_images("chin_tuck", save=True)

# Or generate a single image with custom prompt
image = service.generate_image(
    prompt="anatomical diagram of shoulder external rotation exercise...",
    seed=42
)

# Free memory when done
service.unload_model()
```

## Prompt Structure

The service uses medical/anatomical terminology for better results:

### Anatomical Viewing Angles

| Angle | Description | Use For |
|-------|-------------|---------|
| `lateral` | Side view (profile) | Most exercises |
| `anterior` | Front view | Symmetrical movements |
| `posterior` | Back view | Back exercises |
| `oblique` | 3/4 angle | Complex positions |
| `close-up` | Detail view | Foot, hand positions |

### Body Positions

| Position | Description |
|----------|-------------|
| `standing` | Upright posture |
| `seated` | On chair |
| `supine` | Lying on back |
| `prone` | Lying face down |
| `quadruped` | On hands and knees |

### Example Prompt Structure

```python
ExercisePrompt(
    exercise_id="piriformis_stretch",
    image_order=2,
    description="figure-four stretch with ankle crossed over opposite knee",
    view_angle=ViewAngle.OBLIQUE,
    body_position=BodyPosition.SUPINE,
    muscles_shown=["piriformis muscle", "hip external rotators"],
    joints_shown=["hip external rotation"],
)
```

This generates a full prompt like:
```
anatomical diagram, physiotherapy illustration, medical reference style,
clean simple lines, professional medical textbook illustration,
gender-neutral human figure, accurate anatomical proportions,
oblique view, supine position lying on back,
figure-four stretch with ankle crossed over opposite knee,
showing piriformis muscle, hip external rotators,
highlighting hip external rotation,
clean white background, no text, no labels, no watermarks,
high contrast black lines, minimal shading, educational diagram
```

## Configuration

### Presets

| Preset | Steps | Refiner | Resolution | Use Case |
|--------|-------|---------|------------|----------|
| `fast` | 20 | No | 1024x1024 | Quick preview |
| `quality` | 40 | Yes | 1024x1024 | Final production |
| `low_vram` | 25 | No | 768x768 | Limited GPU memory |

### Custom Configuration

```python
from src.image_generation.config import ImageGenerationConfig

config = ImageGenerationConfig(
    model_id="stabilityai/stable-diffusion-xl-base-1.0",
    num_inference_steps=35,
    guidance_scale=8.0,
    base_seed=42,
    device="cuda",  # or "mps" for Mac

    # Optional: Use a medical LoRA for better anatomy
    lora_path="models/loras/medical-illustration.safetensors",
    lora_weight=0.7,
)
```

## Recommended LoRAs

For better medical/anatomical illustrations, consider these LoRAs from CivitAI:

| LoRA | Purpose |
|------|---------|
| Medical Illustration Style | Clean diagram aesthetic |
| Anatomy Reference | Accurate body proportions |
| Line Art / Technical Drawing | Clean black lines |

Place LoRA files in `models/loras/` and reference in config.

## Output Structure

Generated images are saved to:

```
content/images/exercises/
├── neck/
│   ├── chin_tuck_01.png
│   ├── chin_tuck_02.png
│   └── chin_tuck_03.png
├── shoulder/
│   └── ...
└── ...
```

## Adding New Exercises

1. **Define prompts** in `src/image_generation/prompts.py`:

```python
EXERCISE_PROMPTS["new_exercise"] = [
    ExercisePrompt(
        exercise_id="new_exercise",
        image_order=1,
        description="starting position using anatomical terminology",
        view_angle=ViewAngle.LATERAL,
        body_position=BodyPosition.STANDING,
        muscles_shown=["target muscles"],
        joints_shown=["relevant joints"],
    ),
    # ... more prompts for other positions
]
```

2. **Update body region mapping** in `service.py`:

```python
region_map = {
    # ...existing...
    "new_exercise": "body_region",
}
```

3. **Generate images**:

```bash
python scripts/generate_images.py --exercise new_exercise
```

## Troubleshooting

### Out of Memory (OOM)

```bash
# Use low_vram preset
python scripts/generate_images.py --all --preset low_vram
```

### Poor Anatomical Accuracy

- Use a medical/anatomy LoRA
- Increase guidance scale (8.0-10.0)
- Add more specific anatomical terms to prompt

### Inconsistent Style

- Use the same seed for related images
- Generate all images for an exercise in one session
- Ensure style_prefix and style_suffix are consistent

### Model Download Issues

The model downloads automatically on first run (~6GB). If interrupted:

```bash
# Clear cache and retry
rm -rf ~/.cache/huggingface/hub/models--stabilityai--stable-diffusion-xl-base-1.0
python scripts/generate_images.py --exercise chin_tuck
```

---

## Seed Exercise Prompts Reference

The following prompts are defined for the 5 seed exercises:

### Chin Tuck (Neck)

| Image | View | Description |
|-------|------|-------------|
| 1 | Lateral | Neutral cervical spine alignment, head balanced over shoulders |
| 2 | Lateral | Cervical retraction, chin drawn posteriorly, suboccipital stretch |
| 3 | Lateral | Comparison: forward head posture vs corrected position |

### Pendulum Exercise (Shoulder)

| Image | View | Description |
|-------|------|-------------|
| 1 | Lateral | Hip flexion, hand on table, arm in dependent position |
| 2 | Anterior | Circumduction movement pattern with motion indicators |
| 3 | Lateral | Sagittal plane pendular motion with motion indicators |

### Cat-Cow Stretch (Lower Back)

| Image | View | Description |
|-------|------|-------------|
| 1 | Lateral | Quadruped neutral spine (tabletop) |
| 2 | Lateral | Spinal flexion (cat pose), thoracic/lumbar kyphosis |
| 3 | Lateral | Spinal extension (cow pose), lumbar lordosis |

### Piriformis Stretch (Hip)

| Image | View | Description |
|-------|------|-------------|
| 1 | Oblique | Supine, bilateral hip/knee flexion |
| 2 | Oblique | Figure-four position, hip external rotation |
| 3 | Lateral | Full stretch, pulling leg toward chest |

### Calf Raises (Ankle/Foot)

| Image | View | Description |
|-------|------|-------------|
| 1 | Lateral | Standing, plantigrade stance, hand on wall |
| 2 | Lateral | Bilateral heel raise, plantarflexion |
| 3 | Close-up | Foot/ankle detail showing gastrocnemius/soleus |
