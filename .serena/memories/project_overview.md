# AI Physio Assistant - Project Overview

## Purpose
Healthcare application that helps physiotherapists create personalized exercise routines for patients. The system combines AI assistance with professional oversight, using Stable Diffusion XL for generating anatomical exercise illustrations.

**Current Phase**: Content Development & Image Generation - building the foundational exercise database with SDXL-generated illustrations.

## Tech Stack
- **Agent Framework**: Google ADK - AI orchestration and tool calling
- **Image Generation**: Stable Diffusion XL (with SD 1.5 CPU fallback)
- **Frontend**: Streamlit - Physiotherapist interface
- **Database**: Firestore - Exercise and routine storage
- **File Storage**: Cloud Storage - Images and generated PDFs
- **Search**: Vertex AI Vector Search - Semantic exercise search
- **PDF Generation**: WeasyPrint - Patient handouts
- **Deployment**: Cloud Run - Serverless hosting
- **Package Manager**: Poetry

## Core Data Models
- **Exercise** (models/exercise.py): Reusable unit with instructions, images, metadata, body region, difficulty, translations
- **Routine** (models/routine.py): Patient-specific collection of exercises with customized parameters

## Image Generation System
- **Key Feature**: CPU fallback automatically switches from SDXL to SD 1.5 for 4x faster generation
- **Medical Prompting**: Uses anatomical terminology for better results
- **Reproducibility**: Fixed seeds for consistent generation
- **Memory Optimization**: Supports low_vram and cpu presets

## Content Structure
Exercise definitions stored as YAML in `content/exercises/`, organized by body region (neck, shoulder, lower_back, etc.)
