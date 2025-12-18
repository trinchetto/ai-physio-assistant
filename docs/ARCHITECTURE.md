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

See `src/models/exercise.py` for the full schema.

### Routine

A routine is a patient-specific collection of exercises with customized parameters.

Key attributes:
- **Patient**: Name, preferred language, optional ID reference
- **Clinical**: Diagnosis, therapeutic goals, precautions
- **Content**: Title, ordered list of exercises with per-patient customizations
- **Schedule**: Frequency, duration, estimated session time
- **Guidance**: General notes, warning signs
- **Delivery**: Status, shareable URL, PDF URL

See `src/models/routine.py` for the full schema.

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
4. **Add images**: Upload or generate illustrations
5. **Save to library**: Exercise available for future routines

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Agent Framework | Google ADK | AI orchestration and tool calling |
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

## Content Guidelines

See `content/CONTENT_GUIDELINES.md` for detailed exercise authoring guidelines.

## Project Structure

```
ai-physio-assistant/
├── src/
│   ├── models/           # Pydantic data models
│   ├── agent/            # ADK agent and tools
│   ├── services/         # Business logic
│   └── api/              # API endpoints
├── content/
│   ├── exercises/        # Seed exercise YAML files
│   │   ├── neck/
│   │   ├── shoulder/
│   │   └── ...
│   ├── images/           # Exercise images
│   └── CONTENT_GUIDELINES.md
├── frontend/             # Streamlit app
├── infrastructure/       # Terraform configs
├── tests/
└── docs/
```
