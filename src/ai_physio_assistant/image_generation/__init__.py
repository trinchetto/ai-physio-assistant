"""
Image generation service using Stable Diffusion XL.

This module provides tools for generating anatomically accurate
exercise illustrations using SDXL with medical-style prompting.
"""

from .config import PRESETS, ImageGenerationConfig
from .prompts import BodyPosition, ExercisePrompt, ViewAngle, get_prompts_for_exercise
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
