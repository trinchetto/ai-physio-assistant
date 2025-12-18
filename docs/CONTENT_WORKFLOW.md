# Content Creation Workflow

This document describes how to create and expand the exercise database.

## Overview

The exercise database is built through a collaborative process:
1. AI drafts exercise content based on guidelines
2. Physiotherapist reviews for medical accuracy
3. Images are created or sourced
4. Content is finalized and added to the database

## Creating New Exercises

### Step 1: Identify Needed Exercises

Consider:
- Which body regions need more coverage?
- What conditions are commonly treated but lack exercises?
- Are there progression variations needed (beginner → advanced)?

### Step 2: Draft with AI Assistance

Provide the AI with:
- Exercise name and type (stretch, strengthening, mobility)
- Target body region and structures
- Therapeutic purpose
- Any specific technique notes

The AI will generate:
- Structured YAML following the template
- Step-by-step instructions
- Common mistakes to avoid
- Translations (if needed)

### Step 3: Review for Accuracy

Check:
- [ ] Instructions are anatomically correct
- [ ] Contraindications are appropriate and complete
- [ ] Common mistakes reflect real patient errors
- [ ] Difficulty level is appropriate
- [ ] Default parameters (sets, reps, hold) are reasonable
- [ ] Translations are accurate (if provided)

### Step 4: Add Images

Each exercise should have 2-3 images:

| Position | Purpose |
|----------|---------|
| Starting | Show initial posture and setup |
| Movement | Show the action in progress |
| End | Show final position (if different from start) |

Image requirements:
- Clear, uncluttered background
- Consistent style across all exercises
- Correct form demonstrated
- Any equipment clearly visible

### Step 5: Save and Validate

1. Save the YAML file in the appropriate body region folder
2. Run validation to check schema compliance
3. Review in the application

## Exercise Categories to Cover

### Priority 1: Foundational (First 40 exercises)

| Body Region | Count | Key Exercises |
|-------------|-------|---------------|
| Neck | 5 | Chin tucks, rotations, lateral flexion, levator stretch, scalene stretch |
| Shoulder | 6 | Pendulum, wall slides, external rotation, cross-body stretch, sleeper stretch, YTWL |
| Upper Back | 4 | Thoracic extension, cat-cow, thread the needle, foam roller extension |
| Lower Back | 6 | Bird-dog, pelvic tilts, McKenzie, child's pose, knee-to-chest, bridges |
| Hip | 6 | Piriformis stretch, hip flexor stretch, clamshells, glute bridges, fire hydrants, 90-90 stretch |
| Knee | 5 | Quad sets, straight leg raises, hamstring curls, terminal knee extension, wall sits |
| Ankle/Foot | 4 | Calf raises, ankle circles, towel scrunches, plantar fascia stretch |
| Core | 4 | Dead bug, plank, abdominal bracing, pallof press |

### Priority 2: Condition-Specific (Next 30 exercises)

- Rotator cuff rehabilitation series
- Sciatica relief protocol
- Post-surgical progressions
- Sports-specific exercises

### Priority 3: Advanced Variations (Ongoing)

- Resistance band progressions
- Balance challenge progressions
- Plyometric variations

## Batch Content Creation

For efficient content creation, work in batches:

1. **Define the batch**: e.g., "5 shoulder exercises for rotator cuff"
2. **AI drafts all 5**: Generate structured YAML for each
3. **Review together**: Compare for consistency
4. **Create images together**: Maintain visual consistency
5. **Import as batch**: Add all to database together

## Quality Checklist

Before adding an exercise to the database:

### Medical Accuracy
- [ ] Instructions describe correct anatomical movement
- [ ] Target muscles/structures are correctly identified
- [ ] Contraindications are medically appropriate
- [ ] Difficulty level matches actual complexity

### Clarity
- [ ] Instructions are understandable by patients
- [ ] No jargon without explanation
- [ ] Step-by-step order is logical
- [ ] Common mistakes are specific and actionable

### Completeness
- [ ] All required fields are filled
- [ ] At least 2 common mistakes listed
- [ ] Appropriate tags for searchability
- [ ] Images show all key positions

### Translations
- [ ] Translations maintain meaning (not just literal)
- [ ] Medical terms are correctly localized
- [ ] Instructions flow naturally in target language

## File Organization

```
content/exercises/
├── _template.yaml          # Copy this for new exercises
├── neck/
│   ├── chin_tuck.yaml
│   ├── neck_rotation.yaml
│   └── ...
├── shoulder/
│   ├── pendulum_exercise.yaml
│   └── ...
├── lower_back/
│   ├── cat_cow_stretch.yaml
│   └── ...
└── ...
```

## Tracking Progress

Maintain a spreadsheet or document tracking:
- Exercises needed per body region
- Exercises drafted (pending review)
- Exercises reviewed (pending images)
- Exercises complete (ready for production)

## Tips for Good Content

1. **Write for patients**: Assume no medical knowledge
2. **Be specific**: "Lift your arm to shoulder height" not "Raise your arm"
3. **Include sensory cues**: "You should feel a stretch in the front of your hip"
4. **Add safety notes**: "If you feel sharp pain, stop immediately"
5. **Keep instructions short**: One action per step
6. **Use consistent terminology**: Same terms across all exercises
