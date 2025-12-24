"""Tests for the Exercise model."""

import pytest
from pydantic import ValidationError

from ai_physio_assistant.models.exercise import (
    BodyRegion,
    Difficulty,
    Exercise,
    ImageRef,
)


def test_exercise_creation_with_minimal_data(sample_exercise_data: dict) -> None:
    """Test that an exercise can be created with minimal required fields."""
    exercise = Exercise(**sample_exercise_data)

    assert exercise.id == "ex-001"
    assert exercise.owner_id == "physio-123"
    assert exercise.name == "Shoulder External Rotation"
    assert len(exercise.instructions) == 4
    assert BodyRegion.SHOULDER in exercise.body_regions


def test_exercise_default_values(sample_exercise_data: dict) -> None:
    """Test that exercise defaults are correctly applied."""
    exercise = Exercise(**sample_exercise_data)

    assert exercise.difficulty == Difficulty.BEGINNER
    assert exercise.default_sets == 3
    assert exercise.default_reps == "10-12"
    assert exercise.default_rest == "30 seconds"
    assert exercise.primary_language == "en"
    assert exercise.translations == {}
    assert exercise.images == []


def test_exercise_name_validation() -> None:
    """Test that exercise name validation works."""
    data = {
        "id": "ex-002",
        "owner_id": "physio-123",
        "name": "AB",  # Too short (min_length=3)
        "description": "Test description",
        "instructions": ["Step 1", "Step 2"],
        "body_regions": ["shoulder"],
    }

    with pytest.raises(ValidationError) as exc_info:
        Exercise(**data)

    assert "name" in str(exc_info.value)


def test_exercise_requires_minimum_instructions() -> None:
    """Test that exercise requires at least 2 instructions."""
    data = {
        "id": "ex-003",
        "owner_id": "physio-123",
        "name": "Test Exercise",
        "description": "Test description",
        "instructions": ["Only one step"],  # min_length=2
        "body_regions": ["shoulder"],
    }

    with pytest.raises(ValidationError) as exc_info:
        Exercise(**data)

    assert "instructions" in str(exc_info.value)


def test_image_ref_creation() -> None:
    """Test that ImageRef can be created properly."""
    image = ImageRef(
        url="https://storage.example.com/image.png",
        alt_text="Person performing shoulder rotation exercise",
        order=1,
    )

    assert image.url == "https://storage.example.com/image.png"
    assert image.order == 1
    assert image.caption is None


def test_body_region_enum_values() -> None:
    """Test that all expected body regions are defined."""
    expected_regions = {
        "neck",
        "shoulder",
        "upper_back",
        "lower_back",
        "chest",
        "core",
        "hip",
        "knee",
        "ankle_foot",
        "wrist_hand",
        "elbow",
        "full_body",
    }

    actual_regions = {region.value for region in BodyRegion}
    assert actual_regions == expected_regions
