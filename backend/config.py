import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI-Powered Multi-Agent Software Engineering Workspace"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    PROJECTS_DIR: str = os.getenv("PROJECTS_DIR", "backend/projects")

settings = Settings()
