"""Tests for package version and basic imports."""

import ai_physio_assistant


def test_version_is_defined() -> None:
    """Test that package version is defined."""
    assert hasattr(ai_physio_assistant, "__version__")
    assert isinstance(ai_physio_assistant.__version__, str)


def test_version_format() -> None:
    """Test that version follows semantic versioning pattern."""
    version = ai_physio_assistant.__version__
    parts = version.split(".")
    assert len(parts) >= 2, "Version should have at least major.minor"
    assert all(part.isdigit() for part in parts[:2]), "Major and minor should be numeric"
