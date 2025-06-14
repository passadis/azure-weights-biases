import requests
from bs4 import BeautifulSoup
import json
import uuid
from urllib.parse import urlparse
from pathlib import Path

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=' ', strip=True)
        title = soup.title.string.strip() if soup.title else "Untitled"
        return title, text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, ""

def chunk_text(text, max_words=100):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def generate_document_chunks(url, category="General"):
    title, full_text = extract_text_from_url(url)
    if not full_text:
        return []

    chunks = chunk_text(full_text)
    parsed = urlparse(url)
    slug = Path(parsed.path).stem or "blog"

    return [
        {
            "id": f"{slug}-{i+1}",
            "content": chunk,
            "category": category,
            "source": url
        }
        for i, chunk in enumerate(chunks)
    ]

if __name__ == "__main__":
    output_file = "blog_documents.json"
    all_docs = []

    # Load existing data if file exists
    if Path(output_file).exists():
        with open(output_file, "r", encoding="utf-8") as f:
            try:
                all_docs = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Warning: JSON file was invalid or empty.")

    # Add new content
    urls = [
        "https://"
    ]
    for url in urls:
        all_docs.extend(generate_document_chunks(url, category="Azure"))

    # Save combined output
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_docs, f, ensure_ascii=False, indent=2)

    print(f"✅ Total documents saved to {output_file}: {len(all_docs)}")

