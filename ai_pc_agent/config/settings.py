"""
Configuration settings for AI Agent
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DOCUMENTS_DIR = BASE_DIR / "documents"

# Ensure directories exist
DOCUMENTS_DIR.mkdir(exist_ok=True)

# Voice settings
VOICE_RATE = 150
VOICE_VOLUME = 0.9

# Browser settings
HEADLESS_BROWSER = False
BROWSER_TIMEOUT = 10

# Logging
LOG_LEVEL = "INFO"
