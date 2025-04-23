import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    JWT_VALIDATE_URL = os.getenv("JWT_VALIDATE_URL")
    SB_API_KEY = os.getenv("SB_API_KEY")
    SB_URL = os.getenv("SB_URL")

settings = Settings()
