import os

class Config:
    DEBUG = os.environ.get("FLASK_DEBUG", True)
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")