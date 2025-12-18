# AI Physio Assistant

An AI-powered assistant that helps physiotherapists and osteopaths create personalized exercise routines for their patients.

## Features

- **AI-Assisted Routine Creation**: Describe the diagnosis and therapeutic goals, and the AI suggests appropriate exercises
- **Exercise Database**: Curated library of exercises with detailed instructions, common mistakes, and images
- **Routine Editor**: Review, customize, and reorder exercises before delivery
- **Multi-Language Support**: Create patient materials in English, Italian, and more
- **Web-First Delivery**: Shareable links that work on any device (WhatsApp-friendly)
- **PDF Export**: Generate professional handouts for printing

## Project Status

**Phase**: Content Development

We're currently building the foundational exercise database. The technical infrastructure will be built around this content.

## Project Structure

```
ai-physio-assistant/
├── src/
│   └── models/           # Data models (Exercise, Routine)
├── content/
│   ├── exercises/        # Exercise definitions (YAML)
│   │   ├── neck/
│   │   ├── shoulder/
│   │   ├── lower_back/
│   │   ├── hip/
│   │   └── ankle_foot/
│   └── CONTENT_GUIDELINES.md
├── docs/
│   ├── ARCHITECTURE.md   # System architecture
│   └── CONTENT_WORKFLOW.md
└── README.md
```

## Seed Exercises (Current)

| Body Region | Exercise | Status |
|-------------|----------|--------|
| Neck | Chin Tuck | Draft |
| Shoulder | Pendulum Exercise | Draft |
| Lower Back | Cat-Cow Stretch | Draft |
| Hip | Piriformis Stretch (Supine) | Draft |
| Ankle/Foot | Calf Raises | Draft |

## Getting Started

### Prerequisites

- Python 3.10+
- (Future: Google Cloud account for deployment)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-physio-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

### Contributing Exercises

1. Copy `content/exercises/_template.yaml`
2. Fill in the exercise details following `content/CONTENT_GUIDELINES.md`
3. Save in the appropriate body region folder
4. Submit for review

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full system design.

Key technologies:
- **Agent Framework**: Google ADK (Agent Development Kit)
- **Frontend**: Streamlit
- **Database**: Firestore
- **Search**: Vertex AI Vector Search
- **Deployment**: Cloud Run

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and data models
- [Content Guidelines](content/CONTENT_GUIDELINES.md) - How to write exercises
- [Content Workflow](docs/CONTENT_WORKFLOW.md) - Process for creating content

## License

See [LICENSE](LICENSE) for details.
