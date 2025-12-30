"""UI components for the Streamlit frontend."""

from ai_physio_assistant.frontend.components.chat_panel import render_chat_panel
from ai_physio_assistant.frontend.components.exercise_browser import render_exercise_browser
from ai_physio_assistant.frontend.components.routine_editor import render_routine_editor

__all__ = ["render_chat_panel", "render_exercise_browser", "render_routine_editor"]
