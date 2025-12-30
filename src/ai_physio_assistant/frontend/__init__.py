"""
Streamlit frontend for the AI Physio Assistant.

This package provides a web interface for physiotherapists to:
- Chat with the AI agent for exercise recommendations
- Browse and search the exercise library
- Create and edit patient routines
"""

from ai_physio_assistant.frontend.app import main

__all__ = ["main"]
