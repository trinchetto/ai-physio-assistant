"""
Tools for the AI Physio Assistant agent.

These tools allow the agent to search exercises, get exercise details,
and create personalized routines for patients.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ai_physio_assistant.models.exercise import BodyRegion, Difficulty

# Cache for loaded exercises
_exercises_cache: dict[str, dict[str, Any]] | None = None


def _get_content_dir() -> Path:
    """Get the content directory path."""
    # Navigate from src/ai_physio_assistant/agent/ to content/
    return Path(__file__).parent.parent.parent.parent / "content" / "exercises"


def _load_all_exercises() -> dict[str, dict[str, Any]]:
    """Load all exercises from YAML files into memory."""
    global _exercises_cache

    if _exercises_cache is not None:
        return _exercises_cache

    exercises: dict[str, dict[str, Any]] = {}
    content_dir = _get_content_dir()

    if not content_dir.exists():
        return exercises

    for yaml_file in content_dir.rglob("*.yaml"):
        # Skip template file
        if yaml_file.name.startswith("_"):
            continue

        try:
            with open(yaml_file, encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data and "id" in data:
                    exercises[data["id"]] = data
        except Exception:
            # Skip files that can't be loaded
            continue

    _exercises_cache = exercises
    return exercises


def list_body_regions() -> str:
    """
    List all available body regions that exercises can target.

    Returns a list of body regions that can be used to filter exercises.

    Returns:
        A formatted string listing all available body regions.
    """
    regions = [region.value for region in BodyRegion]
    return "Available body regions:\n" + "\n".join(f"- {r}" for r in regions)


def list_difficulty_levels() -> str:
    """
    List all available difficulty levels for exercises.

    Returns:
        A formatted string listing all difficulty levels.
    """
    levels = [level.value for level in Difficulty]
    return "Available difficulty levels:\n" + "\n".join(f"- {lvl}" for lvl in levels)


def search_exercises(
    body_region: str | None = None,
    condition: str | None = None,
    difficulty: str | None = None,
    therapeutic_goal: str | None = None,
    equipment: str | None = None,
    max_results: int = 10,
) -> str:
    """
    Search for exercises based on various criteria.

    Use this tool to find exercises that match specific requirements.
    All filter parameters are optional and can be combined.

    Args:
        body_region: Filter by body region (e.g., 'neck', 'shoulder', 'lower_back').
                    Use list_body_regions() to see all options.
        condition: Filter by medical condition (e.g., 'neck_pain', 'sciatica').
        difficulty: Filter by difficulty level ('beginner', 'intermediate', 'advanced').
        therapeutic_goal: Filter by goal (e.g., 'reduce_pain', 'improve_mobility', 'strengthen').
        equipment: Filter by required equipment (e.g., 'none', 'resistance_band', 'dumbbell').
        max_results: Maximum number of results to return (default 10).

    Returns:
        A formatted string listing matching exercises with their key details.
    """
    exercises = _load_all_exercises()
    results: list[dict[str, Any]] = []

    for _exercise_id, exercise in exercises.items():
        # Apply filters
        if body_region:
            regions = exercise.get("body_regions", [])
            if body_region.lower() not in [r.lower() for r in regions]:
                continue

        if condition:
            conditions = exercise.get("conditions", [])
            # Partial match for conditions
            if not any(condition.lower() in c.lower() for c in conditions):
                continue

        if difficulty:
            if exercise.get("difficulty", "").lower() != difficulty.lower():
                continue

        if therapeutic_goal:
            goals = exercise.get("therapeutic_goals", [])
            if not any(therapeutic_goal.lower() in g.lower() for g in goals):
                continue

        if equipment:
            equip = exercise.get("equipment", [])
            if equipment.lower() not in [e.lower() for e in equip]:
                continue

        results.append(exercise)

        if len(results) >= max_results:
            break

    if not results:
        return "No exercises found matching the specified criteria."

    # Format results
    output_lines = [f"Found {len(results)} exercise(s):\n"]
    for ex in results:
        regions = ", ".join(ex.get("body_regions", []))
        diff = ex.get("difficulty", "unknown")
        output_lines.append(f"- **{ex['name']}** (ID: {ex['id']})")
        output_lines.append(f"  Body regions: {regions} | Difficulty: {diff}")
        # Truncate description for brevity
        desc = ex.get("description", "")[:150]
        if len(ex.get("description", "")) > 150:
            desc += "..."
        output_lines.append(f"  {desc}")
        output_lines.append("")

    return "\n".join(output_lines)


def get_exercise_details(exercise_id: str) -> str:
    """
    Get complete details for a specific exercise.

    Use this tool to get full information about an exercise including
    instructions, common mistakes, contraindications, and parameters.

    Args:
        exercise_id: The unique ID of the exercise (e.g., 'chin_tuck', 'cat_cow_stretch').

    Returns:
        Formatted details of the exercise or an error message if not found.
    """
    exercises = _load_all_exercises()

    if exercise_id not in exercises:
        available = list(exercises.keys())[:10]
        return f"Exercise '{exercise_id}' not found. Some available IDs: {', '.join(available)}..."

    ex = exercises[exercise_id]

    lines = [
        f"# {ex['name']}",
        "",
        f"**ID:** {ex['id']}",
        f"**Difficulty:** {ex.get('difficulty', 'N/A')}",
        f"**Body Regions:** {', '.join(ex.get('body_regions', []))}",
        "",
        "## Description",
        ex.get("description", "No description available."),
        "",
        "## Instructions",
    ]

    for i, instruction in enumerate(ex.get("instructions", []), 1):
        lines.append(f"{i}. {instruction}")

    lines.append("")
    lines.append("## Common Mistakes to Avoid")
    for mistake in ex.get("common_mistakes", []):
        lines.append(f"- {mistake}")

    lines.append("")
    lines.append("## Default Parameters")
    lines.append(f"- Sets: {ex.get('default_sets', 3)}")
    lines.append(f"- Reps: {ex.get('default_reps', '10-12')}")
    if ex.get("default_hold"):
        lines.append(f"- Hold: {ex.get('default_hold')}")
    lines.append(f"- Rest: {ex.get('default_rest', '30 seconds')}")

    if ex.get("conditions"):
        lines.append("")
        lines.append("## Conditions This Helps")
        lines.append(", ".join(ex.get("conditions", [])))

    if ex.get("contraindications"):
        lines.append("")
        lines.append("## Contraindications (Do NOT use if patient has)")
        for contra in ex.get("contraindications", []):
            lines.append(f"- {contra}")

    if ex.get("equipment") and ex.get("equipment") != ["none"]:
        lines.append("")
        lines.append(f"## Equipment Needed: {', '.join(ex.get('equipment', []))}")

    return "\n".join(lines)


def list_all_exercises() -> str:
    """
    List all available exercises in the database.

    Returns a summary of all exercises organized by body region.

    Returns:
        A formatted string listing all exercises grouped by body region.
    """
    exercises = _load_all_exercises()

    if not exercises:
        return "No exercises found in the database."

    # Group by body region
    by_region: dict[str, list[dict[str, Any]]] = {}
    for ex in exercises.values():
        for region in ex.get("body_regions", ["uncategorized"]):
            if region not in by_region:
                by_region[region] = []
            by_region[region].append(ex)

    lines = [f"Total exercises: {len(exercises)}\n"]
    for region in sorted(by_region.keys()):
        lines.append(f"## {region.replace('_', ' ').title()}")
        for ex in sorted(by_region[region], key=lambda x: x.get("name", "")):
            diff = ex.get("difficulty", "")
            lines.append(f"- {ex['name']} ({ex['id']}) - {diff}")
        lines.append("")

    return "\n".join(lines)


def get_exercises_for_condition(condition: str) -> str:
    """
    Find all exercises recommended for a specific medical condition.

    Use this when a patient presents with a particular diagnosis or symptom.

    Args:
        condition: The medical condition (e.g., 'neck_pain', 'sciatica',
                  'rotator_cuff', 'plantar_fasciitis').

    Returns:
        A list of exercises that help with the specified condition.
    """
    return search_exercises(condition=condition, max_results=20)


def create_routine_draft(
    patient_name: str,
    diagnosis: str,
    therapeutic_goals: list[str],
    exercise_ids: list[str],
    frequency: str = "once daily",
    general_notes: str | None = None,
) -> str:
    """
    Create a draft routine for a patient with selected exercises.

    This creates a structured routine that can be reviewed and delivered to the patient.

    Args:
        patient_name: The patient's name for the handout.
        diagnosis: Primary diagnosis or reason for treatment.
        therapeutic_goals: List of goals (e.g., ['reduce pain', 'improve mobility']).
        exercise_ids: List of exercise IDs to include in the routine.
        frequency: How often to perform (e.g., 'once daily', 'twice daily', '3x per week').
        general_notes: Optional notes or context for the patient.

    Returns:
        A formatted routine draft that can be reviewed by the physiotherapist.
    """
    exercises = _load_all_exercises()

    # Validate exercises exist
    valid_exercises = []
    invalid_ids = []
    for ex_id in exercise_ids:
        if ex_id in exercises:
            valid_exercises.append(exercises[ex_id])
        else:
            invalid_ids.append(ex_id)

    if invalid_ids:
        return f"Error: The following exercise IDs were not found: {', '.join(invalid_ids)}"

    if not valid_exercises:
        return "Error: No valid exercises provided for the routine."

    # Build routine draft
    lines = [
        "=" * 60,
        "EXERCISE ROUTINE DRAFT",
        "=" * 60,
        "",
        f"**Patient:** {patient_name}",
        f"**Diagnosis:** {diagnosis}",
        f"**Goals:** {', '.join(therapeutic_goals)}",
        f"**Frequency:** {frequency}",
        "",
    ]

    if general_notes:
        lines.append(f"**Notes:** {general_notes}")
        lines.append("")

    # Estimate total time
    total_time = len(valid_exercises) * 3  # ~3 min per exercise average
    lines.append(f"**Estimated Session Duration:** {total_time}-{total_time + 5} minutes")
    lines.append("")
    lines.append("-" * 60)
    lines.append("EXERCISES")
    lines.append("-" * 60)

    for i, ex in enumerate(valid_exercises, 1):
        lines.append("")
        lines.append(f"### {i}. {ex['name']}")
        lines.append(f"- Sets: {ex.get('default_sets', 3)}")
        lines.append(f"- Reps: {ex.get('default_reps', '10-12')}")
        if ex.get("default_hold"):
            lines.append(f"- Hold: {ex.get('default_hold')}")
        lines.append(f"- Rest: {ex.get('default_rest', '30 seconds')}")
        lines.append("")
        lines.append("Instructions:")
        for j, instruction in enumerate(ex.get("instructions", [])[:5], 1):
            lines.append(f"  {j}. {instruction}")

    lines.append("")
    lines.append("-" * 60)
    lines.append("SAFETY REMINDERS")
    lines.append("-" * 60)
    lines.append("- Stop immediately if you experience sharp or sudden pain")
    lines.append("- Contact your physiotherapist if symptoms worsen")
    lines.append("- Perform exercises in a slow, controlled manner")
    lines.append("")
    lines.append("=" * 60)
    lines.append("END OF ROUTINE DRAFT")
    lines.append("=" * 60)

    return "\n".join(lines)
