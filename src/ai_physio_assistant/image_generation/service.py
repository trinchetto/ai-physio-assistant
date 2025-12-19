"""
SDXL-based image generation service for exercise illustrations.

This service generates anatomically accurate exercise illustrations
using Stable Diffusion XL with optional medical/anatomy fine-tuned models.
"""

import logging
from pathlib import Path
from typing import Optional

import torch
from PIL import Image

from .config import ImageGenerationConfig
from .prompts import ExercisePrompt, get_prompts_for_exercise

logger = logging.getLogger(__name__)


class ImageGenerationService:
    """
    Service for generating exercise illustrations using SDXL.

    Usage:
        config = ImageGenerationConfig()
        service = ImageGenerationService(config)
        service.load_model()

        # Generate single image
        image = service.generate_image(prompt, seed=42)

        # Generate all images for an exercise
        images = service.generate_exercise_images("chin_tuck")
    """

    def __init__(self, config: ImageGenerationConfig | None = None):
        self.config = config or ImageGenerationConfig()
        self.pipeline = None
        self.refiner = None
        self._loaded = False

    def load_model(self) -> None:
        """Load the SDXL model and optional refiner."""
        if self._loaded:
            logger.info("Model already loaded")
            return

        try:
            from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline

            logger.info(f"Loading SDXL model: {self.config.model_id}")

            # Determine torch dtype
            dtype = torch.float16 if self.config.dtype == "float16" else torch.float32

            # Load base model
            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                self.config.model_id,
                torch_dtype=dtype,
                use_safetensors=True,
                variant="fp16" if dtype == torch.float16 else None,
            )

            # Move to device
            self.pipeline = self.pipeline.to(self.config.device)

            # Apply memory optimizations
            if self.config.enable_attention_slicing:
                self.pipeline.enable_attention_slicing()

            if self.config.enable_vae_tiling:
                self.pipeline.enable_vae_tiling()

            # Load LoRA if specified
            if self.config.lora_path:
                logger.info(f"Loading LoRA: {self.config.lora_path}")
                self.pipeline.load_lora_weights(self.config.lora_path)

            # Load refiner if specified
            if self.config.use_refiner and self.config.refiner_id:
                logger.info(f"Loading refiner: {self.config.refiner_id}")
                self.refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                    self.config.refiner_id,
                    torch_dtype=dtype,
                    use_safetensors=True,
                    variant="fp16" if dtype == torch.float16 else None,
                )
                self.refiner = self.refiner.to(self.config.device)

            self._loaded = True
            logger.info("Model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def generate_image(
        self,
        prompt: str,
        negative_prompt: str | None = None,
        seed: int | None = None,
        num_inference_steps: int | None = None,
        guidance_scale: float | None = None,
    ) -> Image.Image:
        """
        Generate a single image from a prompt.

        Args:
            prompt: The positive prompt describing the image
            negative_prompt: Optional negative prompt (uses config default if None)
            seed: Random seed for reproducibility (uses config if None)
            num_inference_steps: Override config inference steps
            guidance_scale: Override config guidance scale

        Returns:
            PIL Image object
        """
        if not self._loaded:
            self.load_model()

        # Set defaults from config
        negative_prompt = negative_prompt or self.config.negative_prompt
        seed = seed if seed is not None else self.config.base_seed
        num_inference_steps = num_inference_steps or self.config.num_inference_steps
        guidance_scale = guidance_scale or self.config.guidance_scale

        # Create generator for reproducibility
        generator = torch.Generator(device=self.config.device).manual_seed(seed)

        logger.info(f"Generating image with seed {seed}")
        logger.debug(f"Prompt: {prompt}")

        # Generate base image
        result = self.pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            width=self.config.width,
            height=self.config.height,
            generator=generator,
        )

        image = result.images[0]

        # Apply refiner if enabled
        if self.refiner is not None:
            logger.info("Applying refiner...")
            generator = torch.Generator(device=self.config.device).manual_seed(seed)
            result = self.refiner(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image=image,
                num_inference_steps=num_inference_steps // 2,
                generator=generator,
            )
            image = result.images[0]

        return image

    def generate_from_exercise_prompt(
        self,
        exercise_prompt: ExercisePrompt,
        seed_offset: int = 0,
    ) -> Image.Image:
        """
        Generate an image from an ExercisePrompt object.

        Args:
            exercise_prompt: The structured exercise prompt
            seed_offset: Offset to add to base seed (for variations)

        Returns:
            PIL Image object
        """
        # Build the full prompt with style
        full_prompt = exercise_prompt.build_prompt(
            style_prefix=self.config.style_prefix,
            style_suffix=self.config.style_suffix,
        )

        # Calculate seed (base + exercise order for consistency within exercise)
        seed = self.config.base_seed + exercise_prompt.image_order + seed_offset

        return self.generate_image(full_prompt, seed=seed)

    def generate_exercise_images(
        self,
        exercise_id: str,
        save: bool = True,
        body_region: str | None = None,
    ) -> list[tuple[Image.Image, Path | None]]:
        """
        Generate all images for a specific exercise.

        Args:
            exercise_id: The exercise ID (must have prompts defined)
            save: Whether to save images to disk
            body_region: Body region for file path (auto-detected if None)

        Returns:
            List of (image, saved_path) tuples
        """
        prompts = get_prompts_for_exercise(exercise_id)
        if not prompts:
            raise ValueError(f"No prompts defined for exercise: {exercise_id}")

        results = []

        for prompt in prompts:
            logger.info(f"Generating {exercise_id} image {prompt.image_order}...")

            image = self.generate_from_exercise_prompt(prompt)
            saved_path = None

            if save:
                saved_path = self._save_image(
                    image=image,
                    exercise_id=exercise_id,
                    image_order=prompt.image_order,
                    body_region=body_region,
                )

            results.append((image, saved_path))

        return results

    def _save_image(
        self,
        image: Image.Image,
        exercise_id: str,
        image_order: int,
        body_region: str | None = None,
    ) -> Path:
        """Save an image to the configured output directory."""
        # Determine body region from exercise ID if not provided
        if body_region is None:
            body_region = self._infer_body_region(exercise_id)

        # Create output directory
        output_dir = self.config.output_dir / body_region
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename = f"{exercise_id}_{image_order:02d}.{self.config.output_format}"
        output_path = output_dir / filename

        # Save image
        image.save(output_path)
        logger.info(f"Saved: {output_path}")

        return output_path

    def _infer_body_region(self, exercise_id: str) -> str:
        """Infer body region from exercise ID."""
        # Map of exercise IDs to body regions
        region_map = {
            "chin_tuck": "neck",
            "pendulum_exercise": "shoulder",
            "cat_cow_stretch": "lower_back",
            "piriformis_stretch_supine": "hip",
            "calf_raises": "ankle_foot",
        }
        return region_map.get(exercise_id, "misc")

    def unload_model(self) -> None:
        """Unload model to free memory."""
        if self.pipeline is not None:
            del self.pipeline
            self.pipeline = None

        if self.refiner is not None:
            del self.refiner
            self.refiner = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        self._loaded = False
        logger.info("Model unloaded")


def generate_all_seed_exercises(config: ImageGenerationConfig | None = None) -> dict:
    """
    Generate images for all seed exercises.

    Returns:
        Dictionary mapping exercise_id to list of saved paths
    """
    from .prompts import get_all_exercise_ids

    service = ImageGenerationService(config)
    service.load_model()

    results = {}

    for exercise_id in get_all_exercise_ids():
        logger.info(f"Processing exercise: {exercise_id}")
        try:
            images = service.generate_exercise_images(exercise_id, save=True)
            results[exercise_id] = [path for _, path in images if path]
        except Exception as e:
            logger.error(f"Failed to generate images for {exercise_id}: {e}")
            results[exercise_id] = []

    service.unload_model()
    return results
