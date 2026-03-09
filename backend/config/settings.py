import os
from dotenv import load_dotenv

load_dotenv()

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Image Generation
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")  # Stable Diffusion

# Video Generation
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")

# Voice
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# YouTube
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Google Analytics
GA4_PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")

# App
ASSETS_PATH = os.getenv("ASSETS_PATH", "../assets")
APPROVAL_REQUIRED = True  # Nunca publicar sem aprovação humana
