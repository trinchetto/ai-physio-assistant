# AI Physio Assistant

An AI-powered assistant that helps physiotherapists and osteopaths create personalized exercise routines for their patients.

## Features

- **AI-Assisted Routine Creation**: Describe the diagnosis and therapeutic goals, and the AI suggests appropriate exercises
- **Exercise Database**: Curated library of exercises with detailed instructions, common mistakes, and images
- **Routine Editor**: Review, customize, and reorder exercises before delivery
- **Multi-Language Support**: Create patient materials in English, Italian, and more
- **Web-First Delivery**: Shareable links that work on any device (WhatsApp-friendly)
- **PDF Export**: Generate professional handouts for printing
- **Integrated Image Generation**: SDXL-based anatomical illustrations with medical-style prompts

## Project Status

**Current Phase**: Content Development & Image Generation

We're building the foundational exercise database and generating anatomically accurate illustrations using Stable Diffusion XL.

## Project Structure

```
ai-physio-assistant/
├── src/ai_physio_assistant/     # Main Python package
│   ├── models/                  # Pydantic data models (Exercise, Routine)
│   ├── image_generation/        # SDXL image generation service
│   │   ├── config.py            # Generation settings and presets
│   │   ├── prompts.py           # Medical-style prompt templates
│   │   └── service.py           # Image generation service
│   └── cli/                     # Command-line tools
│       └── generate_images.py   # Image generation CLI
├── scripts/                     # Development convenience scripts
├── content/
│   ├── exercises/               # Exercise definitions (YAML)
│   │   ├── neck/
│   │   ├── shoulder/
│   │   ├── lower_back/
│   │   ├── hip/
│   │   └── ankle_foot/
│   ├── images/                  # Generated exercise images
│   ├── CONTENT_GUIDELINES.md
│   └── IMAGE_GENERATION_GUIDE.md
├── docs/
│   ├── ARCHITECTURE.md          # System architecture
│   └── CONTENT_WORKFLOW.md      # Content creation process
├── pyproject.toml               # Package configuration and dependencies
└── README.md
```

## Seed Exercises

| Body Region | Exercise | Status |
|-------------|----------|--------|
| Neck | Chin Tuck | Content ready, images pending |
| Shoulder | Pendulum Exercise | Content ready, images pending |
| Lower Back | Cat-Cow Stretch | Content ready, images pending |
| Hip | Piriformis Stretch (Supine) | Content ready, images pending |
| Ankle/Foot | Calf Raises | Content ready, images pending |

## Getting Started

### Prerequisites

- Python 3.10+
- For image generation:
  - **Recommended**: NVIDIA GPU (8GB+ VRAM) or Apple Silicon Mac
  - **CPU fallback**: Available for development/testing (much slower, lower quality)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-physio-assistant

# Install dependencies with Poetry
poetry install

# For development (includes testing and linting tools)
poetry install --with dev
```

That's it! Poetry will automatically install all dependencies including PyTorch.

**Note**: If you need a specific PyTorch version for your hardware (CUDA, ROCm, etc.), you can install it separately after the Poetry installation. The default installation includes the CPU version of PyTorch, which will automatically use the SD 1.5 fallback for faster generation.

### Generating Exercise Images

After installation, you can use the CLI:

```bash
# Using Poetry
poetry run physio-generate-images --list
poetry run physio-generate-images --exercise chin_tuck
poetry run physio-generate-images --all

# Or activate the virtual environment first
poetry shell
physio-generate-images --list
```

#### CLI Options

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

# Use CPU preset (faster on CPU, automatically uses SD 1.5)
poetry run physio-generate-images --all --preset cpu

# Or manually specify device (automatically switches to SD 1.5 on CPU)
poetry run physio-generate-images --exercise chin_tuck --device cpu
poetry run physio-generate-images --exercise chin_tuck --device mps  # For Apple Silicon
poetry run physio-generate-images --exercise chin_tuck --device cuda # For NVIDIA GPUs
```

**Note**: When using CPU, the system automatically switches to Stable Diffusion 1.5 (instead of SDXL) for ~4x faster generation. Images will be 512x512 instead of 1024x1024, with fewer inference steps. This is perfect for development and testing!

See [content/IMAGE_GENERATION_GUIDE.md](content/IMAGE_GENERATION_GUIDE.md) for detailed options.

### Contributing Exercises

1. Copy `content/exercises/_template.yaml`
2. Fill in the exercise details following `content/CONTENT_GUIDELINES.md`
3. Save in the appropriate body region folder
4. Add image generation prompts in `src/ai_physio_assistant/image_generation/prompts.py`
5. Generate images with `physio-generate-images --exercise <id>`

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full system design.

Key technologies:
- **Agent Framework**: Google ADK (Agent Development Kit)
- **Image Generation**: Stable Diffusion XL (local)
- **Frontend**: Streamlit
- **Database**: Firestore
- **Search**: Vertex AI Vector Search
- **Deployment**: Cloud Run

## Development

```bash
# Install with development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Run linter
poetry run ruff check src/

# Run formatter
poetry run ruff format src/

# Run type checker
poetry run mypy src/

# Run pre-commit hooks
poetry run pre-commit run --all-files
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and data models
- [Content Guidelines](content/CONTENT_GUIDELINES.md) - How to write exercises
- [Content Workflow](docs/CONTENT_WORKFLOW.md) - Process for creating content
- [Image Generation Guide](content/IMAGE_GENERATION_GUIDE.md) - SDXL image generation

## License

See [LICENSE](LICENSE) for details.
