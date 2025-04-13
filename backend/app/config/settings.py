import os
from dotenv import load_dotenv


if os.path.exists(".env"):
    load_dotenv()

class Settings:
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ER Triage Backend"
    
    FHIR_SERVER_URL: str = os.getenv("FHIR_SERVER_URL")
    BASE_URL: str = os.getenv("BASE_URL")
    
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    REDIRECT_URI: str = os.getenv("REDIRECT_URI")

    AUTH_SERVER_URL: str = os.getenv("AUTH_SERVER_URL")
    TOKEN_SERVER_URL: str = os.getenv("TOKEN_SERVER_URL")

    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "https://triage-ml.vercel.app/")

    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()
print(settings.OPENAI_API_KEY)