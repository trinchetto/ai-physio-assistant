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
    """Muscle groups for anatomical reference."""

    # Neck
    DEEP_CERVICAL_FLEXORS = "deep cervical flexor muscles, longus colli, longus capitis"
    SUBOCCIPITALS = "suboccipital muscles"
    UPPER_TRAPEZIUS = "upper trapezius muscle"
    LEVATOR_SCAPULAE = "levator scapulae muscle"
    SCALENES = "scalene muscles"
    STERNOCLEIDOMASTOID = "sternocleidomastoid muscle"

    # Shoulder
    ROTATOR_CUFF = "rotator cuff muscles, supraspinatus, infraspinatus, teres minor, subscapularis"
    DELTOID = "deltoid muscle"
    RHOMBOIDS = "rhomboid muscles"
    SERRATUS_ANTERIOR = "serratus anterior muscle"

    # Spine
    ERECTOR_SPINAE = "erector spinae muscles"
    MULTIFIDUS = "multifidus muscle"
    THORACIC_EXTENSORS = "thoracic extensor muscles"
    LUMBAR_EXTENSORS = "lumbar extensor muscles"

    # Core
    TRANSVERSE_ABDOMINIS = "transverse abdominis muscle"
    RECTUS_ABDOMINIS = "rectus abdominis muscle"
    OBLIQUES = "internal and external oblique muscles"

    # Hip
    PIRIFORMIS = "piriformis muscle"
    GLUTEUS_MAXIMUS = "gluteus maximus muscle"
    GLUTEUS_MEDIUS = "gluteus medius muscle"
    HIP_FLEXORS = "hip flexor muscles, iliopsoas"
    ADDUCTORS = "hip adductor muscles"

    # Leg
    QUADRICEPS = "quadriceps muscle group"
    HAMSTRINGS = "hamstring muscles"
    GASTROCNEMIUS = "gastrocnemius muscle"
    SOLEUS = "soleus muscle"
    TIBIALIS_ANTERIOR = "tibialis anterior muscle"


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
            description="human figure seated upright demonstrating neutral cervical spine alignment, head balanced over shoulders",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SEATED,
            muscles_shown=["cervical spine", "head position neutral"],
            joints_shown=["cervical vertebrae alignment"],
        ),
        ExercisePrompt(
            exercise_id="chin_tuck",
            image_order=2,
            description="human figure performing cervical retraction exercise, chin drawn posteriorly, creating suboccipital stretch",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SEATED,
            muscles_shown=[MuscleGroup.DEEP_CERVICAL_FLEXORS, MuscleGroup.SUBOCCIPITALS],
            joints_shown=["cervical spine in retracted position"],
        ),
        ExercisePrompt(
            exercise_id="chin_tuck",
            image_order=3,
            description="comparison diagram showing forward head posture versus corrected cervical retraction, two head and neck profiles side by side",
            view_angle=ViewAngle.LATERAL,
            muscles_shown=["cervical alignment comparison"],
        ),
    ],
    "pendulum_exercise": [
        ExercisePrompt(
            exercise_id="pendulum_exercise",
            image_order=1,
            description="human figure in hip flexion position bent forward at waist, one hand supported on table surface, opposite arm hanging relaxed in dependent position, glenohumeral joint in neutral",
            view_angle=ViewAngle.LATERAL,
            muscles_shown=["relaxed shoulder musculature", "pendular arm position"],
            joints_shown=["glenohumeral joint", "hip flexion approximately 90 degrees"],
            equipment=["table or support surface"],
        ),
        ExercisePrompt(
            exercise_id="pendulum_exercise",
            image_order=2,
            description="human figure performing Codman pendulum exercise with circumduction movement pattern of dependent arm",
            view_angle=ViewAngle.ANTERIOR,
            muscles_shown=["relaxed shoulder girdle"],
            joints_shown=["glenohumeral joint passive movement"],
            equipment=["table support"],
            movement_indicators=True,
        ),
        ExercisePrompt(
            exercise_id="pendulum_exercise",
            image_order=3,
            description="human figure performing Codman pendulum exercise with sagittal plane pendular motion, arm swinging anterior to posterior",
            view_angle=ViewAngle.LATERAL,
            muscles_shown=["passive shoulder movement"],
            joints_shown=["glenohumeral flexion and extension range"],
            equipment=["table support"],
            movement_indicators=True,
        ),
    ],
    "cat_cow_stretch": [
        ExercisePrompt(
            exercise_id="cat_cow_stretch",
            image_order=1,
            description="human figure in quadruped position, neutral spine alignment, wrists directly under shoulders, knees under hips, tabletop position",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.QUADRUPED,
            muscles_shown=["neutral spinal curvature"],
            joints_shown=["wrist, shoulder, hip, knee alignment"],
        ),
        ExercisePrompt(
            exercise_id="cat_cow_stretch",
            image_order=2,
            description="human figure in quadruped position performing spinal flexion, thoracic and lumbar kyphosis, cat stretch pose, spine rounded superiorly toward ceiling, head in cervical flexion",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.QUADRUPED,
            muscles_shown=[MuscleGroup.ERECTOR_SPINAE, "stretched posterior chain"],
            joints_shown=["thoracic kyphosis", "lumbar flexion", "posterior pelvic tilt"],
        ),
        ExercisePrompt(
            exercise_id="cat_cow_stretch",
            image_order=3,
            description="human figure in quadruped position performing spinal extension, cow pose, lumbar lordosis, thoracic extension, anterior pelvic tilt, cervical extension with gaze forward",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.QUADRUPED,
            muscles_shown=[MuscleGroup.ERECTOR_SPINAE, "contracted spinal extensors"],
            joints_shown=["lumbar lordosis", "thoracic extension", "anterior pelvic tilt"],
        ),
    ],
    "piriformis_stretch_supine": [
        ExercisePrompt(
            exercise_id="piriformis_stretch_supine",
            image_order=1,
            description="human figure in supine position on floor, bilateral hip and knee flexion, feet flat on supporting surface, arms relaxed at sides",
            view_angle=ViewAngle.OBLIQUE,
            body_position=BodyPosition.SUPINE,
            muscles_shown=["relaxed lower extremity position"],
            joints_shown=["hip flexion", "knee flexion"],
        ),
        ExercisePrompt(
            exercise_id="piriformis_stretch_supine",
            image_order=2,
            description="human figure in supine position performing figure-four stretch, one ankle crossed over opposite knee creating lateral hip rotation, foot in dorsiflexion",
            view_angle=ViewAngle.OBLIQUE,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.PIRIFORMIS, "hip external rotators"],
            joints_shown=["hip external rotation", "figure-four leg position"],
        ),
        ExercisePrompt(
            exercise_id="piriformis_stretch_supine",
            image_order=3,
            description="human figure in supine position performing deep piriformis stretch, hands clasped behind thigh pulling leg toward chest, maintaining figure-four position, back flat on surface",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[
                MuscleGroup.PIRIFORMIS,
                MuscleGroup.GLUTEUS_MAXIMUS,
                "deep hip rotators stretched",
            ],
            joints_shown=["hip flexion with external rotation"],
        ),
    ],
    "calf_raises": [
        ExercisePrompt(
            exercise_id="calf_raises",
            image_order=1,
            description="human figure in standing position, feet hip-width apart, bilateral plantigrade stance, one hand on wall for balance support, upright posture",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.GASTROCNEMIUS, MuscleGroup.SOLEUS, "ankle neutral position"],
            joints_shown=["ankle in neutral", "subtalar joint"],
            equipment=["wall for support"],
        ),
        ExercisePrompt(
            exercise_id="calf_raises",
            image_order=2,
            description="human figure performing bilateral heel raise, plantarflexion at ankle, standing on metatarsal heads, heels elevated off floor, calf muscles contracted",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[
                MuscleGroup.GASTROCNEMIUS,
                MuscleGroup.SOLEUS,
                "contracted triceps surae",
            ],
            joints_shown=["ankle plantarflexion", "metatarsophalangeal extension"],
            equipment=["wall for support"],
        ),
        ExercisePrompt(
            exercise_id="calf_raises",
            image_order=3,
            description="anatomical close-up of foot and ankle performing calf raise, showing gastrocnemius and soleus contraction, heel elevated, weight on metatarsal heads",
            view_angle=ViewAngle.CLOSE_UP,
            muscles_shown=[MuscleGroup.GASTROCNEMIUS, MuscleGroup.SOLEUS, "Achilles tendon"],
            joints_shown=["ankle plantarflexion", "calcaneal elevation"],
        ),
    ],
}


def get_prompts_for_exercise(exercise_id: str) -> list[ExercisePrompt]:
    """Get all prompts for a specific exercise."""
    return EXERCISE_PROMPTS.get(exercise_id, [])


def get_all_exercise_ids() -> list[str]:
    """Get list of all exercise IDs with defined prompts."""
    return list(EXERCISE_PROMPTS.keys())
