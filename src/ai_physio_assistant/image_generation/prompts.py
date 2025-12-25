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
    # === NECK EXERCISES ===
    "neck_rotation": [
        ExercisePrompt(
            exercise_id="neck_rotation",
            image_order=1,
            description="seated, neutral head position, looking straight ahead",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SEATED,
        ),
        ExercisePrompt(
            exercise_id="neck_rotation",
            image_order=2,
            description="cervical rotation, head turned to side, looking over shoulder",
            view_angle=ViewAngle.SUPERIOR,
            body_position=BodyPosition.SEATED,
            muscles_shown=[MuscleGroup.STERNOCLEIDOMASTOID, MuscleGroup.SCALENES],
            joints_shown=["cervical rotation"],
        ),
    ],
    "lateral_neck_flexion": [
        ExercisePrompt(
            exercise_id="lateral_neck_flexion",
            image_order=1,
            description="seated upright, neutral head position",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SEATED,
        ),
        ExercisePrompt(
            exercise_id="lateral_neck_flexion",
            image_order=2,
            description="lateral cervical flexion, ear toward shoulder, neck side stretch",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SEATED,
            muscles_shown=[MuscleGroup.UPPER_TRAPEZIUS, MuscleGroup.SCALENES],
            joints_shown=["cervical lateral flexion"],
        ),
    ],
    "levator_scapulae_stretch": [
        ExercisePrompt(
            exercise_id="levator_scapulae_stretch",
            image_order=1,
            description="seated, hand grasping chair seat, head rotated 45 degrees and flexed",
            view_angle=ViewAngle.OBLIQUE,
            body_position=BodyPosition.SEATED,
            muscles_shown=[MuscleGroup.LEVATOR_SCAPULAE],
            joints_shown=["cervical rotation and flexion"],
        ),
    ],
    "scalene_stretch": [
        ExercisePrompt(
            exercise_id="scalene_stretch",
            image_order=1,
            description="standing, hand behind back, head tilted laterally and rotated upward",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.SCALENES],
            joints_shown=["cervical lateral flexion with rotation"],
        ),
    ],
    # === SHOULDER EXERCISES ===
    "wall_slides": [
        ExercisePrompt(
            exercise_id="wall_slides",
            image_order=1,
            description="back against wall, arms in goalpost position at 90 degrees",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.SERRATUS_ANTERIOR],
            equipment=["wall"],
        ),
        ExercisePrompt(
            exercise_id="wall_slides",
            image_order=2,
            description="wall slide, arms extended overhead, maintaining wall contact",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.SERRATUS_ANTERIOR, MuscleGroup.RHOMBOIDS],
            equipment=["wall"],
            movement_indicators=True,
        ),
    ],
    "shoulder_external_rotation": [
        ExercisePrompt(
            exercise_id="shoulder_external_rotation",
            image_order=1,
            description="standing, elbow bent 90 degrees at side, holding resistance band",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.ROTATOR_CUFF],
            equipment=["resistance band"],
        ),
        ExercisePrompt(
            exercise_id="shoulder_external_rotation",
            image_order=2,
            description="external rotation, forearm rotated outward, elbow at side",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.ROTATOR_CUFF],
            equipment=["resistance band"],
            movement_indicators=True,
        ),
    ],
    "cross_body_stretch": [
        ExercisePrompt(
            exercise_id="cross_body_stretch",
            image_order=1,
            description="arm across body at shoulder height, opposite hand pulling toward chest",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.STANDING,
            muscles_shown=["posterior shoulder"],
            joints_shown=["glenohumeral horizontal adduction"],
        ),
    ],
    "sleeper_stretch": [
        ExercisePrompt(
            exercise_id="sleeper_stretch",
            image_order=1,
            description="side-lying, bottom arm forward, elbow bent 90 degrees",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SIDE_LYING,
            muscles_shown=["posterior shoulder"],
        ),
        ExercisePrompt(
            exercise_id="sleeper_stretch",
            image_order=2,
            description="sleeper stretch, top hand pushing forearm toward floor",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SIDE_LYING,
            muscles_shown=[MuscleGroup.ROTATOR_CUFF],
            joints_shown=["glenohumeral internal rotation"],
        ),
    ],
    "ytwl_exercise": [
        ExercisePrompt(
            exercise_id="ytwl_exercise",
            image_order=1,
            description="prone on bench, arms in Y position, thumbs up",
            view_angle=ViewAngle.POSTERIOR,
            body_position=BodyPosition.PRONE,
            muscles_shown=[MuscleGroup.RHOMBOIDS],
        ),
        ExercisePrompt(
            exercise_id="ytwl_exercise",
            image_order=2,
            description="prone, showing Y T W L arm positions for scapular strengthening",
            view_angle=ViewAngle.POSTERIOR,
            body_position=BodyPosition.PRONE,
            muscles_shown=[MuscleGroup.RHOMBOIDS, MuscleGroup.ROTATOR_CUFF],
        ),
    ],
    # === UPPER BACK EXERCISES ===
    "thoracic_extension": [
        ExercisePrompt(
            exercise_id="thoracic_extension",
            image_order=1,
            description="supine, foam roller under upper back at shoulder blades, knees bent",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.THORACIC_EXTENSORS],
            equipment=["foam roller"],
        ),
        ExercisePrompt(
            exercise_id="thoracic_extension",
            image_order=2,
            description="extending backward over foam roller, thoracic spine arching",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.THORACIC_EXTENSORS],
            joints_shown=["thoracic extension"],
            equipment=["foam roller"],
        ),
    ],
    "thread_the_needle": [
        ExercisePrompt(
            exercise_id="thread_the_needle",
            image_order=1,
            description="quadruped position, neutral spine",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.QUADRUPED,
        ),
        ExercisePrompt(
            exercise_id="thread_the_needle",
            image_order=2,
            description="threading arm under torso, shoulder on floor, thoracic rotation",
            view_angle=ViewAngle.OBLIQUE,
            body_position=BodyPosition.QUADRUPED,
            muscles_shown=[MuscleGroup.THORACIC_EXTENSORS],
            joints_shown=["thoracic rotation"],
        ),
    ],
    "book_opener": [
        ExercisePrompt(
            exercise_id="book_opener",
            image_order=1,
            description="side-lying, knees bent, arms extended forward, palms together",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SIDE_LYING,
        ),
        ExercisePrompt(
            exercise_id="book_opener",
            image_order=2,
            description="open book stretch, top arm rotating open toward ceiling",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SIDE_LYING,
            muscles_shown=[MuscleGroup.THORACIC_EXTENSORS],
            joints_shown=["thoracic rotation"],
        ),
    ],
    "prone_y_raise": [
        ExercisePrompt(
            exercise_id="prone_y_raise",
            image_order=1,
            description="prone, arms overhead in Y position, thumbs up",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.PRONE,
        ),
        ExercisePrompt(
            exercise_id="prone_y_raise",
            image_order=2,
            description="prone Y raise, arms lifted, scapulae retracted",
            view_angle=ViewAngle.POSTERIOR,
            body_position=BodyPosition.PRONE,
            muscles_shown=[MuscleGroup.RHOMBOIDS],
            movement_indicators=True,
        ),
    ],
    # === LOWER BACK EXERCISES ===
    "bird_dog": [
        ExercisePrompt(
            exercise_id="bird_dog",
            image_order=1,
            description="quadruped, neutral spine, tabletop position",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.QUADRUPED,
            muscles_shown=[MuscleGroup.MULTIFIDUS],
        ),
        ExercisePrompt(
            exercise_id="bird_dog",
            image_order=2,
            description="bird dog, opposite arm and leg extended, level spine",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.QUADRUPED,
            muscles_shown=[MuscleGroup.ERECTOR_SPINAE, MuscleGroup.GLUTEUS_MAXIMUS],
            joints_shown=["hip extension", "shoulder flexion"],
        ),
    ],
    "pelvic_tilts": [
        ExercisePrompt(
            exercise_id="pelvic_tilts",
            image_order=1,
            description="supine, knees bent, feet flat, neutral spine",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
        ),
        ExercisePrompt(
            exercise_id="pelvic_tilts",
            image_order=2,
            description="posterior pelvic tilt, lower back flattened against floor",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.RECTUS_ABDOMINIS],
            joints_shown=["posterior pelvic tilt"],
        ),
    ],
    "mckenzie_extension": [
        ExercisePrompt(
            exercise_id="mckenzie_extension",
            image_order=1,
            description="prone, hands under shoulders, preparing for press up",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.PRONE,
        ),
        ExercisePrompt(
            exercise_id="mckenzie_extension",
            image_order=2,
            description="prone press up, arms extended, lumbar extension, hips on floor",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.PRONE,
            muscles_shown=[MuscleGroup.LUMBAR_EXTENSORS],
            joints_shown=["lumbar extension"],
        ),
    ],
    "childs_pose": [
        ExercisePrompt(
            exercise_id="childs_pose",
            image_order=1,
            description="child's pose, sitting back on heels, arms extended, forehead on floor",
            view_angle=ViewAngle.LATERAL,
            muscles_shown=[MuscleGroup.ERECTOR_SPINAE],
            joints_shown=["lumbar flexion", "hip flexion"],
        ),
    ],
    "knee_to_chest": [
        ExercisePrompt(
            exercise_id="knee_to_chest",
            image_order=1,
            description="supine, pulling one knee toward chest, hands behind thigh",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.ERECTOR_SPINAE],
            joints_shown=["hip flexion"],
        ),
        ExercisePrompt(
            exercise_id="knee_to_chest",
            image_order=2,
            description="double knee to chest, both knees pulled toward chest",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.LUMBAR_EXTENSORS],
            joints_shown=["bilateral hip flexion"],
        ),
    ],
    "glute_bridge": [
        ExercisePrompt(
            exercise_id="glute_bridge",
            image_order=1,
            description="supine, knees bent, feet flat, arms at sides",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
        ),
        ExercisePrompt(
            exercise_id="glute_bridge",
            image_order=2,
            description="glute bridge, hips lifted, straight line shoulders to knees",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.GLUTEUS_MAXIMUS, MuscleGroup.HAMSTRINGS],
            joints_shown=["hip extension"],
        ),
    ],
    "supine_spinal_twist": [
        ExercisePrompt(
            exercise_id="supine_spinal_twist",
            image_order=1,
            description="supine, one knee bent and crossed over body, arms extended",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.OBLIQUES],
            joints_shown=["lumbar rotation"],
        ),
    ],
    # === HIP EXERCISES ===
    "hip_flexor_stretch": [
        ExercisePrompt(
            exercise_id="hip_flexor_stretch",
            image_order=1,
            description="half-kneeling lunge, back knee on floor, front foot forward",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.KNEELING,
            muscles_shown=[MuscleGroup.HIP_FLEXORS],
            joints_shown=["hip extension rear leg"],
        ),
        ExercisePrompt(
            exercise_id="hip_flexor_stretch",
            image_order=2,
            description="deep hip flexor stretch, posterior pelvic tilt, torso upright",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.KNEELING,
            muscles_shown=[MuscleGroup.HIP_FLEXORS],
            joints_shown=["hip extension"],
        ),
    ],
    "clamshell": [
        ExercisePrompt(
            exercise_id="clamshell",
            image_order=1,
            description="side-lying, hips and knees bent, feet together",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SIDE_LYING,
            muscles_shown=[MuscleGroup.GLUTEUS_MEDIUS],
        ),
        ExercisePrompt(
            exercise_id="clamshell",
            image_order=2,
            description="clamshell, top knee raised, feet together, hip abduction",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SIDE_LYING,
            muscles_shown=[MuscleGroup.GLUTEUS_MEDIUS],
            joints_shown=["hip abduction"],
            movement_indicators=True,
        ),
    ],
    "fire_hydrant": [
        ExercisePrompt(
            exercise_id="fire_hydrant",
            image_order=1,
            description="quadruped, neutral spine",
            view_angle=ViewAngle.POSTERIOR,
            body_position=BodyPosition.QUADRUPED,
        ),
        ExercisePrompt(
            exercise_id="fire_hydrant",
            image_order=2,
            description="fire hydrant, lifting bent leg out to side",
            view_angle=ViewAngle.POSTERIOR,
            body_position=BodyPosition.QUADRUPED,
            muscles_shown=[MuscleGroup.GLUTEUS_MEDIUS],
            joints_shown=["hip abduction"],
            movement_indicators=True,
        ),
    ],
    "ninety_ninety_stretch": [
        ExercisePrompt(
            exercise_id="ninety_ninety_stretch",
            image_order=1,
            description="seated, front leg bent 90 degrees, back leg bent 90 degrees to side",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SEATED,
            muscles_shown=[MuscleGroup.PIRIFORMIS, MuscleGroup.GLUTEUS_MEDIUS],
            joints_shown=["hip rotation"],
        ),
    ],
    "seated_hip_internal_rotation": [
        ExercisePrompt(
            exercise_id="seated_hip_internal_rotation",
            image_order=1,
            description="seated, knees bent, knees dropping inward",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SEATED,
            joints_shown=["hip internal rotation"],
        ),
    ],
    "standing_hip_abduction": [
        ExercisePrompt(
            exercise_id="standing_hip_abduction",
            image_order=1,
            description="standing, lifting leg out to side, hand on wall",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.GLUTEUS_MEDIUS],
            joints_shown=["hip abduction"],
            equipment=["wall"],
            movement_indicators=True,
        ),
    ],
    # === KNEE EXERCISES ===
    "quad_sets": [
        ExercisePrompt(
            exercise_id="quad_sets",
            image_order=1,
            description="supine, leg extended, quadriceps relaxed",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.QUADRICEPS],
        ),
        ExercisePrompt(
            exercise_id="quad_sets",
            image_order=2,
            description="quad set, quadriceps contracted, pushing knee down",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.QUADRICEPS],
            joints_shown=["knee extension isometric"],
        ),
    ],
    "straight_leg_raise": [
        ExercisePrompt(
            exercise_id="straight_leg_raise",
            image_order=1,
            description="supine, one knee bent, other leg straight",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
        ),
        ExercisePrompt(
            exercise_id="straight_leg_raise",
            image_order=2,
            description="straight leg raise, quad contracted, leg lifted",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.QUADRICEPS, MuscleGroup.HIP_FLEXORS],
            joints_shown=["hip flexion"],
            movement_indicators=True,
        ),
    ],
    "hamstring_curl": [
        ExercisePrompt(
            exercise_id="hamstring_curl",
            image_order=1,
            description="standing on one leg, hand on wall",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            equipment=["wall"],
        ),
        ExercisePrompt(
            exercise_id="hamstring_curl",
            image_order=2,
            description="standing hamstring curl, heel toward buttock",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.HAMSTRINGS],
            joints_shown=["knee flexion"],
            equipment=["wall"],
            movement_indicators=True,
        ),
    ],
    "terminal_knee_extension": [
        ExercisePrompt(
            exercise_id="terminal_knee_extension",
            image_order=1,
            description="standing, resistance band behind knee, knee slightly bent",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.QUADRICEPS],
            equipment=["resistance band"],
        ),
        ExercisePrompt(
            exercise_id="terminal_knee_extension",
            image_order=2,
            description="terminal knee extension, straightening knee against band",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.QUADRICEPS],
            joints_shown=["knee extension"],
            equipment=["resistance band"],
        ),
    ],
    "wall_sit": [
        ExercisePrompt(
            exercise_id="wall_sit",
            image_order=1,
            description="wall sit, back against wall, thighs parallel to floor",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.QUADRICEPS, MuscleGroup.GLUTEUS_MAXIMUS],
            joints_shown=["knee flexion 90 degrees"],
            equipment=["wall"],
        ),
    ],
    "step_ups": [
        ExercisePrompt(
            exercise_id="step_ups",
            image_order=1,
            description="facing step, one foot on step",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            equipment=["step"],
        ),
        ExercisePrompt(
            exercise_id="step_ups",
            image_order=2,
            description="stepping up, pushing through front heel, body upright",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.QUADRICEPS, MuscleGroup.GLUTEUS_MAXIMUS],
            joints_shown=["knee extension", "hip extension"],
            equipment=["step"],
            movement_indicators=True,
        ),
    ],
    # === ANKLE/FOOT EXERCISES ===
    "ankle_circles": [
        ExercisePrompt(
            exercise_id="ankle_circles",
            image_order=1,
            description="foot and ankle, circular motion",
            view_angle=ViewAngle.LATERAL,
            joints_shown=["ankle circumduction"],
            movement_indicators=True,
        ),
    ],
    "towel_scrunches": [
        ExercisePrompt(
            exercise_id="towel_scrunches",
            image_order=1,
            description="seated, foot on towel, toes gripping towel",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SEATED,
            muscles_shown=["intrinsic foot muscles"],
            equipment=["towel"],
        ),
    ],
    "plantar_fascia_stretch": [
        ExercisePrompt(
            exercise_id="plantar_fascia_stretch",
            image_order=1,
            description="seated, foot crossed over knee, hand pulling toes back",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SEATED,
            muscles_shown=["plantar fascia"],
            joints_shown=["toe extension"],
        ),
    ],
    "heel_toe_walks": [
        ExercisePrompt(
            exercise_id="heel_toe_walks",
            image_order=1,
            description="walking on heels, toes lifted",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.TIBIALIS_ANTERIOR],
            joints_shown=["ankle dorsiflexion"],
        ),
        ExercisePrompt(
            exercise_id="heel_toe_walks",
            image_order=2,
            description="walking on toes, heels lifted",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.GASTROCNEMIUS],
            joints_shown=["ankle plantarflexion"],
        ),
    ],
    "single_leg_balance": [
        ExercisePrompt(
            exercise_id="single_leg_balance",
            image_order=1,
            description="standing on one leg, other leg lifted, arms at sides",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.GLUTEUS_MEDIUS],
            joints_shown=["single leg stance"],
        ),
    ],
    # === CORE EXERCISES ===
    "dead_bug": [
        ExercisePrompt(
            exercise_id="dead_bug",
            image_order=1,
            description="supine, arms toward ceiling, hips and knees bent 90 degrees",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.TRANSVERSE_ABDOMINIS],
        ),
        ExercisePrompt(
            exercise_id="dead_bug",
            image_order=2,
            description="dead bug, opposite arm and leg extended, back flat",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.TRANSVERSE_ABDOMINIS, MuscleGroup.OBLIQUES],
            movement_indicators=True,
        ),
    ],
    "plank": [
        ExercisePrompt(
            exercise_id="plank",
            image_order=1,
            description="forearm plank, straight line head to heels, core engaged",
            view_angle=ViewAngle.LATERAL,
            muscles_shown=[MuscleGroup.RECTUS_ABDOMINIS, MuscleGroup.OBLIQUES],
        ),
    ],
    "abdominal_bracing": [
        ExercisePrompt(
            exercise_id="abdominal_bracing",
            image_order=1,
            description="supine, knees bent, hands on abdomen, core contracted",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.SUPINE,
            muscles_shown=[MuscleGroup.TRANSVERSE_ABDOMINIS],
        ),
    ],
    "pallof_press": [
        ExercisePrompt(
            exercise_id="pallof_press",
            image_order=1,
            description="standing perpendicular to anchor, hands at chest, holding band",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.OBLIQUES],
            equipment=["resistance band"],
        ),
        ExercisePrompt(
            exercise_id="pallof_press",
            image_order=2,
            description="Pallof press, arms extended forward, resisting rotation",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.STANDING,
            muscles_shown=[MuscleGroup.OBLIQUES],
            equipment=["resistance band"],
            movement_indicators=True,
        ),
    ],
    "side_plank": [
        ExercisePrompt(
            exercise_id="side_plank",
            image_order=1,
            description="side plank on forearm, hips lifted, straight line head to feet",
            view_angle=ViewAngle.ANTERIOR,
            body_position=BodyPosition.SIDE_LYING,
            muscles_shown=[MuscleGroup.OBLIQUES, MuscleGroup.GLUTEUS_MEDIUS],
        ),
    ],
    # === WRIST/HAND EXERCISES ===
    "wrist_flexor_stretch": [
        ExercisePrompt(
            exercise_id="wrist_flexor_stretch",
            image_order=1,
            description="arm extended, palm up, other hand pulling fingers back",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=["wrist flexors"],
            joints_shown=["wrist extension"],
        ),
    ],
    "wrist_extensor_stretch": [
        ExercisePrompt(
            exercise_id="wrist_extensor_stretch",
            image_order=1,
            description="arm extended, palm down, fist, other hand pushing fist down",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=["wrist extensors"],
            joints_shown=["wrist flexion"],
        ),
    ],
    # === CHEST EXERCISES ===
    "doorway_pec_stretch": [
        ExercisePrompt(
            exercise_id="doorway_pec_stretch",
            image_order=1,
            description="standing in doorway, forearm on frame, stepping through",
            view_angle=ViewAngle.LATERAL,
            body_position=BodyPosition.STANDING,
            muscles_shown=["pectorals"],
            joints_shown=["shoulder horizontal abduction"],
            equipment=["doorway"],
        ),
    ],
}


def get_prompts_for_exercise(exercise_id: str) -> list[ExercisePrompt]:
    """Get all prompts for a specific exercise."""
    return EXERCISE_PROMPTS.get(exercise_id, [])


def get_all_exercise_ids() -> list[str]:
    """Get list of all exercise IDs with defined prompts."""
    return list(EXERCISE_PROMPTS.keys())
