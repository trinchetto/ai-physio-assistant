"""
Routine editor component for creating and editing patient routines.
"""

from __future__ import annotations

from uuid import uuid4

import streamlit as st

from ai_physio_assistant.frontend.services.exercise_service import get_exercise_service
from ai_physio_assistant.frontend.state import (
    RoutineEditorState,
    clear_routine_editor,
    remove_exercise_from_routine,
)
from ai_physio_assistant.models.routine import Routine, RoutineExercise


def render_routine_editor() -> None:
    """Render the routine editor page."""
    st.header("Routine Editor")

    routine_state: RoutineEditorState = st.session_state.routines

    # Sidebar with routine list and actions
    with st.sidebar:
        st.subheader("Actions")

        if st.button("New Routine", use_container_width=True, type="primary"):
            clear_routine_editor()
            st.rerun()

        if routine_state.exercise_ids:
            st.divider()
            st.caption(f"{len(routine_state.exercise_ids)} exercise(s) in routine")

            if st.button("Clear All Exercises", use_container_width=True):
                routine_state.exercise_ids = []
                st.rerun()

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        _render_patient_info_form()
        st.divider()
        _render_exercise_list()

    with col2:
        _render_routine_preview()


def _render_patient_info_form() -> None:
    """Render the patient information form."""
    st.subheader("Patient Information")

    routine_state: RoutineEditorState = st.session_state.routines

    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input(
            "Patient Name",
            value=routine_state.patient_name,
            placeholder="Enter patient name",
            key="patient_name_input",
        )
        routine_state.patient_name = patient_name

    with col2:
        diagnosis = st.text_input(
            "Diagnosis",
            value=routine_state.diagnosis,
            placeholder="e.g., Chronic neck pain",
            key="diagnosis_input",
        )
        routine_state.diagnosis = diagnosis

    # Therapeutic goals
    st.write("**Therapeutic Goals**")
    goal_options = [
        "Reduce pain",
        "Improve mobility",
        "Strengthen muscles",
        "Improve flexibility",
        "Improve posture",
        "Prevent injury",
    ]

    selected_goals = st.multiselect(
        "Select goals",
        options=goal_options,
        default=routine_state.therapeutic_goals,
        key="goals_select",
        label_visibility="collapsed",
    )
    routine_state.therapeutic_goals = selected_goals


def _render_exercise_list() -> None:
    """Render the list of exercises in the routine."""
    st.subheader("Exercises")

    routine_state: RoutineEditorState = st.session_state.routines
    exercise_service = get_exercise_service()

    if not routine_state.exercise_ids:
        st.info(
            "No exercises added yet. "
            "Add exercises from the Exercise Library or use the AI Chat to get recommendations."
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Browse Exercise Library", use_container_width=True):
                st.session_state.current_page = "Exercise Library"
                st.rerun()
        with col2:
            if st.button("Ask AI for Suggestions", use_container_width=True):
                st.session_state.current_page = "Chat with AI"
                st.rerun()
        return

    # Get exercise details
    exercises = exercise_service.get_multiple(routine_state.exercise_ids)

    # Render each exercise with controls
    for i, ex in enumerate(exercises):
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"**{i + 1}. {ex['name']}**")
                st.caption(f"{', '.join(ex.get('body_regions', []))} | {ex.get('difficulty', 'N/A')}")

            with col2:
                # Move up/down buttons
                up_col, down_col = st.columns(2)
                with up_col:
                    if i > 0:
                        if st.button("↑", key=f"up_{ex['id']}", use_container_width=True):
                            _move_exercise(i, i - 1)
                            st.rerun()
                with down_col:
                    if i < len(exercises) - 1:
                        if st.button("↓", key=f"down_{ex['id']}", use_container_width=True):
                            _move_exercise(i, i + 1)
                            st.rerun()

            with col3:
                if st.button("Remove", key=f"remove_{ex['id']}", use_container_width=True):
                    remove_exercise_from_routine(ex["id"])
                    st.rerun()

            # Expandable parameters
            with st.expander("Parameters"):
                param_cols = st.columns(4)
                with param_cols[0]:
                    st.number_input(
                        "Sets",
                        value=ex.get("default_sets", 3),
                        min_value=1,
                        max_value=10,
                        key=f"sets_{ex['id']}",
                    )
                with param_cols[1]:
                    st.text_input(
                        "Reps",
                        value=ex.get("default_reps", "10-12"),
                        key=f"reps_{ex['id']}",
                    )
                with param_cols[2]:
                    st.text_input(
                        "Hold",
                        value=ex.get("default_hold", ""),
                        key=f"hold_{ex['id']}",
                    )
                with param_cols[3]:
                    st.text_input(
                        "Rest",
                        value=ex.get("default_rest", "30s"),
                        key=f"rest_{ex['id']}",
                    )

                st.text_area(
                    "Notes for patient",
                    placeholder="Special instructions for this patient...",
                    key=f"notes_{ex['id']}",
                )


def _move_exercise(from_index: int, to_index: int) -> None:
    """Move an exercise from one position to another."""
    routine_state: RoutineEditorState = st.session_state.routines
    exercises = routine_state.exercise_ids
    exercises[from_index], exercises[to_index] = exercises[to_index], exercises[from_index]
    routine_state.is_modified = True


def _render_routine_preview() -> None:
    """Render a preview of the routine and export options."""
    st.subheader("Preview & Export")

    routine_state: RoutineEditorState = st.session_state.routines
    exercise_service = get_exercise_service()

    # Validation
    is_valid = _validate_routine()

    if not is_valid:
        st.warning("Complete the form to enable export")
        return

    # Estimate duration
    num_exercises = len(routine_state.exercise_ids)
    est_time = num_exercises * 3  # ~3 min per exercise

    st.metric("Estimated Duration", f"{est_time}-{est_time + 5} min")
    st.metric("Exercises", num_exercises)

    st.divider()

    # Export buttons
    if st.button("Export as Markdown", use_container_width=True, type="primary"):
        markdown = _generate_markdown_export()
        st.download_button(
            "Download Markdown",
            data=markdown,
            file_name=f"routine_{routine_state.patient_name.lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # Preview section
    st.divider()
    st.subheader("Routine Summary")

    st.markdown(f"**Patient:** {routine_state.patient_name}")
    st.markdown(f"**Diagnosis:** {routine_state.diagnosis}")
    st.markdown(f"**Goals:** {', '.join(routine_state.therapeutic_goals)}")

    st.divider()

    # Exercise list preview
    exercises = exercise_service.get_multiple(routine_state.exercise_ids)
    for i, ex in enumerate(exercises, 1):
        st.markdown(f"{i}. {ex['name']}")


def _validate_routine() -> bool:
    """Validate that the routine has required information."""
    routine_state: RoutineEditorState = st.session_state.routines

    return bool(
        routine_state.patient_name
        and routine_state.diagnosis
        and routine_state.therapeutic_goals
        and routine_state.exercise_ids
    )


def _generate_markdown_export() -> str:
    """Generate a markdown export of the routine."""
    routine_state: RoutineEditorState = st.session_state.routines
    exercise_service = get_exercise_service()
    exercises = exercise_service.get_multiple(routine_state.exercise_ids)

    lines = [
        f"# Exercise Routine for {routine_state.patient_name}",
        "",
        f"**Diagnosis:** {routine_state.diagnosis}",
        f"**Goals:** {', '.join(routine_state.therapeutic_goals)}",
        f"**Frequency:** Once daily",
        "",
        "---",
        "",
        "## Exercises",
        "",
    ]

    for i, ex in enumerate(exercises, 1):
        lines.append(f"### {i}. {ex['name']}")
        lines.append("")
        lines.append(f"**Sets:** {ex.get('default_sets', 3)} | "
                    f"**Reps:** {ex.get('default_reps', '10-12')} | "
                    f"**Rest:** {ex.get('default_rest', '30s')}")

        if ex.get("default_hold"):
            lines.append(f"**Hold:** {ex.get('default_hold')}")

        lines.append("")
        lines.append("**Instructions:**")
        for j, instruction in enumerate(ex.get("instructions", []), 1):
            lines.append(f"{j}. {instruction}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Safety Reminders",
        "",
        "- Stop immediately if you experience sharp or sudden pain",
        "- Contact your physiotherapist if symptoms worsen",
        "- Perform exercises in a slow, controlled manner",
        "",
    ])

    return "\n".join(lines)


def _create_routine_object() -> Routine:
    """Create a Routine object from the current state."""
    routine_state: RoutineEditorState = st.session_state.routines

    routine_exercises = [
        RoutineExercise(exercise_id=ex_id, order=i + 1)
        for i, ex_id in enumerate(routine_state.exercise_ids)
    ]

    return Routine(
        id=f"routine_{uuid4().hex[:8]}",
        physio_id="default_physio",
        patient_name=routine_state.patient_name,
        diagnosis=routine_state.diagnosis,
        therapeutic_goals=routine_state.therapeutic_goals,
        title=f"{routine_state.patient_name}'s Exercise Program",
        exercises=routine_exercises,
    )
