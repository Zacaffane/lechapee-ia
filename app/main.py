from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI
from app.api import books
# Charger le fichier .env depuis le dossier parent
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

app = FastAPI()
app.include_router(books.router)
