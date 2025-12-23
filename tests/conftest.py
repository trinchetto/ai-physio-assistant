"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def sample_exercise_data() -> dict:
    """Provide sample exercise data for testing."""
    return {
        "id": "ex-001",
        "owner_id": "physio-123",
        "name": "Shoulder External Rotation",
        "description": "Strengthens the rotator cuff muscles through external rotation movement.",
        "instructions": [
            "Stand with your elbow at 90 degrees, arm at your side",
            "Hold a resistance band attached to a fixed point",
            "Rotate your forearm outward while keeping your elbow fixed",
            "Return slowly to the starting position",
        ],
        "body_regions": ["shoulder"],
        "difficulty": "beginner",
    }
