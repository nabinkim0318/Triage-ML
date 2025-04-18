import os
from dotenv import load_dotenv
from pathlib import Path
import os

# settings.py
print("📍 현재 경로:", os.getcwd())  # 현재 작업 디렉토리
print("📍 .env 존재?", os.path.exists(".env"))  # .env가 실제로 거기에 있는지


env_path = Path(__file__).resolve().parents[2] / ".env"

print("📍 현재 경로:", os.getcwd())
print("📍 .env 존재?", env_path.exists())
print("📍 .env 경로:", env_path)
load_dotenv(dotenv_path=env_path)

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("❌ OPENAI_API_KEY not set! Check .env or environment.")


class Settings:
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ER Triage Backend"
    
    FHIR_SERVER_URL: str = os.getenv("FHIR_SERVER_URL")
    BASE_URL: str = os.getenv("BASE_URL")
    
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    REDIRECT_URI: str = os.getenv("REDIRECT_URI")

    AUTH_SERVER_URL: str = os.getenv("AUTH_SERVER_URL")
    TOKEN_SERVER_URL: str = os.getenv("TOKEN_SERVER_URL")

    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "https://triage-ml.onrender.com")

    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    def __init__(self):
        print("🔑 OPENAI_API_KEY:", self.OPENAI_API_KEY)
        if not self.OPENAI_API_KEY:
            raise RuntimeError("❌ OPENAI_API_KEY not set! Check .env or environment.")


settings = Settings()
print(settings.OPENAI_API_KEY)