"""
Main Streamlit application for the AI Physio Assistant.

This module provides the entry point for the Streamlit frontend,
with navigation between the Chat, Exercise Library, and Routine Editor.
"""

from __future__ import annotations

import subprocess
import sys

import streamlit as st

from ai_physio_assistant.frontend.components import (
    render_chat_panel,
    render_exercise_browser,
    render_routine_editor,
)
from ai_physio_assistant.frontend.state import initialize_session_state


def configure_page() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="AI Physio Assistant",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_navigation() -> str:
    """Render the navigation sidebar and return the selected page."""
    with st.sidebar:
        st.title("AI Physio Assistant")
        st.divider()

        # Navigation
        page = str(st.radio(
            "Navigation",
            options=["Chat with AI", "Exercise Library", "Routine Editor"],
            key="nav_radio",
            label_visibility="collapsed",
        ))

        # Update session state
        st.session_state.current_page = page

        return page


def render_main_content(page: str) -> None:
    """Render the main content based on the selected page."""
    if page == "Chat with AI":
        render_chat_panel()
    elif page == "Exercise Library":
        render_exercise_browser()
    elif page == "Routine Editor":
        render_routine_editor()


def app() -> None:
    """Main application function."""
    # Configure page (must be first Streamlit command)
    configure_page()

    # Initialize session state
    initialize_session_state()

    # Render navigation and get selected page
    page = render_navigation()

    # Render main content
    render_main_content(page)


def main() -> None:
    """
    Entry point for the physio-app CLI command.

    This function launches the Streamlit server with the app.
    """
    # Get the path to this module
    import ai_physio_assistant.frontend.app as app_module

    app_path = app_module.__file__

    # Launch Streamlit
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", app_path, "--server.headless", "true"],
        check=True,
    )


if __name__ == "__main__":
    # When run directly by Streamlit
    app()
