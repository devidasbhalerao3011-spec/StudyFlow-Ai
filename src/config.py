
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=False)

APP_NAME = "StudyFlow AI"
AI_PROVIDER = "groq"


def get_setting(name, default=""):
    try:
        secret_value = st.secrets.get(name, "")
    except Exception:
        secret_value = ""

    value = secret_value or os.getenv(name, default)
    return str(value).strip()


GROQ_API_KEY = get_setting("GROQ_API_KEY")
GROQ_MODEL = get_setting(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)
