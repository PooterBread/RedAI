"""
Configuration module for RedAI Pen Testing Tool
Compatible with Udoo Key (RP2040/ESP32)
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Database configuration
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "exploits.db"

# AI Model configuration
# Default to OpenAI API, but can be configured for local models
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # Options: openai, anthropic, local
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")  # Lightweight model for Udoo Key

# Local model configuration (for running on device)
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "")
LOCAL_MODEL_TYPE = os.getenv("LOCAL_MODEL_TYPE", "llama")  # llama, mistral, etc.

# Safety and limits
MAX_EXECUTION_TIME = 300  # 5 minutes max per exploit
REQUIRE_CONFIRMATION = True  # Require user confirmation before executing exploits
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Exploit storage
EXPLOITS_DIR = BASE_DIR / "exploits"
LOGS_DIR = BASE_DIR / "logs"

# Create necessary directories
DATABASE_DIR.mkdir(exist_ok=True)
EXPLOITS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)







