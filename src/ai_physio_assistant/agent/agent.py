"""
Main agent definition for the AI Physio Assistant.

This module creates a LangChain/LangGraph agent with specialized tools
for helping physiotherapists create exercise routines.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from ai_physio_assistant.agent.tools import (
    create_routine_draft as _create_routine_draft,
)
from ai_physio_assistant.agent.tools import (
    get_exercise_details as _get_exercise_details,
)
from ai_physio_assistant.agent.tools import (
    get_exercises_for_condition as _get_exercises_for_condition,
)
from ai_physio_assistant.agent.tools import (
    list_all_exercises as _list_all_exercises,
)
from ai_physio_assistant.agent.tools import (
    list_body_regions as _list_body_regions,
)
from ai_physio_assistant.agent.tools import (
    list_difficulty_levels as _list_difficulty_levels,
)
from ai_physio_assistant.agent.tools import (
    search_exercises as _search_exercises,
)

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel
    from langgraph.graph.state import CompiledStateGraph

# System prompt for the Physio Assistant agent
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
    "gemini-pro": "gemini-1.5-pro",
    "claude": "claude-sonnet-4-0",
    "claude-sonnet": "claude-sonnet-4-0",
    "claude-haiku": "claude-3-5-haiku-latest",
    "gpt-4": "gpt-4o",
    "gpt-4o": "gpt-4o",
    "gpt-4o-mini": "gpt-4o-mini",
}


# Define tools using LangChain's @tool decorator
# The docstrings are used as tool descriptions for the LLM


@tool
def list_body_regions() -> str:
    """List all available body regions that exercises can target.

    Use this tool to see what body regions are available for filtering exercises.
    Returns a formatted list of body regions like neck, shoulder, lower_back, etc.
    """
    return _list_body_regions()


@tool
def list_difficulty_levels() -> str:
    """List all available difficulty levels for exercises.

    Returns beginner, intermediate, and advanced difficulty options.
    """
    return _list_difficulty_levels()


@tool
def search_exercises(
    body_region: str | None = None,
    condition: str | None = None,
    difficulty: str | None = None,
    therapeutic_goal: str | None = None,
    equipment: str | None = None,
    max_results: int = 10,
) -> str:
    """Search for exercises based on various criteria.

    Use this tool to find exercises that match specific requirements.
    All filter parameters are optional and can be combined.

    Args:
        body_region: Filter by body region (e.g., 'neck', 'shoulder', 'lower_back').
        condition: Filter by medical condition (e.g., 'neck_pain', 'sciatica').
        difficulty: Filter by difficulty level ('beginner', 'intermediate', 'advanced').
        therapeutic_goal: Filter by goal (e.g., 'reduce_pain', 'improve_mobility').
        equipment: Filter by required equipment (e.g., 'none', 'resistance_band').
        max_results: Maximum number of results to return (default 10).

    Returns:
        A formatted string listing matching exercises with their key details.
    """
    return _search_exercises(
        body_region=body_region,
        condition=condition,
        difficulty=difficulty,
        therapeutic_goal=therapeutic_goal,
        equipment=equipment,
        max_results=max_results,
    )


@tool
def get_exercise_details(exercise_id: str) -> str:
    """Get complete details for a specific exercise.

    Use this tool to get full information about an exercise including
    instructions, common mistakes, contraindications, and parameters.

    Args:
        exercise_id: The unique ID of the exercise (e.g., 'chin_tuck', 'cat_cow_stretch').

    Returns:
        Formatted details of the exercise or an error message if not found.
    """
    return _get_exercise_details(exercise_id)


@tool
def list_all_exercises() -> str:
    """List all available exercises in the database.

    Returns a summary of all exercises organized by body region.
    Use this to see the complete exercise library.
    """
    return _list_all_exercises()


@tool
def get_exercises_for_condition(condition: str) -> str:
    """Find all exercises recommended for a specific medical condition.

    Use this when a patient presents with a particular diagnosis or symptom.

    Args:
        condition: The medical condition (e.g., 'neck_pain', 'sciatica',
                  'rotator_cuff', 'plantar_fasciitis').

    Returns:
        A list of exercises that help with the specified condition.
    """
    return _get_exercises_for_condition(condition)


@tool
def create_routine_draft(
    patient_name: str,
    diagnosis: str,
    therapeutic_goals: list[str],
    exercise_ids: list[str],
    frequency: str = "once daily",
    general_notes: str | None = None,
) -> str:
    """Create a draft routine for a patient with selected exercises.

    This creates a structured routine that can be reviewed and delivered to the patient.

    Args:
        patient_name: The patient's name for the handout.
        diagnosis: Primary diagnosis or reason for treatment.
        therapeutic_goals: List of goals (e.g., ['reduce pain', 'improve mobility']).
        exercise_ids: List of exercise IDs to include in the routine.
        frequency: How often to perform (e.g., 'once daily', 'twice daily').
        general_notes: Optional notes or context for the patient.

    Returns:
        A formatted routine draft that can be reviewed by the physiotherapist.
    """
    return _create_routine_draft(
        patient_name=patient_name,
        diagnosis=diagnosis,
        therapeutic_goals=therapeutic_goals,
        exercise_ids=exercise_ids,
        frequency=frequency,
        general_notes=general_notes,
    )


# List of all tools for the agent
AGENT_TOOLS = [
    list_body_regions,
    list_difficulty_levels,
    search_exercises,
    get_exercise_details,
    list_all_exercises,
    get_exercises_for_condition,
    create_routine_draft,
]


def get_llm(model: str) -> BaseChatModel:
    """
    Get the appropriate LLM instance based on the model string.

    Args:
        model: Model identifier (e.g., 'gpt-4o', 'claude-sonnet-4-0', 'gemini-2.0-flash')

    Returns:
        A LangChain chat model instance.
    """
    # Resolve alias
    resolved = MODEL_ALIASES.get(model, model)

    # Determine provider and create appropriate LLM
    if resolved.startswith("gpt-") or resolved.startswith("o1"):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=resolved)
    elif resolved.startswith("claude-"):
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=resolved)
    elif resolved.startswith("gemini-"):
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=resolved)
    else:
        # Default to OpenAI for unknown models
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=resolved)


def create_physio_agent(model: str = "gemini-2.0-flash") -> CompiledStateGraph:
    """
    Create and return the Physio Assistant agent.

    Args:
        model: The model to use. Can be a full model string (e.g., 'gpt-4o',
               'claude-sonnet-4-0', 'gemini-2.0-flash') or an alias
               (e.g., 'claude', 'gpt-4', 'gemini').

    Returns:
        A LangGraph CompiledStateGraph configured for physiotherapy assistance.
    """
    # Get the LLM
    llm = get_llm(model)

    # Create the agent using LangGraph's create_react_agent
    # This creates a graph that calls tools in a loop until done
    agent = create_react_agent(
        model=llm,
        tools=AGENT_TOOLS,
        prompt=SystemMessage(content=SYSTEM_PROMPT),
    )

    return agent


def invoke_agent(
    agent: CompiledStateGraph,
    message: str,
    chat_history: list[dict[str, Any]] | None = None,
) -> str:
    """
    Invoke the agent with a message and return the response.

    Args:
        agent: The compiled agent graph.
        message: The user's message.
        chat_history: Optional list of previous messages in the format
                     [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

    Returns:
        The agent's response as a string.
    """
    from langchain_core.messages import AIMessage, HumanMessage

    # Build messages list
    messages = []

    # Add chat history if provided
    if chat_history:
        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

    # Add current message
    messages.append(HumanMessage(content=message))

    # Invoke the agent
    result = agent.invoke({"messages": messages})

    # Extract the final response
    final_messages = result.get("messages", [])
    if final_messages:
        # Get the last AI message
        for msg in reversed(final_messages):
            if isinstance(msg, AIMessage) and msg.content:
                return str(msg.content)

    return "I apologize, but I couldn't generate a response. Please try again."
