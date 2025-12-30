"""
Exercise service for frontend data operations.

This service wraps the exercise loading functionality from the agent tools
and provides additional methods for the UI.
"""

from __future__ import annotations

from typing import Any

from ai_physio_assistant.agent.tools import _load_all_exercises
from ai_physio_assistant.models.exercise import BodyRegion, Difficulty


class ExerciseService:
    """Service for exercise data operations."""

    def __init__(self) -> None:
        """Initialize the exercise service."""
        self._exercises: dict[str, dict[str, Any]] | None = None

    @property
    def exercises(self) -> dict[str, dict[str, Any]]:
        """Lazily load and cache all exercises."""
        if self._exercises is None:
            self._exercises = _load_all_exercises()
        return self._exercises

    def get_all(self) -> list[dict[str, Any]]:
        """Get all exercises as a list."""
        return list(self.exercises.values())

    def get_by_id(self, exercise_id: str) -> dict[str, Any] | None:
        """Get a single exercise by ID."""
        return self.exercises.get(exercise_id)

    def get_multiple(self, exercise_ids: list[str]) -> list[dict[str, Any]]:
        """Get multiple exercises by their IDs, preserving order."""
        return [self.exercises[eid] for eid in exercise_ids if eid in self.exercises]

    def search(
        self,
        query: str = "",
        body_regions: list[str] | None = None,
        difficulty: str | None = None,
        condition: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search and filter exercises.

        Args:
            query: Text search in name and description
            body_regions: Filter by body regions (any match)
            difficulty: Filter by exact difficulty level
            condition: Filter by condition (partial match)

        Returns:
            List of matching exercises
        """
        results = []

        for ex in self.exercises.values():
            # Text search
            if query:
                query_lower = query.lower()
                name_match = query_lower in ex.get("name", "").lower()
                desc_match = query_lower in ex.get("description", "").lower()
                if not (name_match or desc_match):
                    continue

            # Body region filter
            if body_regions:
                ex_regions = [r.lower() for r in ex.get("body_regions", [])]
                if not any(br.lower() in ex_regions for br in body_regions):
                    continue

            # Difficulty filter
            if difficulty:
                if ex.get("difficulty", "").lower() != difficulty.lower():
                    continue

            # Condition filter
            if condition:
                conditions = ex.get("conditions", [])
                if not any(condition.lower() in c.lower() for c in conditions):
                    continue

            results.append(ex)

        return results

    def get_body_regions(self) -> list[str]:
        """Get all available body regions."""
        return [r.value for r in BodyRegion]

    def get_difficulty_levels(self) -> list[str]:
        """Get all available difficulty levels."""
        return [d.value for d in Difficulty]

    def get_all_conditions(self) -> list[str]:
        """Get all unique conditions from exercises."""
        conditions: set[str] = set()
        for ex in self.exercises.values():
            conditions.update(ex.get("conditions", []))
        return sorted(conditions)

    def get_exercises_by_region(self) -> dict[str, list[dict[str, Any]]]:
        """Get exercises grouped by body region."""
        by_region: dict[str, list[dict[str, Any]]] = {}

        for ex in self.exercises.values():
            for region in ex.get("body_regions", ["uncategorized"]):
                if region not in by_region:
                    by_region[region] = []
                by_region[region].append(ex)

        return by_region

    def count(self) -> int:
        """Get total number of exercises."""
        return len(self.exercises)


# Singleton instance for the app
_exercise_service: ExerciseService | None = None


def get_exercise_service() -> ExerciseService:
    """Get the singleton ExerciseService instance."""
    global _exercise_service
    if _exercise_service is None:
        _exercise_service = ExerciseService()
    return _exercise_service
