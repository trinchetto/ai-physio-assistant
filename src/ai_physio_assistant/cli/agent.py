"""
CLI entry point for the AI Physio Assistant agent.

Provides an interactive command-line interface for physiotherapists
to chat with the AI assistant and create exercise routines.
"""

from __future__ import annotations

import argparse
import os
import sys

from pydantic_ai.messages import ModelMessage

from ai_physio_assistant.agent import create_physio_agent
from ai_physio_assistant.agent.agent import MODEL_ALIASES


def check_api_keys(model: str) -> bool:
    """
    Check if the required API key is set for the given model.

    Args:
        model: The model string to check.

    Returns:
        True if the API key is set, False otherwise.
    """
    # Determine which API key is needed based on model
    if model.startswith("openai:") or model.startswith("gpt"):
        key_name = "OPENAI_API_KEY"
        key = os.environ.get("OPENAI_API_KEY")
    elif model.startswith("anthropic:") or model.startswith("claude"):
        key_name = "ANTHROPIC_API_KEY"
        key = os.environ.get("ANTHROPIC_API_KEY")
    else:
        # Gemini models
        key_name = "GOOGLE_API_KEY or GEMINI_API_KEY"
        key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if key:
            # Ensure GOOGLE_API_KEY is set for pydantic-ai
            os.environ["GOOGLE_API_KEY"] = key

    if not key:
        print(f"Error: Please set the {key_name} environment variable.")
        print("\nTo get an API key:")
        if "OPENAI" in key_name:
            print("  OpenAI: https://platform.openai.com/api-keys")
        elif "ANTHROPIC" in key_name:
            print("  Anthropic: https://console.anthropic.com/")
        else:
            print("  Google: https://aistudio.google.com/apikey")
        print(f"\nThen set it: export {key_name.split(' or ')[0]}='your-key-here'")
        return False

    return True


def run_agent_loop(model: str = "gemini-2.0-flash") -> None:
    """
    Run the interactive agent conversation loop.

    Args:
        model: The model to use.
    """
    # Resolve model alias
    resolved_model = MODEL_ALIASES.get(model, model)

    # Check for API key
    if not check_api_keys(resolved_model):
        sys.exit(1)

    # Create the agent
    agent = create_physio_agent(model=resolved_model)

    print("=" * 60)
    print("AI Physio Assistant")
    print("=" * 60)
    print(f"Model: {resolved_model}")
    print("-" * 60)
    print("I'm here to help you create personalized exercise routines.")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("Type 'help' for a list of things I can do.")
    print("Type 'clear' to start a new conversation.")
    print("=" * 60)
    print()

    # Message history for multi-turn conversation
    message_history: list[ModelMessage] = []

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle special commands
            if user_input.lower() in ("quit", "exit", "q"):
                print("\nGoodbye! Thank you for using AI Physio Assistant.")
                break

            if user_input.lower() == "clear":
                message_history = []
                print("\n--- Conversation cleared ---\n")
                continue

            if user_input.lower() == "help":
                print("\n--- Help ---")
                print("I can help you with:")
                print("- Search exercises: 'Find exercises for lower back pain'")
                print("- Get exercise details: 'Tell me about chin tuck'")
                print("- List exercises: 'Show all shoulder exercises'")
                print("- Create routines: 'Create a routine for John with neck pain'")
                print("- Filter by difficulty: 'Show beginner hip exercises'")
                print("-" * 40)
                print()
                continue

            # Run the agent
            print("\nAssistant: ", end="", flush=True)

            try:
                result = agent.run_sync(
                    user_input,
                    message_history=message_history,
                )

                # Print the response
                print(result.output)

                # Update message history for next turn
                message_history = result.all_messages()

            except Exception as e:
                error_msg = str(e)
                if "API key" in error_msg or "authentication" in error_msg.lower():
                    print(f"\nAPI Error: {error_msg}")
                    print("Please check your API key and try again.")
                else:
                    print(f"\nError: {error_msg}")

            print()

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except EOFError:
            print("\n\nEnd of input. Goodbye!")
            break


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="AI Physio Assistant - Interactive exercise routine builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  physio-agent                          # Start with default model (Gemini)
  physio-agent --model claude           # Use Claude
  physio-agent --model gpt-4            # Use GPT-4
  physio-agent --model gemini-2.5-pro   # Use Gemini Pro

Model Aliases:
  gemini, gemini-flash  -> gemini-2.0-flash
  gemini-pro            -> gemini-2.5-pro
  claude, claude-sonnet -> anthropic:claude-sonnet-4-0
  gpt-4, gpt-4o         -> openai:gpt-4o
  gpt-4o-mini           -> openai:gpt-4o-mini

Environment Variables:
  GOOGLE_API_KEY or GEMINI_API_KEY   For Gemini models
  OPENAI_API_KEY                     For OpenAI models
  ANTHROPIC_API_KEY                  For Anthropic models
        """,
    )
    parser.add_argument(
        "--model",
        default="gemini-2.0-flash",
        help="Model to use (default: gemini-2.0-flash). See aliases above.",
    )

    args = parser.parse_args()

    # Run the agent loop (synchronous)
    run_agent_loop(model=args.model)


if __name__ == "__main__":
    main()
