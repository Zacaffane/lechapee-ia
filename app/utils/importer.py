import requests
import re
import os

def download_book(gutenberg_id):
    url = f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.txt"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Erreur de téléchargement")

def clean_gutenberg_text(text):
    # Supprimer l'en-tête et le pied Project Gutenberg
    start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK"
    start = text.find(start_marker)
    end = text.find(end_marker)

    if start != -1 and end != -1:
        text = text[start + len(start_marker):end]
    return text.strip()

def split_into_chapters(text):
    # Trouver tous les titres de chapitres et les index de début
    matches = list(re.finditer(r'CHAPTER\s+[IVXLC0-9]+', text))
    chapters = []

    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chapter_text = text[start:end].strip()
        chapters.append(chapter_text)

    return chapters


def save_chapters(chapters, book_id):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{book_id}_chapters.txt", "w", encoding="utf-8") as f:
        for chapter in chapters:
            f.write("### CHAPTER ###\n")
            f.write(chapter.strip() + "\n")

if __name__ == "__main__":
    text = download_book(1342)  # Pride and Prejudice
    cleaned = clean_gutenberg_text(text)
    chapters = split_into_chapters(cleaned)
    save_chapters(chapters, "pride")
    print(f"{len(chapters)} chapitres sauvegardés.")
    print("\nEXTRAIT DU CHAPITRE 0 :\n", chapters[0][:300])
