"""Tests for the AI agent tools."""

from ai_physio_assistant.agent.tools import (
    get_exercise_details,
    get_exercises_for_condition,
    list_all_exercises,
    list_body_regions,
    list_difficulty_levels,
    search_exercises,
)


class TestListFunctions:
    """Tests for listing functions."""

    def test_list_body_regions(self) -> None:
        """Test that body regions are listed."""
        result = list_body_regions()
        assert "neck" in result
        assert "shoulder" in result
        assert "lower_back" in result
        assert "hip" in result

    def test_list_difficulty_levels(self) -> None:
        """Test that difficulty levels are listed."""
        result = list_difficulty_levels()
        assert "beginner" in result
        assert "intermediate" in result
        assert "advanced" in result

    def test_list_all_exercises(self) -> None:
        """Test that all exercises are listed."""
        result = list_all_exercises()
        assert "Total exercises:" in result
        # Should have exercises from our database
        assert "chin_tuck" in result.lower() or "Chin Tuck" in result


class TestSearchExercises:
    """Tests for search functionality."""

    def test_search_by_body_region(self) -> None:
        """Test searching exercises by body region."""
        result = search_exercises(body_region="neck")
        assert "Found" in result
        # Should find neck exercises
        assert "neck" in result.lower() or "Chin" in result

    def test_search_by_difficulty(self) -> None:
        """Test searching exercises by difficulty."""
        result = search_exercises(difficulty="beginner")
        assert "Found" in result or "No exercises found" in result

    def test_search_no_results(self) -> None:
        """Test search with no matching results."""
        result = search_exercises(body_region="nonexistent_region")
        assert "No exercises found" in result

    def test_search_by_condition(self) -> None:
        """Test searching exercises by condition."""
        result = search_exercises(condition="neck_pain")
        # Should find exercises or return no results message
        assert "Found" in result or "No exercises found" in result


class TestGetExerciseDetails:
    """Tests for getting exercise details."""

    def test_get_valid_exercise(self) -> None:
        """Test getting details for a valid exercise."""
        result = get_exercise_details("chin_tuck")
        assert "Chin Tuck" in result
        assert "Instructions" in result
        assert "Description" in result

    def test_get_invalid_exercise(self) -> None:
        """Test getting details for an invalid exercise ID."""
        result = get_exercise_details("nonexistent_exercise")
        assert "not found" in result


class TestGetExercisesForCondition:
    """Tests for condition-based search."""

    def test_get_exercises_for_condition(self) -> None:
        """Test finding exercises for a condition."""
        result = get_exercises_for_condition("neck_pain")
        # Should return search results
        assert "Found" in result or "No exercises found" in result
