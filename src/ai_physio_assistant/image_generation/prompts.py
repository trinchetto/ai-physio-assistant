"""
Medical-style prompt builder for exercise illustrations.

Uses anatomical terminology and medical illustration conventions
for better results with fine-tuned SDXL models.
"""

from dataclasses import dataclass
from enum import Enum


class ViewAngle(str, Enum):
    """Standard anatomical viewing angles."""

    LATERAL = "lateral view"  # Side view
    ANTERIOR = "anterior view"  # Front view
    POSTERIOR = "posterior view"  # Back view
    LATERAL_RIGHT = "right lateral view"
    LATERAL_LEFT = "left lateral view"
    SUPERIOR = "superior view"  # From above
    OBLIQUE = "oblique view"  # 3/4 angle
    CLOSE_UP = "close-up detail view"


class BodyPosition(str, Enum):
    """Common body positions in physiotherapy."""

    STANDING = "standing position, upright posture"
    SEATED = "seated position on chair, upright posture"
    SUPINE = "supine position, lying on back"
    PRONE = "prone position, lying face down"
    QUADRUPED = "quadruped position, on hands and knees"
    SIDE_LYING = "side-lying position"
    KNEELING = "kneeling position"


@dataclass
class MuscleGroup:
    """Muscle groups for anatomical reference. Kept concise for CLIP's 77 token limit."""

    # Neck
    DEEP_CERVICAL_FLEXORS = "deep cervical flexors"
    SUBOCCIPITALS = "suboccipital muscles"
    UPPER_TRAPEZIUS = "upper trapezius"
    LEVATOR_SCAPULAE = "levator scapulae"
    SCALENES = "scalenes"
    STERNOCLEIDOMASTOID = "sternocleidomastoid"

    # Shoulder
    ROTATOR_CUFF = "rotator cuff"
    DELTOID = "deltoid"
    RHOMBOIDS = "rhomboids"
    SERRATUS_ANTERIOR = "serratus anterior"

    # Spine
    ERECTOR_SPINAE = "erector spinae"
    MULTIFIDUS = "multifidus"
    THORACIC_EXTENSORS = "thoracic extensors"
    LUMBAR_EXTENSORS = "lumbar extensors"

    # Core
    TRANSVERSE_ABDOMINIS = "transverse abdominis"
    RECTUS_ABDOMINIS = "rectus abdominis"
    OBLIQUES = "obliques"

    # Hip
    PIRIFORMIS = "piriformis"
    GLUTEUS_MAXIMUS = "gluteus maximus"
    GLUTEUS_MEDIUS = "gluteus medius"
    HIP_FLEXORS = "hip flexors"
    ADDUCTORS = "hip adductors"

    # Leg
    QUADRICEPS = "quadriceps"
    HAMSTRINGS = "hamstrings"
    GASTROCNEMIUS = "gastrocnemius"
    SOLEUS = "soleus"
    TIBIALIS_ANTERIOR = "tibialis anterior"


@dataclass
class ExercisePrompt:
    """A complete prompt for generating an exercise illustration."""

    exercise_id: str
    image_order: int
    description: str
    view_angle: ViewAngle
    body_position: BodyPosition | None = None
    muscles_shown: list[str] | None = None
    joints_shown: list[str] | None = None
    equipment: list[str] | None = None
    movement_indicators: bool = False  # Show dotted lines for movement

    def build_prompt(self, style_prefix: str = "", style_suffix: str = "") -> str:
        """Build the complete prompt string."""
        parts = []

        # Style prefix
        if style_prefix:
            parts.append(style_prefix)

        # View angle
        parts.append(self.view_angle.value)

        # Body position
        if self.body_position:
            parts.append(self.body_position.value)

        # Main description
        parts.append(self.description)

        # Anatomical details
        if self.muscles_shown:
            muscles = ", ".join(self.muscles_shown)
            parts.append(f"showing {muscles}")

        if self.joints_shown:
            joints = ", ".join(self.joints_shown)
            parts.append(f"highlighting {joints}")

        # Equipment
        if self.equipment:
            equip = ", ".join(self.equipment)
            parts.append(f"using {equip}")

        # Movement indicators
        if self.movement_indicators:
            parts.append("with dotted lines indicating movement direction and range")

        # Style suffix
        if style_suffix:
            parts.append(style_suffix)

        return ", ".join(parts)


# Pre-defined prompts for the seed exercises
EXERCISE_PROMPTS: dict[str, list[ExercisePrompt]] = {
    "chin_tuck": [
        ExercisePrompt(
            exercise_id="chin_tuck",
            image_order=1,
            description="seated figure, neutral cervical spine, head balanced over shoulders",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SEATED,
            muscles_shown=["cervical spine neutral"],
            joints_shown=["cervical alignment"],
        ),
        ExercisePrompt(
            exercise_id="chin_tuck",
            image_order=2,
            description="cervical retraction, chin drawn back, suboccipital stretch",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SEATED,
            muscles_shown=[MuscleGroup.DEEP_CERVICAL_FLEXORS, MuscleGroup.SUBOCCIPITALS],
            joints_shown=["cervical retraction"],
        ),
        ExercisePrompt(
            exercise_id="chin_tuck",
            image_order=3,
            description="forward head posture vs corrected alignment, side-by-side comparison",
            view_angle=ViewAngle.LATERAL,
            muscles_shown=["cervical alignment"],
        ),
    ],
    "pendulum_exercise": [
        ExercisePrompt(
            exercise_id="pendulum_exercise",
            image_order=1,
            description="bent forward at waist, hand on table, opposite arm hanging relaxed",
            view_angle=ViewAngle.LATERAL,
            muscles_shown=["relaxed shoulder"],
            joints_shown=["glenohumeral joint", "hip flexion 90 degrees"],
            equipment=["table"],
        ),
        ExercisePrompt(
            exercise_id="pendulum_exercise",
            image_order=2,
            description="Codman pendulum, arm circumduction movement",
            view_angle=ViewAngle.ANTERIOR,
            muscles_shown=["relaxed shoulder"],
            joints_shown=["glenohumeral passive movement"],
            equipment=["table"],
            movement_indicators=True,
        ),
        ExercisePrompt(
            exercise_id="pendulum_exercise",
            image_order=3,
            description="pendulum exercise, arm swinging forward and back",
            view_angle=ViewAngle.LATERAL,
            muscles_shown=["shoulder passive movement"],
            joints_shown=["glenohumeral flexion-extension"],
            equipment=["table"],
            movement_indicators=True,
        ),
    ],
    "cat_cow_stretch": [
        ExercisePrompt(
            exercise_id="cat_cow_stretch",
            image_order=1,
            description="tabletop position, neutral spine, wrists under shoulders, knees under hips",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.QUADRUPED,
            muscles_shown=["neutral spine"],
            joints_shown=["spine alignment"],
        ),
        ExercisePrompt(
            exercise_id="cat_cow_stretch",
            image_order=2,
            description="cat pose, spine rounded upward, head down, thoracic and lumbar kyphosis",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.QUADRUPED,
            muscles_shown=[MuscleGroup.ERECTOR_SPINAE],
            joints_shown=["thoracic kyphosis", "lumbar flexion"],
        ),
        ExercisePrompt(
            exercise_id="cat_cow_stretch",
            image_order=3,
            description="cow pose, spine arched downward, head up, lumbar lordosis",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.QUADRUPED,
            muscles_shown=[MuscleGroup.ERECTOR_SPINAE],
            joints_shown=["lumbar lordosis", "thoracic extension"],
        ),
    ],
    "piriformis_stretch_supine": [
        ExercisePrompt(
            exercise_id="piriformis_stretch_supine",
            image_order=1,
            description="lying on back, knees bent, feet flat, arms at sides",
            view_angle=ViewAngle.OBLIQUE,
            body_position=BodyPosition.SUPINE,
            muscles_shown=["relaxed position"],
            joints_shown=["hip flexion", "knee flexion"],
        ),
        ExercisePrompt(
            exercise_id="piriformis_stretch_supine",
            image_order=2,
            description="figure-four position, ankle crossed over opposite knee",
            view_angle=ViewAngle.OBLIQUE,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.PIRIFORMIS],
            joints_shown=["hip external rotation"],
        ),
        ExercisePrompt(
            exercise_id="piriformis_stretch_supine",
            image_order=3,
            description="deep piriformis stretch, hands behind thigh, pulling leg to chest",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.PIRIFORMIS, MuscleGroup.GLUTEUS_MAXIMUS],
            joints_shown=["hip flexion with external rotation"],
        ),
    ],
    "calf_raises": [
        ExercisePrompt(
            exercise_id="calf_raises",
            image_order=1,
            description="standing, feet hip-width, hand on wall for balance",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.GASTROCNEMIUS, MuscleGroup.SOLEUS],
            joints_shown=["ankle neutral"],
            equipment=["wall"],
        ),
        ExercisePrompt(
            exercise_id="calf_raises",
            image_order=2,
            description="heel raise, standing on toes, calves contracted",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.GASTROCNEMIUS, MuscleGroup.SOLEUS],
            joints_shown=["ankle plantarflexion"],
            equipment=["wall"],
        ),
        ExercisePrompt(
            exercise_id="calf_raises",
            image_order=3,
            description="close-up foot and ankle, calf raise, heel elevated",
            view_angle=ViewAngle.CLOSE_UP,
            muscles_shown=[MuscleGroup.GASTROCNEMIUS, MuscleGroup.SOLEUS],
            joints_shown=["ankle plantarflexion"],
        ),
    ],
}


def get_prompts_for_exercise(exercise_id: str) -> list[ExercisePrompt]:
    """Get all prompts for a specific exercise."""
    return EXERCISE_PROMPTS.get(exercise_id, [])


def get_all_exercise_ids() -> list[str]:
    """Get list of all exercise IDs with defined prompts."""
    return list(EXERCISE_PROMPTS.keys())
