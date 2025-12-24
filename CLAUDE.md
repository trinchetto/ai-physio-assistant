# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Physio Assistant is a healthcare application that helps physiotherapists create personalized exercise routines for patients. The system combines AI assistance with professional oversight, using Stable Diffusion XL for generating anatomical exercise illustrations.

**Current Phase**: Content Development & Image Generation - building the foundational exercise database with SDXL-generated illustrations.

## Development Commands

### Installation & Setup

```bash
# Install all dependencies
poetry install

# Install with development tools (testing, linting)
poetry install --with dev

# GPU acceleration (optional, after Poetry install)
# NVIDIA GPU (CUDA 12.1):
poetry run pip install torch --index-url https://download.pytorch.org/whl/cu121
# Apple Silicon uses MPS backend - no additional installation needed
```

### Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=ai_physio_assistant --cov-report=term-missing

# Run a specific test file
poetry run pytest tests/test_exercise_model.py

# Run a specific test function
poetry run pytest tests/test_exercise_model.py::test_exercise_creation_with_minimal_data
```

### Code Quality

```bash
# Run linter (checks code quality)
poetry run ruff check src/

# Run linter with auto-fix
poetry run ruff check --fix src/

# Run formatter
poetry run ruff format src/

# Run type checker
poetry run mypy src/

# Run all pre-commit hooks (lint, format, type check)
poetry run pre-commit run --all-files
```

### Image Generation

```bash
# List available exercises
poetry run physio-generate-images --list

# Generate images for a specific exercise
poetry run physio-generate-images --exercise chin_tuck

# Generate all seed exercises
poetry run physio-generate-images --all

# Preview prompts without generating (no GPU needed)
poetry run physio-generate-images --all --dry-run

# Use quality preset (slower, better results)
poetry run physio-generate-images --all --preset quality

# Use low VRAM preset (for 8GB GPUs)
poetry run physio-generate-images --all --preset low_vram

# Use CPU preset (automatically uses SD 1.5 for 4x faster generation)
poetry run physio-generate-images --all --preset cpu

# Manually specify device
poetry run physio-generate-images --exercise chin_tuck --device cuda  # NVIDIA
poetry run physio-generate-images --exercise chin_tuck --device mps   # Apple Silicon
poetry run physio-generate-images --exercise chin_tuck --device cpu   # CPU fallback
```

## Architecture Overview

### Core Data Models

The application is built around two main Pydantic models in `src/ai_physio_assistant/models/`:

**Exercise** (`exercise.py`):
- Reusable unit of content with instructions, images, and metadata
- Strongly typed with enums: `BodyRegion`, `Difficulty`, `ExerciseSource`
- Supports multi-language translations cached in `translations` dict
- Default parameters (sets, reps, hold, rest) can be overridden in routines
- Images stored as `ImageRef` objects with URL, alt text, order, and caption

**Routine** (`routine.py`):
- Patient-specific collection of exercises with customized parameters
- Includes diagnosis, therapeutic goals, schedule, and delivery info

### Image Generation System

Located in `src/ai_physio_assistant/image_generation/`:

**Key Architecture Decisions**:
1. **CPU Fallback**: When device="cpu", automatically switches from SDXL to Stable Diffusion 1.5 for ~4x faster generation (512x512 instead of 1024x1024)
2. **Medical Prompting**: Uses anatomical terminology (lateral view, supine, erector spinae, glenohumeral joint) for better results
3. **Reproducibility**: Fixed seeds for consistent image generation across runs
4. **Memory Optimization**: Attention slicing and VAE tiling for limited VRAM scenarios

**Files**:
- `config.py`: Generation settings with presets (fast, quality, low_vram, cpu)
- `prompts.py`: Medical-style prompt templates with anatomical terminology
- `service.py`: Image generation service with batch processing
- `cli/generate_images.py`: Command-line interface

### Content Structure

Exercise definitions are stored as YAML files in `content/exercises/`, organized by body region:
- `neck/`, `shoulder/`, `lower_back/`, `hip/`, `ankle_foot/`, etc.

Each exercise YAML includes:
- Unique ID, name, description
- Step-by-step instructions (minimum 3 steps)
- Common mistakes patients make
- Body regions, conditions, therapeutic goals, contraindications
- Default parameters: sets, reps, hold duration, rest time
- Equipment requirements
- Difficulty level
- Optional translations

See `content/exercises/_template.yaml` for the complete structure.

### Multi-Tenancy Design

**Current**: Separate libraries per physiotherapist
- Exercises: `physios/{physio_id}/exercises/`
- Routines: `physios/{physio_id}/routines/`

**Future**: Shared community library
- Shared exercises: `shared/exercises/`
- Physios can copy and contribute back

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Agent Framework | Google ADK | AI orchestration and tool calling |
| Image Generation | Stable Diffusion XL | Anatomical exercise illustrations |
| Frontend | Streamlit | Physiotherapist interface |
| Database | Firestore | Exercise and routine storage |
| File Storage | Cloud Storage | Images and generated PDFs |
| Search | Vertex AI Vector Search | Semantic exercise search |
| PDF Generation | WeasyPrint | Patient handouts |
| Deployment | Cloud Run | Serverless hosting |

## Code Style & Quality Standards

### Type Hints
- **Mandatory**: All function signatures must have complete type hints (enforced by mypy)
- Use `from __future__ import annotations` for Python 3.10+ forward references
- Modern syntax: `list[str]` instead of `List[str]`, `dict[str, int]` instead of `Dict[str, int]`
- Optional types: `str | None` instead of `Optional[str]`

### Ruff Configuration
- Line length: 100 characters
- Target: Python 3.10+
- Enabled rules: pycodestyle (E/W), Pyflakes (F), isort (I), flake8-bugbear (B), comprehensions (C4), pyupgrade (UP)
- Ignores E501 (line length handled by formatter)

### Pydantic Best Practices
- Use `Field()` for validation constraints and descriptions
- Enum subclasses for constrained string choices (e.g., `BodyRegion`, `Difficulty`)
- `default_factory` for mutable defaults (lists, dicts)
- Model-level `Config.use_enum_values = True` when serializing to JSON/YAML

### Testing
- Test files follow `test_*.py` naming convention
- Use fixtures defined in `tests/conftest.py`
- Aim for meaningful test names that describe behavior
- Test validation errors with `pytest.raises(ValidationError)`

## Important Constraints & Considerations

### PyTorch Dependency Management
The project uses PyTorch CPU-only by default to avoid the `triton` dependency issue on macOS/Windows:
- Default installation via `poetry.lock` uses PyTorch CPU from the pytorch-cpu index
- For GPU support, users manually install PyTorch with CUDA/ROCm after Poetry install
- The image generation service auto-detects CPU and switches to SD 1.5 fallback

### Image Generation Performance
- **GPU recommended**: 8GB+ VRAM for SDXL (use `low_vram` preset for 8GB)
- **Apple Silicon**: Works well with MPS backend
- **CPU**: Automatically uses SD 1.5 (512x512, 15-20 steps) instead of SDXL for practical development/testing

### Exercise Content Guidelines
When creating or modifying exercises:
- Instructions must be clear, specific, and sequenced (minimum 3 steps)
- Include breathing cues and safety warnings where relevant
- Common mistakes should explain what's wrong AND why it matters
- Use standard body region and condition names (see `content/CONTENT_GUIDELINES.md`)
- Follow the YAML template structure exactly

### Anatomical Prompt Engineering
When adding prompts in `image_generation/prompts.py`:
- Use proper anatomical terminology: muscle names (piriformis, gastrocnemius), joint references (glenohumeral, cervical spine)
- Specify view angles: lateral, anterior, posterior, oblique, close-up
- Include body positions: standing, seated, supine, prone, quadruped
- Keep prompts concise to stay under CLIP's 77 token limit
- Style prefix/suffix applied automatically from config

## Documentation References

- **Architecture**: `docs/ARCHITECTURE.md` - system design and data models
- **Content Guidelines**: `content/CONTENT_GUIDELINES.md` - how to write exercises
- **Content Workflow**: `docs/CONTENT_WORKFLOW.md` - process for creating content
- **Image Generation**: `content/IMAGE_GENERATION_GUIDE.md` - SDXL image generation
- **README**: `README.md` - project overview and getting started
