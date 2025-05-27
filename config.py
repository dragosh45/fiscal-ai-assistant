import os
from dotenv import load_dotenv

# Încarcă .env.local dacă rulezi local, altfel .env.docker va fi folosit de Docker
if os.getenv("FLASK_ENV") != "docker":
    load_dotenv(".env.local")
else:
    load_dotenv(".env.docker")


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecret')

    # Fix pentru Fly.io: transformă postgres:// în postgresql://
    raw_url = os.getenv("DATABASE_URL", "")
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = (
            raw_url or
            os.getenv("SQLALCHEMY_DATABASE_URI") or
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    UPLOAD_FOLDER = 'uploads'
