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

def split_into_chapters(text):
    chapters = re.split(r'\n\s*CHAPTER [^\n]+\n', text)
    return chapters[1:] if len(chapters) > 1 else [text]

def save_chapters(chapters, book_id):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{book_id}_chapters.txt", "w", encoding="utf-8") as f:
        for chapter in chapters:
            f.write("### CHAPTER ###\n")
            f.write(chapter.strip() + "\n")

if __name__ == "__main__":
    text = download_book(1342)  # Pride and Prejudice
    chapters = split_into_chapters(text)
    save_chapters(chapters, "pride")
    print(f"{len(chapters)} chapitres sauvegardés.")
