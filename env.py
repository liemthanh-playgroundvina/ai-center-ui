import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
load_dotenv(".env")


class Settings():
    AUTHORIZATION = os.getenv("AUTHORIZATION")

settings = Settings()
