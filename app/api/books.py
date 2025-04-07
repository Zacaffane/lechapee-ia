from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/books")
def list_books():
    books = [{"id": f.split("_")[0], "title": "Pride and Prejudice", "author": "Jane Austen"} for f in os.listdir("data") if f.endswith("_chapters.txt")]
    return {"books": books}

@router.get("/books/{book_id}/chapter/{chapter_number}")
def get_chapter(book_id: str, chapter_number: int):
    try:
        with open(f"data/{book_id}_chapters.txt", "r", encoding="utf-8") as f:
            chapters = f.read().split("### CHAPTER ###")
        return {"chapter": chapters[chapter_number].strip()}
    except Exception as e:
        return {"error": str(e)}
