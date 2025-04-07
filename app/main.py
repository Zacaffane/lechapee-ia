from fastapi import FastAPI
from app.api import books

app = FastAPI()
app.include_router(books.router)
