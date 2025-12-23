"""
Image generation service using Stable Diffusion XL.

This module provides tools for generating anatomically accurate
exercise illustrations using SDXL with medical-style prompting.
"""

from typing import TYPE_CHECKING

from .config import PRESETS, ImageGenerationConfig
from .prompts import BodyPosition, ExercisePrompt, ViewAngle, get_prompts_for_exercise

# Lazy import to avoid torch dependency when not needed
if TYPE_CHECKING:
    from .service import ImageGenerationService, generate_all_seed_exercises

__all__ = [
    "ImageGenerationConfig",
    "PRESETS",
    "ExercisePrompt",
    "ViewAngle",
    "BodyPosition",
    "get_prompts_for_exercise",
    "ImageGenerationService",
    "generate_all_seed_exercises",
]


def __getattr__(name: str) -> object:
    """Lazy import for service to avoid torch dependency."""
    if name == "ImageGenerationService":
        from .service import ImageGenerationService

        return ImageGenerationService
    if name == "generate_all_seed_exercises":
        from .service import generate_all_seed_exercises

        return generate_all_seed_exercises
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
