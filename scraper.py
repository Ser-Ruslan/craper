import os
import json
import time
import hashlib
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com"
DATA_DIR = "data"
LINKS_FILE = os.path.join(DATA_DIR, "raw_links.json")
PAGES_DIR = os.path.join(DATA_DIR, "raw_pages")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/133.0 Safari/537.36"
}

os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LINKS_FILE), exist_ok=True)

def get_filename(url: str) -> str:
    return hashlib.md5(url.encode("utf-8")).hexdigest() + ".html"

def load_links():
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_links(links):
    with open(LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)

def discover_links():
    print("Запуск обнаружения ссылок (первый запуск)...")
    links = []
    visited_urls = set()
    queue = ["http://books.toscrape.com/catalogue/page-1.html"]
    page_count = 0

    while queue:
        url = queue.pop(0)
        if url in visited_urls:
            continue
        visited_urls.add(url)
        page_count += 1
        print(f"Обработка страницы {page_count}: {url}")

        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            # Собираем ссылки на книги
            books_found = 0
            for h3 in soup.find_all("h3"):
                a = h3.find("a")
                if a and "href" in a.attrs:
                    book_url = urljoin(url, a["href"])  # Используем текущий URL для правильного присоединения
                    if book_url not in visited_urls:
                        links.append({"url": book_url, "status": "pending", "html_file": None})
                        visited_urls.add(book_url)
                        books_found += 1

            print(f"  Найдено книг: {books_found}")

            # Следующая страница каталога
            next_li = soup.find("li", class_="next")
            if next_li:
                next_a = next_li.find("a")
                if next_a and "href" in next_a.attrs:
                    next_url = urljoin(url, next_a["href"])
                    if next_url not in visited_urls:
                        queue.append(next_url)
                        links.append({"url": next_url, "status": "pending", "html_file": None})
                        print(f"  Добавлена следующая страница: {next_url}")

            time.sleep(0.5)
        except Exception as e:
            print(f"Ошибка при обходе {url}: {e}")

    print(f" Найдено {len(links)} ссылок (1000+ книг + страницы каталога)")
    return links

def main_scraper():
    links = load_links()
    if not links:
        links = discover_links()
        save_links(links)

    pending = [lnk for lnk in links if lnk["status"] == "pending"]
    print(f" Скачивание {len(pending)} страниц (можно прерывать и продолжать)...")

    for item in pending:
        url = item["url"]
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()

            filename = get_filename(url)
            filepath = os.path.join(PAGES_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(r.text)

            item["status"] = "done"
            item["html_file"] = filename
            print(f"✔ Скачано: {url}")
        except Exception as e:
            item["status"] = "error"
            print(f"✖ Ошибка: {url} — {e}")

        save_links(links)          # сохраняем прогресс после каждой страницы
        time.sleep(0.5)            

    print(" Скачивание завершено!")

if __name__ == "__main__":
    main_scraper()
