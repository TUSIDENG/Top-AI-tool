import os
from pathlib import Path

# Example test script to demonstrate init_chat_model usage without making API calls.
ENV_FILE = Path(__file__).with_suffix(".env")

def write_example_env():
    content = """
# Example .env for OpenAI
MODEL_PROVIDER=openai
MODEL_NAME=gpt-3.5-turbo
MODEL_TEMPERATURE=0.0
# OPENAI_API_KEY=your_api_key_here
"""
    ENV_FILE.write_text(content)


def main():
    # Create an example .env if not present
    if not ENV_FILE.exists():
        write_example_env()
        print(f"Wrote example .env to {ENV_FILE}")

    # Ensure agent-server package path is on sys.path
    import sys
    sys.path.append(str(Path(__file__).parent))

    # Import and run the example init helper
    from agent.core import example_init_and_print

    example_init_and_print()


if __name__ == "__main__":
    main()
# Simple test script to demonstrate init_chat_model without making network calls.
# Usage: python test_init_model.py

import os
from pathlib import Path

# Optional: create a .env file for demonstration if one doesn't exist
env_path = Path(__file__).parent / '.env'
if not env_path.exists():
    with open(env_path, 'w') as f:
        f.write('MODEL_PROVIDER=openai\n')
        f.write('MODEL_NAME=gpt-3.5-turbo\n')
        f.write('MODEL_TEMPERATURE=0\n')
        # Note: not setting OPENAI_API_KEY to avoid accidental network calls

# Now import the module and run the example initializer
from agent.core import example_init_and_print

if __name__ == '__main__':
    example_init_and_print()
