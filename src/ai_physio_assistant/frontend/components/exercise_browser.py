"""
Exercise browser component for viewing and searching exercises.
"""

from __future__ import annotations

import streamlit as st

from ai_physio_assistant.frontend.services.exercise_service import get_exercise_service
from ai_physio_assistant.frontend.state import (
    ExerciseBrowserState,
    add_exercise_to_routine,
)


def render_exercise_browser() -> None:
    """Render the exercise browser page."""
    st.header("Exercise Library")

    exercise_service = get_exercise_service()
    state: ExerciseBrowserState = st.session_state.exercises

    # Sidebar filters
    with st.sidebar:
        st.subheader("Filters")

        # Search box
        search_query = st.text_input(
            "Search",
            value=state.filters.search_query,
            placeholder="Search exercises...",
            key="exercise_search",
        )
        state.filters.search_query = search_query

        # Body region filter
        body_regions = st.multiselect(
            "Body Regions",
            options=exercise_service.get_body_regions(),
            default=state.filters.body_regions,
            key="body_region_filter",
        )
        state.filters.body_regions = body_regions

        # Difficulty filter
        difficulty = st.selectbox(
            "Difficulty",
            options=["All"] + exercise_service.get_difficulty_levels(),
            index=0 if not state.filters.difficulty else None,
            key="difficulty_filter",
        )
        state.filters.difficulty = None if difficulty == "All" else difficulty

        # View mode toggle
        view_mode = st.radio(
            "View Mode",
            options=["Grid", "List"],
            index=0 if state.view_mode == "grid" else 1,
            horizontal=True,
            key="view_mode",
        )
        state.view_mode = view_mode.lower()

        if st.button("Clear Filters", use_container_width=True):
            state.filters.search_query = ""
            state.filters.body_regions = []
            state.filters.difficulty = None
            st.rerun()

    # Get filtered exercises
    exercises = exercise_service.search(
        query=state.filters.search_query,
        body_regions=state.filters.body_regions if state.filters.body_regions else None,
        difficulty=state.filters.difficulty,
    )

    # Display count
    st.caption(f"Showing {len(exercises)} of {exercise_service.count()} exercises")

    # Check if an exercise is selected for detail view
    if state.selected_exercise_id:
        _render_exercise_detail(state.selected_exercise_id)
        return

    # Render exercises
    if not exercises:
        st.info("No exercises match your filters. Try adjusting your search criteria.")
        return

    if state.view_mode == "grid":
        _render_grid_view(exercises)
    else:
        _render_list_view(exercises)


def _render_grid_view(exercises: list[dict]) -> None:
    """Render exercises in a grid layout."""
    # 3 columns per row
    cols_per_row = 3

    for i in range(0, len(exercises), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(exercises):
                ex = exercises[i + j]
                with col:
                    _render_exercise_card(ex)


def _render_list_view(exercises: list[dict]) -> None:
    """Render exercises in a list layout."""
    for ex in exercises:
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(ex["name"])
                st.caption(
                    f"**{', '.join(ex.get('body_regions', []))}** | "
                    f"{ex.get('difficulty', 'N/A')}"
                )
                description = ex.get("description", "")[:200]
                if len(ex.get("description", "")) > 200:
                    description += "..."
                st.write(description)

            with col2:
                if st.button("View", key=f"view_{ex['id']}", use_container_width=True):
                    st.session_state.exercises.selected_exercise_id = ex["id"]
                    st.rerun()

                if st.button(
                    "Add to Routine",
                    key=f"add_{ex['id']}",
                    use_container_width=True,
                    type="secondary",
                ):
                    add_exercise_to_routine(ex["id"])
                    st.toast(f"Added {ex['name']} to routine")

            st.divider()


def _render_exercise_card(exercise: dict) -> None:
    """Render a single exercise card for grid view."""
    with st.container(border=True):
        st.subheader(exercise["name"])

        # Body regions and difficulty badges
        regions = ", ".join(exercise.get("body_regions", []))
        difficulty = exercise.get("difficulty", "N/A")
        st.caption(f"{regions} | {difficulty}")

        # Truncated description
        description = exercise.get("description", "")[:100]
        if len(exercise.get("description", "")) > 100:
            description += "..."
        st.write(description)

        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View", key=f"card_view_{exercise['id']}", use_container_width=True):
                st.session_state.exercises.selected_exercise_id = exercise["id"]
                st.rerun()
        with col2:
            if st.button("+", key=f"card_add_{exercise['id']}", use_container_width=True):
                add_exercise_to_routine(exercise["id"])
                st.toast(f"Added {exercise['name']}")


def _render_exercise_detail(exercise_id: str) -> None:
    """Render the full detail view for an exercise."""
    exercise_service = get_exercise_service()
    exercise = exercise_service.get_by_id(exercise_id)

    if not exercise:
        st.error(f"Exercise '{exercise_id}' not found.")
        if st.button("Back to List"):
            st.session_state.exercises.selected_exercise_id = None
            st.rerun()
        return

    # Back button
    if st.button("← Back to Exercise List"):
        st.session_state.exercises.selected_exercise_id = None
        st.rerun()

    st.divider()

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(exercise["name"])
    with col2:
        if st.button("Add to Routine", type="primary", use_container_width=True):
            add_exercise_to_routine(exercise_id)
            st.toast(f"Added {exercise['name']} to routine")

    # Metadata badges
    regions = ", ".join(exercise.get("body_regions", []))
    difficulty = exercise.get("difficulty", "N/A")
    equipment = ", ".join(exercise.get("equipment", ["none"]))

    st.markdown(
        f"**Body Regions:** {regions} | **Difficulty:** {difficulty} | **Equipment:** {equipment}"
    )

    st.divider()

    # Description
    st.subheader("Description")
    st.write(exercise.get("description", "No description available."))

    # Instructions
    st.subheader("Instructions")
    for i, instruction in enumerate(exercise.get("instructions", []), 1):
        st.markdown(f"{i}. {instruction}")

    # Common Mistakes
    if exercise.get("common_mistakes"):
        st.subheader("Common Mistakes to Avoid")
        for mistake in exercise.get("common_mistakes", []):
            st.markdown(f"- {mistake}")

    # Parameters
    st.subheader("Default Parameters")
    param_cols = st.columns(4)
    with param_cols[0]:
        st.metric("Sets", exercise.get("default_sets", 3))
    with param_cols[1]:
        st.metric("Reps", exercise.get("default_reps", "10-12"))
    with param_cols[2]:
        st.metric("Hold", exercise.get("default_hold", "N/A"))
    with param_cols[3]:
        st.metric("Rest", exercise.get("default_rest", "30s"))

    # Conditions
    if exercise.get("conditions"):
        st.subheader("Conditions This Helps")
        st.write(", ".join(exercise.get("conditions", [])))

    # Contraindications
    if exercise.get("contraindications"):
        st.subheader("Contraindications")
        st.warning("Do NOT use if patient has:")
        for contra in exercise.get("contraindications", []):
            st.markdown(f"- {contra}")

    # Therapeutic Goals
    if exercise.get("therapeutic_goals"):
        st.subheader("Therapeutic Goals")
        st.write(", ".join(exercise.get("therapeutic_goals", [])))
