import requests

def search_books_external(query: str, lang="fre", limit=10):
    url = "https://openlibrary.org/search.json"
    params = {
        "q": query,
        "language": lang,
        "has_fulltext": "true",
        "limit": limit
    }
    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for doc in data.get("docs", []):
        if "title" in doc:
            results.append({
                "title": doc["title"],
                "author": doc.get("author_name", ["Auteur inconnu"])[0],
                "openlibrary_id": doc.get("edition_key", [None])[0],  # important pour importer ensuite
                "year": doc.get("first_publish_year")
            })
    return results
