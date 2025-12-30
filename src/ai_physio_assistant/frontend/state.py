"""
Session state management for the Streamlit frontend.

This module provides type-safe session state management with default values
and helper functions for common state operations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import streamlit as st

if TYPE_CHECKING:
    from langgraph.graph.state import CompiledStateGraph

    from ai_physio_assistant.models.routine import Routine


@dataclass
class ChatMessage:
    """A message in the chat history."""

    role: str  # "user" or "assistant"
    content: str


@dataclass
class ExerciseFilters:
    """Current filter state for the exercise browser."""

    body_regions: list[str] = field(default_factory=list)
    difficulty: str | None = None
    search_query: str = ""


@dataclass
class ChatState:
    """Chat panel state."""

    messages: list[ChatMessage] = field(default_factory=list)
    agent: CompiledStateGraph | None = None
    model_name: str = "gemini-2.0-flash"
    is_processing: bool = False


@dataclass
class ExerciseBrowserState:
    """Exercise browser state."""

    selected_exercise_id: str | None = None
    filters: ExerciseFilters = field(default_factory=ExerciseFilters)
    view_mode: str = "grid"  # "grid" or "list"


@dataclass
class RoutineEditorState:
    """Routine editor state."""

    current_routine: Routine | None = None
    is_modified: bool = False
    # Form fields for creating new routine
    patient_name: str = ""
    diagnosis: str = ""
    therapeutic_goals: list[str] = field(default_factory=list)
    exercise_ids: list[str] = field(default_factory=list)


def initialize_session_state() -> None:
    """Initialize all session state with defaults."""
    if "chat" not in st.session_state:
        st.session_state.chat = ChatState()

    if "exercises" not in st.session_state:
        st.session_state.exercises = ExerciseBrowserState()

    if "routines" not in st.session_state:
        st.session_state.routines = RoutineEditorState()

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Chat with AI"


def get_chat_history_for_agent() -> list[dict[str, Any]]:
    """Convert chat messages to the format expected by the agent."""
    chat_state: ChatState = st.session_state.chat
    return [{"role": msg.role, "content": msg.content} for msg in chat_state.messages]


def add_chat_message(role: str, content: str) -> None:
    """Add a message to the chat history."""
    chat_state: ChatState = st.session_state.chat
    chat_state.messages.append(ChatMessage(role=role, content=content))


def clear_chat_history() -> None:
    """Clear all chat messages."""
    chat_state: ChatState = st.session_state.chat
    chat_state.messages = []
    chat_state.agent = None  # Force agent recreation


def add_exercise_to_routine(exercise_id: str) -> None:
    """Add an exercise to the current routine being edited."""
    routine_state: RoutineEditorState = st.session_state.routines
    if exercise_id not in routine_state.exercise_ids:
        routine_state.exercise_ids.append(exercise_id)
        routine_state.is_modified = True


def remove_exercise_from_routine(exercise_id: str) -> None:
    """Remove an exercise from the current routine."""
    routine_state: RoutineEditorState = st.session_state.routines
    if exercise_id in routine_state.exercise_ids:
        routine_state.exercise_ids.remove(exercise_id)
        routine_state.is_modified = True


def clear_routine_editor() -> None:
    """Clear the routine editor state."""
    st.session_state.routines = RoutineEditorState()
