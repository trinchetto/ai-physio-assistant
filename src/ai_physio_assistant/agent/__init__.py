"""
AI Agent module for the Physio Assistant.

This module provides an AI-powered agent that helps physiotherapists
create personalized exercise routines using LangChain.
"""

from __future__ import annotations


def create_physio_agent(model: str = "gemini-2.0-flash"):  # type: ignore[no-untyped-def]
    """
    Create and return the Physio Assistant agent.

    This is a lazy import wrapper to avoid requiring langchain
    until the agent is actually used.

    Args:
        model: The model to use. Supports multiple providers:
               - Gemini: 'gemini-2.0-flash', 'gemini-1.5-pro'
               - OpenAI: 'gpt-4o', 'gpt-4o-mini'
               - Anthropic: 'claude-sonnet-4-0', 'claude-3-5-haiku-latest'
               Also supports aliases: 'claude', 'gpt-4', 'gemini'

    Returns:
        A LangChain AgentExecutor configured for physiotherapy assistance.
    """
    from ai_physio_assistant.agent.agent import create_physio_agent as _create

    return _create(model)


__all__ = ["create_physio_agent"]
