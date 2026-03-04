import os
import json
from bs4 import BeautifulSoup

LINKS_FILE = "data/raw_links.json"
PAGES_DIR = "data/raw_pages"
EXTRACTED_DIR = "data/extracted"
os.makedirs(EXTRACTED_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(EXTRACTED_DIR, "books.json")

def main_parser():
    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        links = json.load(f)

    dataset = []
    for item in links:
        if item["status"] != "done" or not item.get("html_file"):
            continue
        # Парсим только детальные страницы книг
        if "catalogue" not in item["url"] or "page-" in item["url"]:
            continue

        filepath = os.path.join(PAGES_DIR, item["html_file"])
        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Извлечение полей
        title = soup.find("h1").text.strip() if soup.find("h1") else None

        price_tag = soup.find("p", class_="price_color")
        price = price_tag.text.strip() if price_tag else None

        rating_tag = soup.find("p", class_="star-rating")
        rating = None
        if rating_tag:
            classes = rating_tag.get("class", [])
            rating = classes[1] if len(classes) > 1 else rating_tag.text.strip()

        # наличие на складе
        avail_tag = soup.find("p", class_="instock availability") or \
                    soup.find(string=lambda t: t and "stock" in str(t).lower())
        availability = avail_tag.strip() if avail_tag and isinstance(avail_tag, str) else \
                       (avail_tag.text.strip() if hasattr(avail_tag, "text") else None)

        # описание
        desc_header = soup.find("h2", string="Product Description")
        description = desc_header.find_next("p").text.strip() if desc_header else None

        dataset.append({
            "url": item["url"],
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "description": description
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f" Датасет готов! {len(dataset)} книг сохранено в {OUTPUT_FILE}")

if __name__ == "__main__":
    main_parser()
