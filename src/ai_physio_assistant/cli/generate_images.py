#!/usr/bin/env python3
"""
Command-line tool for generating exercise illustrations.

Usage:
    # After installing the package:
    physio-generate-images --all
    physio-generate-images --exercise chin_tuck
    physio-generate-images --list

    # Or run directly:
    python -m ai_physio_assistant.cli.generate_images --all
"""

import argparse
import logging
import sys
from pathlib import Path

from ai_physio_assistant.image_generation import (
    ImageGenerationConfig,
    PRESETS,
    get_prompts_for_exercise,
)
from ai_physio_assistant.image_generation.service import (
    ImageGenerationService,
    generate_all_seed_exercises,
)
from ai_physio_assistant.image_generation.prompts import get_all_exercise_ids


def setup_logging(verbose: bool = False) -> None:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )


def list_exercises() -> None:
    """List all available exercises with prompts."""
    print("\nAvailable exercises:")
    print("-" * 40)
    for exercise_id in get_all_exercise_ids():
        prompts = get_prompts_for_exercise(exercise_id)
        print(f"  {exercise_id}: {len(prompts)} images")
    print()


def generate_single_exercise(
    exercise_id: str,
    config: ImageGenerationConfig,
    dry_run: bool = False,
) -> bool:
    """Generate images for a single exercise."""
    prompts = get_prompts_for_exercise(exercise_id)
    if not prompts:
        print(f"Error: No prompts found for exercise '{exercise_id}'")
        print("Use --list to see available exercises")
        return False

    print(f"\nGenerating {len(prompts)} images for: {exercise_id}")

    if dry_run:
        print("\n[DRY RUN] Would generate with these prompts:")
        for prompt in prompts:
            full_prompt = prompt.build_prompt(
                style_prefix=config.style_prefix,
                style_suffix=config.style_suffix,
            )
            print(f"\n  Image {prompt.image_order}:")
            print(f"    {full_prompt[:100]}...")
        return True

    service = ImageGenerationService(config)
    try:
        service.load_model()
        results = service.generate_exercise_images(exercise_id, save=True)

        print(f"\nGenerated {len(results)} images:")
        for image, path in results:
            if path:
                print(f"  - {path}")

        return True

    except Exception as e:
        print(f"Error generating images: {e}")
        return False
    finally:
        service.unload_model()


def generate_all(config: ImageGenerationConfig, dry_run: bool = False) -> bool:
    """Generate images for all seed exercises."""
    exercise_ids = get_all_exercise_ids()
    print(f"\nGenerating images for {len(exercise_ids)} exercises...")

    if dry_run:
        for exercise_id in exercise_ids:
            prompts = get_prompts_for_exercise(exercise_id)
            print(f"  {exercise_id}: {len(prompts)} images")
        print("\n[DRY RUN] No images generated")
        return True

    results = generate_all_seed_exercises(config)

    print("\nGeneration complete:")
    total = 0
    for exercise_id, paths in results.items():
        print(f"  {exercise_id}: {len(paths)} images")
        total += len(paths)

    print(f"\nTotal: {total} images generated")
    return True


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate exercise illustrations using SDXL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Action arguments
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--exercise", "-e",
        type=str,
        help="Generate images for a specific exercise ID",
    )
    action.add_argument(
        "--all", "-a",
        action="store_true",
        help="Generate images for all seed exercises",
    )
    action.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available exercises",
    )

    # Configuration arguments
    parser.add_argument(
        "--preset", "-p",
        type=str,
        choices=list(PRESETS.keys()),
        help="Use a preset configuration (fast, quality, low_vram)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="stabilityai/stable-diffusion-xl-base-1.0",
        help="SDXL model ID or path",
    )
    parser.add_argument(
        "--lora",
        type=str,
        help="Path to LoRA weights for medical/anatomy style",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=30,
        help="Number of inference steps (default: 30)",
    )
    parser.add_argument(
        "--guidance",
        type=float,
        default=7.5,
        help="Guidance scale (default: 7.5)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Base random seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--device",
        type=str,
        choices=["cuda", "mps", "cpu"],
        default="cuda",
        help="Device to use (default: cuda)",
    )

    # Output arguments
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        help="Output directory for generated images",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without running",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    # Handle list command
    if args.list:
        list_exercises()
        return 0

    # Build configuration
    if args.preset:
        config = PRESETS[args.preset]
    else:
        config = ImageGenerationConfig()

    # Apply command-line overrides
    config.model_id = args.model
    config.lora_path = args.lora
    config.num_inference_steps = args.steps
    config.guidance_scale = args.guidance
    config.base_seed = args.seed
    config.device = args.device

    if args.output_dir:
        config.output_dir = Path(args.output_dir)

    # Generate images
    if args.exercise:
        success = generate_single_exercise(args.exercise, config, args.dry_run)
    else:  # args.all
        success = generate_all(config, args.dry_run)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
