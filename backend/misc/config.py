import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    DEBUG = os.getenv("DEBUG")
    API_KEY = os.getenv("API_KEY")
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
