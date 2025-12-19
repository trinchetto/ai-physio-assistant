"""
Configuration for SDXL image generation.

Recommended models and LoRAs for medical/anatomical illustrations:

BASE MODELS (pick one):
- stabilityai/stable-diffusion-xl-base-1.0 (default SDXL)
- RunDiffusion/Juggernaut-XL-v9 (good for realistic anatomy)

RECOMMENDED LoRAs (from CivitAI or HuggingFace):
- Medical illustration style LoRAs
- Anatomy diagram LoRAs
- Line art / technical drawing LoRAs

Place LoRA files in: models/loras/
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ImageGenerationConfig:
    """Configuration for the image generation service."""

    # Model settings
    model_id: str = "stabilityai/stable-diffusion-xl-base-1.0"
    refiner_id: str | None = "stabilityai/stable-diffusion-xl-refiner-1.0"
    use_refiner: bool = False  # Refiner can improve details but slower

    # LoRA settings (optional)
    lora_path: str | None = None  # Path to medical/anatomy LoRA
    lora_weight: float = 0.8  # LoRA influence strength

    # Generation settings
    num_inference_steps: int = 30
    guidance_scale: float = 7.5
    width: int = 1024
    height: int = 1024

    # Consistency settings
    use_fixed_seed: bool = True
    base_seed: int = 42  # For reproducibility

    # Output settings
    output_dir: Path = field(default_factory=lambda: Path("content/images/exercises"))
    output_format: str = "png"

    # Hardware settings
    device: str = "cuda"  # "cuda", "mps" (Mac), or "cpu"
    dtype: str = "float16"  # "float16" for GPU, "float32" for CPU
    enable_attention_slicing: bool = True  # Reduce VRAM usage
    enable_vae_tiling: bool = True  # For large images with limited VRAM

    # Style settings (embedded in all prompts)
    style_prefix: str = (
        "anatomical diagram, physiotherapy illustration, medical reference style, "
        "clean simple lines, professional medical textbook illustration, "
        "gender-neutral human figure, accurate anatomical proportions"
    )
    style_suffix: str = (
        "clean white background, no text, no labels, no watermarks, "
        "high contrast black lines, minimal shading, educational diagram"
    )

    negative_prompt: str = (
        "photo, photograph, realistic skin texture, face details, "
        "colored background, text, labels, watermark, signature, "
        "blurry, low quality, distorted anatomy, extra limbs, "
        "artistic, painterly, sketch, rough lines"
    )


# Preset configurations for different use cases
PRESETS = {
    "fast": ImageGenerationConfig(
        num_inference_steps=20,
        use_refiner=False,
        guidance_scale=7.0,
    ),
    "quality": ImageGenerationConfig(
        num_inference_steps=40,
        use_refiner=True,
        guidance_scale=8.0,
    ),
    "low_vram": ImageGenerationConfig(
        num_inference_steps=25,
        use_refiner=False,
        width=768,
        height=768,
        enable_attention_slicing=True,
        enable_vae_tiling=True,
    ),
}
