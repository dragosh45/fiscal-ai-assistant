import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Încarcă .env.local dacă rulezi local, altfel .env.docker va fi folosit de Docker Compose
if os.getenv("FLASK_ENV") != "docker":
    load_dotenv(".env.local")
else:
    load_dotenv(".env.docker")


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecret')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or \
                              f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    SQLALCHEMY_ECHO = True
