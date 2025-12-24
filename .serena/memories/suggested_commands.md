# Suggested Commands

## Installation & Setup
```bash
poetry install                              # Install all dependencies
poetry install --with dev                   # Install with dev tools (testing, linting)
poetry run pip install torch --index-url https://download.pytorch.org/whl/cu121  # GPU (CUDA 12.1)
```

## Testing
```bash
poetry run pytest                           # Run all tests
poetry run pytest --cov=ai_physio_assistant --cov-report=term-missing  # With coverage
poetry run pytest tests/test_exercise_model.py  # Specific test file
```

## Code Quality
```bash
poetry run ruff check src/                  # Lint
poetry run ruff check --fix src/            # Auto-fix linting
poetry run ruff format src/                 # Format code
poetry run mypy src/                        # Type checking
poetry run pre-commit run --all-files       # All pre-commit hooks
```

## Image Generation
```bash
poetry run physio-generate-images --list    # List available exercises
poetry run physio-generate-images --exercise <name>  # Generate for one exercise
poetry run physio-generate-images --all     # Generate all exercises
poetry run physio-generate-images --all --preset cpu  # CPU preset (auto SD 1.5)
poetry run physio-generate-images --all --preset quality  # Best quality (slow)
poetry run physio-generate-images --all --preset low_vram  # 8GB GPU
poetry run physio-generate-images --all --dry-run  # Preview without generating
```

## Device Selection
```bash
poetry run physio-generate-images --exercise <name> --device cpu    # CPU fallback
poetry run physio-generate-images --exercise <name> --device cuda   # NVIDIA GPU
poetry run physio-generate-images --exercise <name> --device mps    # Apple Silicon
```
