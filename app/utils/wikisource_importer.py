import requests
import re
import os
import json
from app.services.wikisource_ai_service import analyze_wikisource_page

def import_from_wikisource(title, book_id=None):
    url = f"https://fr.wikisource.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "rvprop": "content",
        "titles": title,
        "formatversion": 2
    }

    response = requests.get(url, params=params)
    data = response.json()

    pages = data.get("query", {}).get("pages", [])
    if not pages or "missing" in pages[0]:
        raise Exception("Œuvre non trouvée sur Wikisource.")

    raw_text = pages[0]["revisions"][0]["content"]

    print("📄 Analyse IA de la page Wikisource en cours...")
    ai_result = analyze_wikisource_page(raw_text)
    print("➡️ Analyse de la structure par l'IA :\n", ai_result)

    return ai_result  # pour l'afficher aussi côté API si besoin

def import_from_wikisource_2(title, book_id=None):
    url = f"https://fr.wikisource.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "rvprop": "content",
        "titles": title,
        "formatversion": 2
    }

    response = requests.get(url, params=params)
    data = response.json()

    pages = data.get("query", {}).get("pages", [])
    if not pages or "missing" in pages[0]:
        raise Exception("Œuvre non trouvée sur Wikisource.")

    raw_text = pages[0]["revisions"][0]["content"]

    # Nettoyage de base du texte (très simplifié, on pourra l'améliorer)
    clean_text = re.sub(r"\{\{[^\}]+\}\}", "", raw_text)  # Supprimer les modèles {{...}}
    clean_text = re.sub(r"<[^>]+>", "", clean_text)  # Supprimer les balises <...>
    clean_text = re.sub(r"==+.*?==+", "", clean_text)  # Supprimer les titres
    clean_text = re.sub(r"\n{2,}", "\n\n", clean_text)  # Réduire les espaces

    # Découpe en pseudo-chapitres par blocs de 1000 mots (simple MVP)
    words = clean_text.split()
    chunks = [' '.join(words[i:i + 1000]) for i in range(0, len(words), 1000)]

    book_id = book_id or title.lower().replace(" ", "_")

    os.makedirs("data", exist_ok=True)
    with open(f"data/{book_id}_chapters.txt", "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write("### CHAPTER ###\n")
            f.write(chunk.strip() + "\n")

    # Mise à jour du catalog.json
    catalog_path = "data/catalog.json"
    if os.path.exists(catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
    else:
        catalog = []

    catalog.append({
        "id": book_id,
        "title": title,
        "author": "Auteur inconnu (Wikisource)",
        "source": "Wikisource"
    })

    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    return {"id": book_id, "chapters": len(chunks)}
