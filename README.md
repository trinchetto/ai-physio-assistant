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
├── src/
│   ├── models/              # Pydantic data models (Exercise, Routine)
│   └── image_generation/    # SDXL image generation service
│       ├── config.py        # Generation settings and presets
│       ├── prompts.py       # Medical-style prompt templates
│       └── service.py       # Image generation service
├── scripts/
│   └── generate_images.py   # CLI for batch image generation
├── content/
│   ├── exercises/           # Exercise definitions (YAML)
│   │   ├── neck/
│   │   ├── shoulder/
│   │   ├── lower_back/
│   │   ├── hip/
│   │   └── ankle_foot/
│   ├── images/              # Generated exercise images
│   │   └── exercises/
│   ├── CONTENT_GUIDELINES.md
│   └── IMAGE_GENERATION_GUIDE.md
├── docs/
│   ├── ARCHITECTURE.md      # System architecture
│   └── CONTENT_WORKFLOW.md  # Content creation process
├── requirements.txt         # Core dependencies
├── requirements-image-gen.txt  # SDXL dependencies
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
- For image generation: NVIDIA GPU (8GB+ VRAM) or Apple Silicon Mac

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-physio-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install core dependencies
pip install -r requirements.txt

# (Optional) Install image generation dependencies
pip install torch torchvision  # Choose appropriate version for your hardware
pip install -r requirements-image-gen.txt
```

### Generating Exercise Images

```bash
# List available exercises
python scripts/generate_images.py --list

# Generate images for a specific exercise
python scripts/generate_images.py --exercise chin_tuck

# Generate all seed exercises
python scripts/generate_images.py --all

# Preview prompts without generating
python scripts/generate_images.py --all --dry-run
```

See [content/IMAGE_GENERATION_GUIDE.md](content/IMAGE_GENERATION_GUIDE.md) for detailed options.

### Contributing Exercises

1. Copy `content/exercises/_template.yaml`
2. Fill in the exercise details following `content/CONTENT_GUIDELINES.md`
3. Save in the appropriate body region folder
4. Add image generation prompts in `src/image_generation/prompts.py`
5. Generate images with `python scripts/generate_images.py --exercise <id>`

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full system design.

Key technologies:
- **Agent Framework**: Google ADK (Agent Development Kit)
- **Image Generation**: Stable Diffusion XL (local)
- **Frontend**: Streamlit
- **Database**: Firestore
- **Search**: Vertex AI Vector Search
- **Deployment**: Cloud Run

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and data models
- [Content Guidelines](content/CONTENT_GUIDELINES.md) - How to write exercises
- [Content Workflow](docs/CONTENT_WORKFLOW.md) - Process for creating content
- [Image Generation Guide](content/IMAGE_GENERATION_GUIDE.md) - SDXL image generation

## License

See [LICENSE](LICENSE) for details.
