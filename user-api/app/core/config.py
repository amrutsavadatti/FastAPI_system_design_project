import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    JWT_API_URL: str = os.getenv("JWT_API_URL", "http://localhost:8001/token")

settings = Settings()