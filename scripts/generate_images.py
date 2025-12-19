#!/usr/bin/env python3
"""
Convenience wrapper for running image generation without installing the package.

For production use, install the package and use:
    physio-generate-images --help

Or:
    python -m ai_physio_assistant.cli.generate_images --help
"""

import sys
from pathlib import Path

# Add src to path for development use
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from ai_physio_assistant.cli.generate_images import main

if __name__ == "__main__":
    sys.exit(main())
