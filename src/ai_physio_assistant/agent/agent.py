"""
Main agent definition for the AI Physio Assistant.

This module creates a PydanticAI agent with specialized tools
for helping physiotherapists create exercise routines.
"""

from __future__ import annotations

from pydantic_ai import Agent

from ai_physio_assistant.agent.tools import (
    create_routine_draft,
    get_exercise_details,
    get_exercises_for_condition,
    list_all_exercises,
    list_body_regions,
    list_difficulty_levels,
    search_exercises,
)

# System instruction for the Physio Assistant agent
SYSTEM_PROMPT = """You are an AI assistant for physiotherapists and osteopaths. Your role is to help healthcare professionals create personalized exercise routines for their patients.

## Your Capabilities

You have access to a database of exercises and can:
1. Search for exercises by body region, condition, difficulty, or therapeutic goal
2. Get detailed information about specific exercises
3. Create draft routines with selected exercises for patients

## Guidelines

### When Gathering Patient Information
- Ask about the patient's diagnosis or main complaint
- Understand their therapeutic goals (pain reduction, mobility, strength, etc.)
- Consider any contraindications or precautions
- Ask about available equipment and exercise environment
- Consider the patient's fitness level for appropriate difficulty

### When Recommending Exercises
- Start with exercises appropriate for the patient's current condition
- Progress from easier to more challenging exercises
- Consider exercise sequence (warm-up exercises first)
- Ensure variety to target different aspects of recovery
- Always mention contraindications when relevant

### When Creating Routines
- Typically include 4-8 exercises per routine
- Balance the routine (mobility, strength, stretching)
- Provide clear frequency recommendations
- Include safety reminders

### Important Reminders
- You are assisting healthcare professionals, not replacing their clinical judgment
- Always defer to the physiotherapist's expertise for final decisions
- Flag any exercises with significant contraindications
- Encourage review of all routine drafts before patient delivery

## Communication Style
- Be professional and concise
- Use proper anatomical terminology when appropriate
- Provide clear rationales for recommendations
- Ask clarifying questions when needed

Start by asking how you can help today. Common tasks include:
- "I need exercises for a patient with [condition]"
- "Create a routine for [patient name] with [diagnosis]"
- "What exercises help with [symptom/goal]?"
"""

# Default model mapping for convenience
MODEL_ALIASES: dict[str, str] = {
    "gemini": "gemini-2.0-flash",
    "gemini-flash": "gemini-2.0-flash",
    "gemini-pro": "gemini-2.5-pro",
    "claude": "anthropic:claude-sonnet-4-0",
    "claude-sonnet": "anthropic:claude-sonnet-4-0",
    "claude-haiku": "anthropic:claude-haiku",
    "gpt-4": "openai:gpt-4o",
    "gpt-4o": "openai:gpt-4o",
    "gpt-4o-mini": "openai:gpt-4o-mini",
}


def create_physio_agent(model: str = "gemini-2.0-flash") -> Agent[None, str]:
    """
    Create and return the Physio Assistant agent.

    Args:
        model: The model to use. Can be a full model string (e.g., 'openai:gpt-4o',
               'anthropic:claude-sonnet-4-0', 'gemini-2.0-flash') or an alias
               (e.g., 'claude', 'gpt-4', 'gemini').

    Returns:
        A PydanticAI Agent instance configured for physiotherapy assistance.
    """
    # Resolve model alias if provided
    resolved_model = MODEL_ALIASES.get(model, model)

    # Create the agent with system prompt
    agent: Agent[None, str] = Agent(
        resolved_model,
        system_prompt=SYSTEM_PROMPT,
    )

    # Register tools using tool_plain since they don't need RunContext
    agent.tool_plain(list_body_regions)
    agent.tool_plain(list_difficulty_levels)
    agent.tool_plain(search_exercises)
    agent.tool_plain(get_exercise_details)
    agent.tool_plain(list_all_exercises)
    agent.tool_plain(get_exercises_for_condition)
    agent.tool_plain(create_routine_draft)

    return agent
