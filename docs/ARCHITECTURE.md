# AI Physio Assistant - Architecture

## Overview

The AI Physio Assistant helps physiotherapists and osteopaths create personalized exercise routines for patients. The system uses AI to suggest exercises based on diagnosis and therapeutic goals, while keeping the medical professional in control of the final prescription.

## Core Principles

1. **Physio in control**: AI assists but doesn't prescribe. The physiotherapist reviews and approves all routines.
2. **Content quality**: Exercises have clear instructions, common mistakes, and visual aids.
3. **Multi-language**: Content is translatable for international patient populations.
4. **Web-first delivery**: Shareable links that work on any device, with PDF as a secondary option.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI PHYSIO ASSISTANT                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         FRONTEND (Streamlit)                         │    │
│  │  ┌─────────────┐  ┌─────────────────┐  ┌──────────────────────────┐ │    │
│  │  │ Chat Panel  │  │ Routine Editor  │  │   Exercise Manager       │ │    │
│  │  │ (AI conv.)  │  │ (drag/drop,     │  │   (add/edit exercises)   │ │    │
│  │  │             │  │  adjust params) │  │                          │ │    │
│  │  └─────────────┘  └─────────────────┘  └──────────────────────────┘ │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         AGENT LAYER (ADK)                            │    │
│  │                                                                      │    │
│  │   Tools: search_exercises | compose_routine | translate | generate  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                          │                    │                              │
│            ┌─────────────┴──────┐    ┌───────┴────────┐                     │
│            ▼                    ▼    ▼                ▼                     │
│  ┌──────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐    │
│  │  EXERCISE DB     │  │  VECTOR SEARCH  │  │   OUTPUT GENERATION     │    │
│  │                  │  │                 │  │                         │    │
│  │  Firestore:      │  │  Vertex AI      │  │  - PDF (WeasyPrint)     │    │
│  │  - physio_id/    │  │  Embeddings     │  │  - Web link (shareable) │    │
│  │    exercises/    │  │                 │  │  - WhatsApp ready       │    │
│  │  - shared/       │  │                 │  │                         │    │
│  │    exercises/    │  │                 │  │                         │    │
│  │                  │  │                 │  │                         │    │
│  │  Cloud Storage:  │  │                 │  │                         │    │
│  │  - images/       │  │                 │  │                         │    │
│  └──────────────────┘  └─────────────────┘  └─────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    IMAGE GENERATION (SDXL)                           │    │
│  │                                                                      │    │
│  │   Local Stable Diffusion XL with medical/anatomical prompts          │    │
│  │   - Anatomical terminology (lateral view, supine, muscle groups)     │    │
│  │   - Consistent style via fixed seeds and style prefixes              │    │
│  │   - Optional LoRA support for medical illustration fine-tuning       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Models

### Exercise

An exercise is a reusable unit of content that can be included in multiple routines.

Key attributes:
- **Identity**: Unique ID, owner (physio or shared)
- **Content**: Name, description, step-by-step instructions, common mistakes
- **Categorization**: Body regions, conditions, therapeutic goals, contraindications
- **Parameters**: Default sets, reps, hold duration, rest time
- **Media**: 2-3 images showing positions, optional video
- **Translations**: Cached translations for supported languages

See `src/ai_physio_assistant/models/exercise.py` for the full schema.

### Routine

A routine is a patient-specific collection of exercises with customized parameters.

Key attributes:
- **Patient**: Name, preferred language, optional ID reference
- **Clinical**: Diagnosis, therapeutic goals, precautions
- **Content**: Title, ordered list of exercises with per-patient customizations
- **Schedule**: Frequency, duration, estimated session time
- **Guidance**: General notes, warning signs
- **Delivery**: Status, shareable URL, PDF URL

See `src/ai_physio_assistant/models/routine.py` for the full schema.

## Image Generation

Exercise illustrations are generated using Stable Diffusion XL with medical-style prompting.

### Components

| File | Purpose |
|------|---------|
| `src/ai_physio_assistant/image_generation/config.py` | SDXL settings, presets (fast, quality, low_vram) |
| `src/ai_physio_assistant/image_generation/prompts.py` | Medical prompt templates with anatomical terminology |
| `src/ai_physio_assistant/image_generation/service.py` | Generation service with batch processing |
| `physio-generate-images` (CLI) | Command-line tool for generating exercise images |

### Prompt Strategy

Prompts use proper anatomical terminology for better results:

- **View angles**: lateral, anterior, posterior, oblique, close-up
- **Body positions**: standing, seated, supine, prone, quadruped
- **Muscle references**: piriformis, gastrocnemius, erector spinae, etc.
- **Joint references**: glenohumeral, cervical spine, hip flexion, etc.

Example generated prompt:
```
anatomical diagram, physiotherapy illustration, medical reference style,
clean simple lines, professional medical textbook illustration,
gender-neutral human figure, accurate anatomical proportions,
lateral view, quadruped position on hands and knees,
spinal flexion cat pose thoracic lumbar kyphosis,
showing erector spinae muscles,
clean white background, no text, no labels, no watermarks
```

See `content/IMAGE_GENERATION_GUIDE.md` for full documentation.

## Workflow

### Creating a Routine

1. **Physio starts conversation**: Describes diagnosis and goals
2. **AI searches exercises**: Finds relevant exercises from the database
3. **AI composes draft**: Suggests a routine with appropriate exercises
4. **Physio reviews in editor**: Adjusts exercises, parameters, order, notes
5. **Generate output**: Creates shareable web link and/or PDF
6. **Deliver to patient**: Share via WhatsApp, email, or print

### Adding Exercises

1. **Physio initiates**: Provides exercise concept or name
2. **AI assists drafting**: Creates structured content following guidelines
3. **Physio reviews**: Edits for accuracy and completeness
4. **Generate images**: Run SDXL with anatomical prompts
5. **Save to library**: Exercise available for future routines

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Agent Framework | Google ADK | AI orchestration and tool calling |
| Image Generation | Stable Diffusion XL | Anatomical exercise illustrations |
| Frontend | Streamlit | Physio interface |
| Database | Firestore | Exercise and routine storage |
| File Storage | Cloud Storage | Images and generated PDFs |
| Search | Vertex AI Vector Search | Semantic exercise search |
| PDF Generation | WeasyPrint | Patient handouts |
| Deployment | Cloud Run | Serverless hosting |
| Infrastructure | Terraform | Infrastructure as code |

## Multi-Tenancy

### Current Phase: Separate Libraries

- Each physio has their own exercise collection
- Exercises stored under `physios/{physio_id}/exercises/`
- Routines stored under `physios/{physio_id}/routines/`

### Future: Shared Library

- Community exercises in `shared/exercises/`
- Physios can copy shared exercises to their library
- Optional: Physios can contribute exercises back to shared library

## Multi-Language Support

### Strategy: Translate on Demand

1. Exercises stored in physio's primary language
2. When generating routine for different language:
   - Check if translation exists in cache
   - If not, translate using AI and cache
   - Physio can review/edit translations
3. Patient materials generated in patient's preferred language

### Supported Languages (Initial)

- English (en)
- Italian (it)

## Project Structure

```
ai-physio-assistant/
├── src/ai_physio_assistant/     # Main Python package
│   ├── models/                  # Pydantic data models
│   ├── image_generation/        # SDXL image generation service
│   │   ├── config.py            # Generation settings and presets
│   │   ├── prompts.py           # Medical-style prompt templates
│   │   └── service.py           # Image generation service
│   ├── cli/                     # Command-line tools
│   │   └── generate_images.py   # Image generation CLI
│   ├── agent/                   # ADK agent and tools (future)
│   ├── services/                # Business logic (future)
│   └── api/                     # API endpoints (future)
├── scripts/                     # Development convenience scripts
├── content/
│   ├── exercises/               # Seed exercise YAML files
│   │   ├── neck/
│   │   ├── shoulder/
│   │   └── ...
│   ├── images/                  # Generated exercise images
│   │   └── exercises/
│   ├── CONTENT_GUIDELINES.md
│   └── IMAGE_GENERATION_GUIDE.md
├── docs/
│   ├── ARCHITECTURE.md
│   └── CONTENT_WORKFLOW.md
├── frontend/                    # Streamlit app (future)
├── infrastructure/              # Terraform configs (future)
├── tests/                       # Test suite (future)
└── pyproject.toml               # Package configuration and dependencies
```
