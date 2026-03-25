# Books to Scrape — учебный скрапер с MongoDB

Скачивает 1050+ страниц (1000 детальных страниц книг + страницы каталога) и сохраняет данные в MongoDB.

## Установка и настройка

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка MongoDB

**Локальная установка:**
- Скачайте и установите [MongoDB Community Server](https://www.mongodb.com/try/download/community)
- Запустите MongoDB сервер (по умолчанию на `mongodb://localhost:27017/`)

### 3. Запуск скрапера
```bash
python scraper.py          # собирает ссылки + скачивает (можно прерывать и продолжать)
```

### 4. Парсинг данных
```bash
python parser.py           # извлекает данные → MongoDB коллекция 'extracted_books'
```

## Структура данных в MongoDB

### Коллекция `scraping_links`
Хранит информацию о ссылках и статусе их обработки:
- `url`: URL страницы
- `status`: pending/done/error
- `html_file`: имя файла с сохраненной HTML страницей

### Коллекция `extracted_books`
Хранит извлеченные данные о книгах:
- `url`: URL книги
- `title`: название
- `price`: цена
- `rating`: рейтинг
- `availability`: наличие
- `description`: описание

## Резервное копирование

Данные также сохраняются в JSON файлы:
- `data/extracted/books.json` - извлеченные данные о книгах
- HTML страницы хранятся в `data/raw_pages/`

Данные используются только в учебных целях.
