from fastapi import APIRouter, Query
import os
import json
from app.utils.open_library import search_books_external
from app.utils.wikisource_importer import import_from_wikisource

router = APIRouter()

@router.get("/books")
def list_books():
    try:
        with open("data/catalog.json", "r", encoding="utf-8") as f:
            catalog = json.load(f)
        return {"books": catalog}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/books/{book_id}/chapter/{chapter_number}")
def get_chapter(book_id: str, chapter_number: int):
    try:
        with open(f"data/{book_id}_chapters.txt", "r", encoding="utf-8") as f:
            raw = f.read().split("### CHAPTER ###")
            chapters = [c.strip() for c in raw if c.strip()]  # on filtre les chapitres vides
        return {"chapter": chapters[chapter_number]}
    except IndexError:
        return {"error": f"Chapitre {chapter_number} non trouvé. Il y en a {len(chapters)}."}
    except Exception as e:
        return {"error": str(e)}

@router.get("/books")
def list_books(query: str = Query(None, description="Recherche par titre ou auteur")):
    try:
        with open("data/catalog.json", "r", encoding="utf-8") as f:
            catalog = json.load(f)

        if query:
            query = query.lower()
            results = [
                book for book in catalog
                if query in book["title"].lower() or query in book["author"].lower()
            ]
        else:
            results = catalog

        return {"results": results}

    except Exception as e:
        return {"error": str(e)}

@router.get("/books/{book_id}")
def get_book_details(book_id: str):
    try:
        with open("data/catalog.json", "r", encoding="utf-8") as f:
            catalog = json.load(f)
        for book in catalog:
            if book["id"] == book_id:
                return book
        return {"error": "Livre non trouvé"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/search/external")
def external_search(query: str, lang: str = "fre"):
    try:
        results = search_books_external(query, lang)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

@router.post("/import/wikisource")
def import_wikisource(title: str):
    try:
        result = import_from_wikisource(title)
        return {"message": "Import réussi", "data": result}
    except Exception as e:
        return {"error": str(e)}

