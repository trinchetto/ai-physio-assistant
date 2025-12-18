"""
Exercise data models for the AI Physio Assistant.

These models define the structure for exercises stored in the database
and used throughout the application.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Difficulty(str, Enum):
    """Exercise difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class BodyRegion(str, Enum):
    """Major body regions for categorization."""
    NECK = "neck"
    SHOULDER = "shoulder"
    UPPER_BACK = "upper_back"
    LOWER_BACK = "lower_back"
    CHEST = "chest"
    CORE = "core"
    HIP = "hip"
    KNEE = "knee"
    ANKLE_FOOT = "ankle_foot"
    WRIST_HAND = "wrist_hand"
    ELBOW = "elbow"
    FULL_BODY = "full_body"


class ExerciseSource(str, Enum):
    """How the exercise was created."""
    MANUAL = "manual"  # Physio created manually
    AI_ASSISTED = "ai_assisted"  # AI drafted, physio reviewed
    IMPORTED = "imported"  # Imported from external source
    SHARED = "shared"  # Copied from shared library


class ImageRef(BaseModel):
    """Reference to an exercise image."""
    url: str = Field(..., description="Cloud Storage URL or path")
    alt_text: str = Field(..., description="Accessibility description")
    order: int = Field(..., description="Display order (1=start, 2=mid, 3=end)")
    caption: Optional[str] = Field(None, description="Optional caption for the image")


class ExerciseTranslation(BaseModel):
    """Translated content for an exercise."""
    language: str = Field(..., description="ISO 639-1 language code (e.g., 'it', 'en')")
    name: str
    description: str
    instructions: list[str]
    common_mistakes: list[str]

    # Optional: translated image alt texts
    image_alt_texts: Optional[list[str]] = None


class Exercise(BaseModel):
    """
    Complete exercise definition.

    Exercises are owned by individual physios but can be shared.
    Content is stored in the physio's primary language with
    translations cached or generated on-demand.
    """

    # Identifiers
    id: str = Field(..., description="Unique exercise ID")
    owner_id: str = Field(
        ...,
        description="Physio ID who owns this exercise, or 'shared' for community exercises"
    )

    # Core content (in primary language)
    name: str = Field(..., description="Exercise name", min_length=3, max_length=100)
    primary_language: str = Field(default="en", description="ISO 639-1 code for primary language")
    description: str = Field(
        ...,
        description="What this exercise does, which muscles/structures it targets"
    )
    instructions: list[str] = Field(
        ...,
        description="Step-by-step instructions for performing the exercise",
        min_length=2
    )
    common_mistakes: list[str] = Field(
        default_factory=list,
        description="Common errors to avoid"
    )

    # Categorization
    body_regions: list[BodyRegion] = Field(
        ...,
        description="Primary body regions targeted",
        min_length=1
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Conditions this exercise helps with (e.g., 'rotator_cuff_injury', 'sciatica')"
    )
    therapeutic_goals: list[str] = Field(
        default_factory=list,
        description="Goals like 'improve_mobility', 'strengthen', 'reduce_pain', 'stretch'"
    )
    contraindications: list[str] = Field(
        default_factory=list,
        description="Conditions where this exercise should NOT be used"
    )

    # Parameters
    difficulty: Difficulty = Field(default=Difficulty.BEGINNER)
    equipment: list[str] = Field(
        default_factory=lambda: ["none"],
        description="Required equipment (use ['none'] if no equipment needed)"
    )

    # Default parameters (can be overridden in routines)
    default_sets: int = Field(default=3, ge=1, le=10)
    default_reps: str = Field(
        default="10-12",
        description="Reps or duration, e.g., '10-12' or '30 seconds' or '5 breaths'"
    )
    default_hold: Optional[str] = Field(
        None,
        description="Hold duration per rep, e.g., '5 seconds'"
    )
    default_rest: str = Field(
        default="30 seconds",
        description="Rest between sets"
    )

    # Media
    images: list[ImageRef] = Field(
        default_factory=list,
        description="Exercise images (ideally 2-3: start, movement, end position)"
    )
    video_url: Optional[str] = Field(
        None,
        description="Optional video demonstration URL"
    )

    # Translations
    translations: dict[str, ExerciseTranslation] = Field(
        default_factory=dict,
        description="Cached translations keyed by language code"
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    source: ExerciseSource = Field(default=ExerciseSource.MANUAL)
    tags: list[str] = Field(
        default_factory=list,
        description="Free-form tags for additional categorization"
    )

    class Config:
        use_enum_values = True
