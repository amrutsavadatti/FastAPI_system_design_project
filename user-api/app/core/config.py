import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    JWT_API_URL: str = os.getenv("JWT_API_URL", "http://localhost:8001/token")
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")

settings = Settings()