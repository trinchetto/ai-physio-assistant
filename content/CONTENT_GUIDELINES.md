# Exercise Content Guidelines

This document describes how to create and format exercises for the AI Physio Assistant.

## Exercise YAML Format

Each exercise is defined in a YAML file. Files are organized by body region:
- `content/exercises/neck/`
- `content/exercises/shoulder/`
- `content/exercises/lower_back/`
- etc.

## Required Fields

Every exercise MUST have:

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique identifier (snake_case) | `chin_tuck` |
| `name` | Human-readable name | `"Chin Tuck"` |
| `description` | What the exercise does (1-2 sentences) | `"Strengthens deep neck flexors..."` |
| `instructions` | Step-by-step list (minimum 3 steps) | See below |
| `body_regions` | List of targeted areas | `[neck]` |

## Writing Good Instructions

Instructions should be:
1. **Clear**: Use simple, direct language
2. **Specific**: Include positions, angles, durations
3. **Sequenced**: Logical order from start to finish
4. **Safe**: Include breathing cues and warnings where relevant

### Instruction Template

```yaml
instructions:
  - "Starting position: [describe initial posture/position]"
  - "Movement: [describe the action to perform]"
  - "Hold: [if applicable, describe hold and duration]"
  - "Return: [describe how to return to start]"
  - "Repeat: [specify repetitions or duration]"
```

### Example (Good)

```yaml
instructions:
  - "Sit or stand with your back straight and shoulders relaxed"
  - "Look straight ahead, keeping your eyes level"
  - "Slowly draw your chin back, as if making a double chin"
  - "Hold for 5 seconds, feeling a gentle stretch at the base of your skull"
  - "Slowly return to the starting position"
  - "Repeat 10 times"
```

### Example (Bad - Too Vague)

```yaml
instructions:
  - "Move your chin back"
  - "Hold it"
  - "Repeat"
```

## Common Mistakes Section

List 2-4 common errors patients make. Format as what they do wrong and why it matters:

```yaml
common_mistakes:
  - "Tilting the head down instead of retracting chin - this stretches the wrong muscles"
  - "Pushing the chin too far back causing pain - the movement should be gentle"
  - "Holding breath during the exercise - breathe normally throughout"
```

## Difficulty Levels

| Level | Criteria |
|-------|----------|
| `beginner` | No equipment, simple movement, low injury risk |
| `intermediate` | May need equipment, compound movement, moderate control needed |
| `advanced` | Complex movement, high control needed, builds on simpler exercises |

## Body Regions

Use these standard values:
- `neck`
- `shoulder`
- `upper_back`
- `lower_back`
- `chest`
- `core`
- `hip`
- `knee`
- `ankle_foot`
- `wrist_hand`
- `elbow`
- `full_body`

## Conditions and Therapeutic Goals

### Common Conditions (use snake_case)

```
neck_pain, cervical_radiculopathy, whiplash, tension_headache
shoulder_impingement, rotator_cuff_injury, frozen_shoulder, post_surgery_shoulder
thoracic_kyphosis, upper_crossed_syndrome, postural_dysfunction
lower_back_pain, disc_herniation, sciatica, spinal_stenosis, post_surgery_spine
hip_osteoarthritis, hip_bursitis, piriformis_syndrome
knee_osteoarthritis, patellofemoral_syndrome, post_surgery_knee, acl_recovery
ankle_sprain, plantar_fasciitis, achilles_tendinopathy
```

### Therapeutic Goals (use snake_case)

```
reduce_pain, improve_mobility, increase_strength, improve_flexibility
improve_posture, increase_stability, improve_balance, reduce_stiffness
maintain_range_of_motion, prevent_recurrence
```

## Contraindications

List conditions where the exercise should NOT be performed:

```yaml
contraindications:
  - "acute_disc_herniation"
  - "cervical_instability"
  - "recent_neck_surgery"
```

## Equipment

Common equipment values:
- `none` (bodyweight only)
- `resistance_band`
- `foam_roller`
- `exercise_ball`
- `chair`
- `wall`
- `towel`
- `pillow`
- `dumbbells`
- `theraband`

## Translations

Translations are stored in the `translations` section:

```yaml
translations:
  it:
    name: "Retrazione del Mento"
    description: "Rafforza i muscoli flessori profondi del collo..."
    instructions:
      - "Siediti o stai in piedi con la schiena dritta..."
      - ...
    common_mistakes:
      - "Inclinare la testa in basso invece di retrarre il mento..."
```

## Image Requirements

Each exercise should have 2-3 images:

| Order | Purpose | Description |
|-------|---------|-------------|
| 1 | Starting position | Show the initial posture |
| 2 | Movement/Mid-point | Show the exercise in action |
| 3 | End position | Show the final position (if different from start) |

Images are generated using the SDXL image generation service with anatomical prompts.

### Generating Images

1. Add prompts in `src/image_generation/prompts.py`
2. Run: `python scripts/generate_images.py --exercise <id>`

See `IMAGE_GENERATION_GUIDE.md` for detailed instructions.

### Image Style

Generated images use:
- Anatomical diagram style (medical textbook aesthetic)
- Gender-neutral figure
- Clean white background
- Proper anatomical terminology in prompts

## Complete Example

See `content/exercises/_template.yaml` for a complete example.
