"""
Routine data models for the AI Physio Assistant.

A Routine is a collection of exercises customized for a specific patient,
created by a physiotherapist with AI assistance.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RoutineStatus(str, Enum):
    """Routine lifecycle status."""

    DRAFT = "draft"  # Being composed/edited
    READY = "ready"  # Ready for delivery
    DELIVERED = "delivered"  # Sent to patient
    ARCHIVED = "archived"  # No longer active


class RoutineExercise(BaseModel):
    """
    An exercise within a routine, with patient-specific customizations.
    """

    exercise_id: str = Field(..., description="Reference to Exercise.id")
    order: int = Field(..., description="Position in the routine sequence", ge=1)

    # Parameter overrides (None = use exercise defaults)
    sets: int | None = Field(None, ge=1, le=10)
    reps: str | None = Field(None, description="Override reps/duration")
    hold: str | None = Field(None, description="Override hold duration")
    rest: str | None = Field(None, description="Override rest period")

    # Patient-specific notes
    notes: str | None = Field(
        None, description="Special instructions for this patient (e.g., 'Use lighter resistance')"
    )
    progression: str | None = Field(
        None, description="How to progress this exercise (e.g., 'Add 2 reps each week')"
    )

    # Flags
    is_warmup: bool = Field(default=False, description="Part of warmup section")
    is_cooldown: bool = Field(default=False, description="Part of cooldown section")


class Routine(BaseModel):
    """
    A complete exercise routine for a patient.

    Created by a physiotherapist with AI assistance, routines are
    customized programs that can be delivered via web link or PDF.
    """

    # Identifiers
    id: str = Field(..., description="Unique routine ID")
    physio_id: str = Field(..., description="Physiotherapist who created this")

    # Patient info
    patient_name: str = Field(..., description="Patient's name for the handout")
    patient_language: str = Field(
        default="en", description="ISO 639-1 code for patient's preferred language"
    )
    patient_id: str | None = Field(None, description="Optional reference to patient record")

    # Clinical context
    diagnosis: str = Field(..., description="Primary diagnosis or reason for treatment")
    therapeutic_goals: list[str] = Field(
        ...,
        description="What we want to achieve (e.g., 'Reduce shoulder pain', 'Improve ROM')",
        min_length=1,
    )
    precautions: list[str] = Field(
        default_factory=list, description="Patient-specific precautions to observe"
    )

    # The routine content
    title: str = Field(
        ..., description="Routine title shown to patient (e.g., 'Shoulder Recovery Program')"
    )
    exercises: list[RoutineExercise] = Field(
        ..., description="Ordered list of exercises", min_length=1
    )

    # Schedule
    frequency: str = Field(
        default="once daily",
        description="How often to perform (e.g., 'twice daily', '3x per week')",
    )
    duration_weeks: int | None = Field(None, description="Recommended program duration in weeks")
    estimated_time_minutes: int | None = Field(
        None, description="Estimated time to complete one session"
    )

    # Patient guidance
    general_notes: str | None = Field(
        None, description="General instructions or context for the patient"
    )
    warning_signs: list[str] = Field(
        default_factory=lambda: [
            "Stop immediately if you experience sharp or sudden pain",
            "Contact your physiotherapist if symptoms worsen",
        ],
        description="When to stop and seek help",
    )

    # Delivery
    status: RoutineStatus = Field(default=RoutineStatus.DRAFT)
    delivery_url: str | None = Field(None, description="Shareable web link for the patient")
    pdf_url: str | None = Field(None, description="Generated PDF download link")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    delivered_at: datetime | None = Field(None)

    # AI assistance tracking
    ai_generated: bool = Field(default=False, description="Whether initial draft was AI-generated")
    ai_prompt: str | None = Field(
        None, description="The prompt used to generate this routine (for learning)"
    )

    class Config:
        use_enum_values = True
