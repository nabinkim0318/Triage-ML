import os
import argparse
from dotenv import load_dotenv, set_key

def setup_test_environment():
    """Setup test environment variables"""
    load_dotenv()
    
    env_file = ".env"
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write("# ER Triage API Environment Variables\n")
    
    env_vars = {
        "FHIR_SERVER_URL": os.getenv("FHIR_SERVER_URL", "https://api.logicahealth.org/ERSANDBOX/data"),
        "CLIENT_ID": os.getenv("CLIENT_ID", "client_id"),
        "CLIENT_SECRET": os.getenv("CLIENT_SECRET", ""),
        "REDIRECT_URI": os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback"),
        "AUTH_SERVER_URL": os.getenv("AUTH_SERVER_URL", "https://auth.logicahealth.org/"),
        "SCOPE": os.getenv("SCOPE", "launch patient/*.read openid profile"),
        "API_V1_STR": os.getenv("API_V1_STR", "/api/v1"),
        "PROJECT_NAME": os.getenv("PROJECT_NAME", "ER Triage API"),
        "DEBUG": os.getenv("DEBUG", "true"),
        "TOKEN_CACHE_EXPIRY": os.getenv("TOKEN_CACHE_EXPIRY", "3500"),
    }
    
    for key, default_value in env_vars.items():
        if not os.getenv(key):
            set_key(env_file, key, default_value)
            print(f"Set {key} to default value")
    
    print("Test environment setup complete")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup test environment for ER Triage API")
    
    args = parser.parse_args()
    setup_test_environment()