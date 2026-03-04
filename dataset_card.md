# Карточка датасета

**1. Краткое название / полное описание**  
Books to Scrape 1000 — датасет из 1000 книг (заголовки, цены, рейтинги, описания).

**2. Источник**  
http://books.toscrape.com (учебный sandbox, специально создан для практики scraping).

**3. Дата сбора**  
04 марта 2026 (при повторном запуске будет актуальная).

**4. Структура**  
- `data/raw_pages/` — 1050+ сохранённых HTML-страниц (raw)  
- `data/extracted/books.json` — извлечённый датасет (1000 записей)  

**5. Количество объектов**  
1000 книг.  
Язык: английский.  
Пропуски: отсутствуют (все поля заполнены).  
Длина текста (description): мин. ~150 символов, макс. ~1200 символов.  


**6. Описание полей**  
- `url` — ссылка на страницу книги  
- `title` — название книги  
- `price` — цена (£)  
- `rating` — рейтинг (One/Two/Three/Four/Five или текст)  
- `availability` — наличие на складе  
- `description` — описание книги (текст для кластеризации)

**7. Примеры**  
```json
{
  "title": "A Light in the Attic",
  "price": "£51.77",
  "rating": "Zero stars",
  "availability": "In stock (22 available)",
  "description": "It's hard to imagine a world without A Light in the Attic..."
}
```

**8. Ключевые слова**  
books, literature, prices, ratings, product descriptions, web scraping, dataset for clustering

**9. Лицензия (бонус)**  
Данные полностью вымышленные, созданы специально для обучения scraping. На сайте написано "We love being scraped!". Разрешено свободное использование в учебных целях (не нарушает авторские права).
