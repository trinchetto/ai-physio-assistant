"""
Chat panel component for AI conversation.
"""

from __future__ import annotations

import os

import streamlit as st

from ai_physio_assistant.agent.agent import (
    MODEL_ALIASES,
    create_physio_agent,
    invoke_agent,
)
from ai_physio_assistant.frontend.state import (
    ChatState,
    add_chat_message,
    clear_chat_history,
    get_chat_history_for_agent,
)


def render_chat_panel() -> None:
    """Render the chat panel page."""
    st.header("Chat with AI Assistant")

    chat_state: ChatState = st.session_state.chat

    # Sidebar settings
    with st.sidebar:
        st.subheader("Model Settings")

        # Model selection
        model_options = list(MODEL_ALIASES.keys())
        current_index = (
            model_options.index(chat_state.model_name)
            if chat_state.model_name in model_options
            else 0
        )

        selected_model = st.selectbox(
            "AI Model",
            options=model_options,
            index=current_index,
            key="model_selector",
            help="Select the AI model to use for conversation",
        )

        # Update model if changed (will recreate agent)
        if selected_model != chat_state.model_name:
            chat_state.model_name = selected_model
            chat_state.agent = None  # Force recreation

        st.divider()

        # Chat controls
        if st.button("Clear Chat", use_container_width=True):
            clear_chat_history()
            st.rerun()

        # API key status
        st.divider()
        st.subheader("API Key Status")
        _render_api_key_status()

    # Check for API key before allowing chat
    if not _has_required_api_key(chat_state.model_name):
        _render_api_key_warning(chat_state.model_name)
        return

    # Display chat messages
    _render_chat_messages()

    # Chat input
    if prompt := st.chat_input("Type your message...", disabled=chat_state.is_processing):
        _handle_user_message(prompt)


def _render_chat_messages() -> None:
    """Render all chat messages."""
    chat_state: ChatState = st.session_state.chat

    # Show welcome message if no messages
    if not chat_state.messages:
        with st.chat_message("assistant"):
            st.markdown(
                """Hello! I'm your AI assistant for creating exercise routines.

I can help you:
- **Find exercises** for specific conditions or body regions
- **Get detailed information** about any exercise
- **Create routine drafts** for your patients

How can I help you today?"""
            )
        return

    # Render message history
    for msg in chat_state.messages:
        with st.chat_message(msg.role):
            st.markdown(msg.content)


def _handle_user_message(prompt: str) -> None:
    """Handle a new user message."""
    chat_state: ChatState = st.session_state.chat

    # Add user message
    add_chat_message("user", prompt)

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show processing state
    chat_state.is_processing = True

    # Get or create agent
    if chat_state.agent is None:
        chat_state.agent = create_physio_agent(model=chat_state.model_name)

    # Invoke agent and get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                history = get_chat_history_for_agent()
                # Remove the last message (current prompt) since we pass it separately
                history = history[:-1] if history else []

                response = invoke_agent(
                    agent=chat_state.agent,
                    message=prompt,
                    chat_history=history,
                )

                # Add assistant response
                add_chat_message("assistant", response)
                st.markdown(response)

            except Exception as e:
                error_msg = f"An error occurred: {e!s}"
                st.error(error_msg)
                add_chat_message("assistant", f"I apologize, but {error_msg}")

    chat_state.is_processing = False
    st.rerun()


def _render_api_key_status() -> None:
    """Render API key status indicators."""
    keys = {
        "Google (Gemini)": "GOOGLE_API_KEY",
        "OpenAI": "OPENAI_API_KEY",
        "Anthropic": "ANTHROPIC_API_KEY",
    }

    for name, env_var in keys.items():
        if os.environ.get(env_var):
            st.success(f"{name}: Configured")
        else:
            st.warning(f"{name}: Not set")


def _has_required_api_key(model: str) -> bool:
    """Check if the required API key is set for the selected model."""
    resolved = MODEL_ALIASES.get(model, model)

    if resolved.startswith("gemini"):
        return bool(os.environ.get("GOOGLE_API_KEY"))
    elif resolved.startswith("gpt") or resolved.startswith("o1"):
        return bool(os.environ.get("OPENAI_API_KEY"))
    elif resolved.startswith("claude"):
        return bool(os.environ.get("ANTHROPIC_API_KEY"))

    return True  # Unknown model, let it try


def _render_api_key_warning(model: str) -> None:
    """Render a warning about missing API key."""
    resolved = MODEL_ALIASES.get(model, model)

    if resolved.startswith("gemini"):
        key_name = "GOOGLE_API_KEY"
        provider = "Google AI"
    elif resolved.startswith("gpt") or resolved.startswith("o1"):
        key_name = "OPENAI_API_KEY"
        provider = "OpenAI"
    elif resolved.startswith("claude"):
        key_name = "ANTHROPIC_API_KEY"
        provider = "Anthropic"
    else:
        key_name = "API_KEY"
        provider = "the selected provider"

    st.warning(
        f"""
        **API Key Required**

        To use {model}, you need to set the `{key_name}` environment variable.

        ```bash
        export {key_name}="your-api-key-here"
        ```

        Get your API key from {provider}'s developer console.

        Alternatively, select a different model in the sidebar.
        """
    )
