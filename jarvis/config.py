from __future__ import annotations

import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseModel):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    elevenlabs_api_key: str | None = os.getenv("ELEVEN_API_KEY")
    api_key: str | None = os.getenv("JARVIS_API_KEY", "changeme")
    data_dir: str = os.getenv("JARVIS_DATA_DIR", str(Path(__file__).resolve().parents[1] / "data"))
    log_level: str = os.getenv("JARVIS_LOG_LEVEL", "INFO")
    allow_shell: bool = os.getenv("JARVIS_ALLOW_SHELL", "false").lower() in {"1", "true", "yes"}


settings = Settings()

# Ensure required directories exist
Path(settings.data_dir).mkdir(parents=True, exist_ok=True)
Path(settings.data_dir, "logs").mkdir(parents=True, exist_ok=True)
