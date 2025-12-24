# Code Style & Conventions

## Type Hints
- **Mandatory**: All function signatures must have complete type hints (enforced by mypy)
- Use `from __future__ import annotations` for forward references
- Modern syntax: `list[str]` instead of `List[str]`, `dict[str, int]` instead of `Dict[str, int]`
- Optional types: `str | None` instead of `Optional[str]`

## Ruff Configuration
- Line length: 100 characters
- Target: Python 3.10+
- Enabled rules: pycodestyle (E/W), Pyflakes (F), isort (I), flake8-bugbear (B), comprehensions (C4), pyupgrade (UP)

## Pydantic Best Practices
- Use `Field()` for validation constraints and descriptions
- Enum subclasses for constrained string choices (e.g., `BodyRegion`, `Difficulty`)
- `default_factory` for mutable defaults (lists, dicts)
- Model-level `Config.use_enum_values = True` for JSON/YAML serialization

## Testing
- Test files follow `test_*.py` naming convention
- Use fixtures defined in `tests/conftest.py`
- Meaningful test names that describe behavior
- Test validation errors with `pytest.raises(ValidationError)`

## Important Constraints
- **PyTorch**: Default is CPU-only to avoid triton dependency on macOS/Windows
- **Image Generation**: GPU recommended with 8GB+ VRAM; CPU auto-detects and uses SD 1.5
- **Anatomical Prompting**: Use proper terminology (muscles, joints), specify views and positions
