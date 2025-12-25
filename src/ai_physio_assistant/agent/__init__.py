"""
AI Agent module for the Physio Assistant.

This module provides an AI-powered agent that helps physiotherapists
create personalized exercise routines using Google ADK.
"""

from __future__ import annotations


def create_physio_agent(model: str = "gemini-2.0-flash"):  # type: ignore[no-untyped-def]
    """
    Create and return the Physio Assistant agent.

    This is a lazy import wrapper to avoid requiring google-adk
    until the agent is actually used.

    Args:
        model: The Gemini model to use.

    Returns:
        An Agent instance configured for physiotherapy assistance.
    """
    from ai_physio_assistant.agent.agent import create_physio_agent as _create

    return _create(model)


__all__ = ["create_physio_agent"]
