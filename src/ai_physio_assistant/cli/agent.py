"""
CLI entry point for the AI Physio Assistant agent.

Provides an interactive command-line interface for physiotherapists
to chat with the AI assistant and create exercise routines.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from ai_physio_assistant.agent import create_physio_agent


async def run_agent_loop(model: str = "gemini-2.0-flash") -> None:
    """
    Run the interactive agent conversation loop.

    Args:
        model: The Gemini model to use.
    """
    # Check for API key
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Please set the GOOGLE_API_KEY or GEMINI_API_KEY environment variable.")
        print("\nTo get an API key:")
        print("1. Go to https://aistudio.google.com/apikey")
        print("2. Create a new API key")
        print("3. Set it: export GOOGLE_API_KEY='your-key-here'")
        sys.exit(1)

    # Set the API key for google-genai
    os.environ["GOOGLE_API_KEY"] = api_key

    # Create the agent
    agent = create_physio_agent(model=model)

    # Set up session management
    app_name = "physio_assistant"
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    session_id = f"session_{uuid.uuid4().hex[:8]}"

    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
    )

    print("=" * 60)
    print("AI Physio Assistant")
    print("=" * 60)
    print(f"Model: {model}")
    print("-" * 60)
    print("I'm here to help you create personalized exercise routines.")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("Type 'help' for a list of things I can do.")
    print("=" * 60)
    print()

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

            # Send message to agent
            content = types.Content(
                role="user",
                parts=[types.Part(text=user_input)],
            )

            print("\nAssistant: ", end="", flush=True)

            # Run the agent and collect response
            response_text = ""
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content,
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            response_text += part.text

            if response_text:
                print(response_text)
            else:
                print("(No response generated)")

            print()

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again or type 'quit' to exit.\n")


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="AI Physio Assistant - Interactive exercise routine builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  physio-agent                     # Start with default model
  physio-agent --model gemini-2.5-flash  # Use a specific model

Environment Variables:
  GOOGLE_API_KEY or GEMINI_API_KEY   Your Google AI API key
        """,
    )
    parser.add_argument(
        "--model",
        default="gemini-2.0-flash",
        choices=["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-pro"],
        help="Gemini model to use (default: gemini-2.0-flash)",
    )

    args = parser.parse_args()

    # Run the async agent loop
    asyncio.run(run_agent_loop(model=args.model))


if __name__ == "__main__":
    main()
