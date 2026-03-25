#!/usr/bin/env python3
"""
Анализ датасета книг с использованием регулярных выражений
"""

import json
import re
from collections import defaultdict

def load_dataset(file_path):
    """Загрузка JSON датасета"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_dataset_with_regex(data):
    """Анализ датасета с помощью регулярных выражений"""
    
    results = {
        'total_books': len(data),
        'patterns_found': defaultdict(list)
    }
    
    # 1. Регулярное выражение для поиска цен в фунтах стерлингов
    price_pattern = r'Â£\d+\.\d{2}'
    price_regex = re.compile(price_pattern)
    
    # 2. Регулярное выражение для поиска URL адресов книг
    url_pattern = r'http://books\.toscrape\.com/catalogue/[^/]+_\d+/'
    url_regex = re.compile(url_pattern)
    
    # 3. Регулярное выражение для поиска рейтингов (One, Two, Three, Four, Five)
    rating_pattern = r'\b(One|Two|Three|Four|Five)\b'
    rating_regex = re.compile(rating_pattern)
    
    # 4. Регулярное выражение для поиска информации о доступности
    availability_pattern = r'In stock \(\d+ available\)|Out of stock'
    availability_regex = re.compile(availability_pattern)
    
    # 5. Регулярное выражение для поиска названий издательств (в кавычках)
    publisher_pattern = r'"([^"]+)"\s*--'
    publisher_regex = re.compile(publisher_pattern)
    
    # 6. Регулярное выражение для поиска ObjectId
    object_id_pattern = r'\$oid":\s*"([a-f0-9]{24})"'
    object_id_regex = re.compile(object_id_pattern)
    
    # 7. Регулярное выражение для поиска годов в описаниях
    year_pattern = r'\b(19|20)\d{2}\b'
    year_regex = re.compile(year_pattern)
    
    # 8. Регулярное выражение для поиска имен авторов (после "by" в описаниях)
    author_pattern = r'\bby\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    author_regex = re.compile(author_pattern)
    
    print("=== АНАЛИЗ ДАТАСЕТА КНИГ С ПОМОЩЬЮ РЕГУЛЯРНЫХ ВЫРАЖЕНИЙ ===\n")
    
    for i, book in enumerate(data):
        book_text = json.dumps(book, ensure_ascii=False)
        
        # Поиск цен
        prices = price_regex.findall(book_text)
        if prices:
            results['patterns_found']['prices'].extend(prices)
        
        # Поиск URL
        urls = url_regex.findall(book_text)
        if urls:
            results['patterns_found']['urls'].extend(urls)
        
        # Поиск рейтингов
        ratings = rating_regex.findall(book_text)
        if ratings:
            results['patterns_found']['ratings'].extend(ratings)
        
        # Поиск информации о доступности
        availability = availability_regex.findall(book_text)
        if availability:
            results['patterns_found']['availability'].extend(availability)
        
        # Поиск издательств
        publishers = publisher_regex.findall(book_text)
        if publishers:
            results['patterns_found']['publishers'].extend(publishers)
        
        # Поиск ObjectId
        object_ids = object_id_regex.findall(book_text)
        if object_ids:
            results['patterns_found']['object_ids'].extend(object_ids)
        
        # Поиск годов
        description = book.get('description', '') or ''
        years = year_regex.findall(description)
        if years:
            results['patterns_found']['years'].extend(years)
        
        # Поиск авторов
        authors = author_regex.findall(description)
        if authors:
            results['patterns_found']['authors'].extend(authors)
    
    return results

def print_analysis_results(results):
    """Вывод результатов анализа"""
    
    print(f"Всего книг в датасете: {results['total_books']}\n")
    
    print("1. ПОИСК ЦЕН В ФУНТАХ СТЕРЛИНГОВ")
    print("Регулярное выражение: r'Â£\\d+\\.\\d{2}'")
    print("Описание: Ищет цены в формате Â£XX.XX")
    prices = results['patterns_found']['prices']
    print(f"Найдено: {len(prices)} цен")
    if prices:
        print(f"Примеры: {prices[:5]}")
        print(f"Диапазон цен: от {min(prices)} до {max(prices)}")
    print()
    
    print("2. ПОИСК URL АДРЕСОВ КНИГ")
    print("Регулярное выражение: r'http://books\\.toscrape\\.com/catalogue/[^/]+_\\d+/'")
    print("Описание: Ищет URL адреса книг на сайте")
    urls = results['patterns_found']['urls']
    print(f"Найдено: {len(urls)} URL")
    if urls:
        print(f"Пример: {urls[0]}")
    print()
    
    print("3. ПОИСК РЕЙТИНГОВ")
    print("Регулярное выражение: r'\\b(One|Two|Three|Four|Five)\\b'")
    print("Описание: Ищет текстовые рейтинги от One до Five")
    ratings = results['patterns_found']['ratings']
    print(f"Найдено: {len(ratings)} рейтингов")
    if ratings:
        rating_counts = defaultdict(int)
        for rating in ratings:
            rating_counts[rating] += 1
        print("Распределение рейтингов:")
        for rating, count in sorted(rating_counts.items()):
            print(f"  {rating}: {count}")
    print()
    
    print("4. ПОИСК ИНФОРМАЦИИ О ДОСТУПНОСТИ")
    print("Регулярное выражение: r'In stock \\(\\d+ available\\)|Out of stock'")
    print("Описание: Ищет статус доступности книг")
    availability = results['patterns_found']['availability']
    print(f"Найдено: {len(availability)} статусов")
    if availability:
        avail_counts = defaultdict(int)
        for status in availability:
            avail_counts[status] += 1
        print("Распределение статусов:")
        for status, count in avail_counts.items():
            print(f"  {status}: {count}")
    print()
    
    print("5. ПОИСК ИЗДАТЕЛЬСТВ И ЖУРНАЛОВ")
    print("Регулярное выражение: r'\"([^\"]+)\"\\s*--'")
    print("Описание: Ищет названия издательств в кавычках перед дефисом")
    publishers = results['patterns_found']['publishers']
    print(f"Найдено: {len(publishers)} издательств")
    if publishers:
        unique_publishers = list(set(publishers))
        print(f"Уникальных издательств: {len(unique_publishers)}")
        print(f"Примеры: {unique_publishers[:5]}")
    print()
    
    print("6. ПОИСК OBJECTID")
    print("Регулярное выражение: r'\\$oid\":\\s*\"([a-f0-9]{24})\"'")
    print("Описание: Ищет MongoDB ObjectId в формате 24-значной шестнадцатеричной строки")
    object_ids = results['patterns_found']['object_ids']
    print(f"Найдено: {len(object_ids)} ObjectId")
    if object_ids:
        print(f"Пример: {object_ids[0]}")
    print()
    
    print("7. ПОИСК ГОДОВ В ОПИСАНИЯХ")
    print("Регулярное выражение: r'\\b(19|20)\\d{2}\\b'")
    print("Описание: Ищет годы с 1900 по 2099")
    years = results['patterns_found']['years']
    print(f"Найдено: {len(years)} лет")
    if years:
        unique_years = sorted(set(years))
        print(f"Диапазон годов: от {min(unique_years)} до {max(unique_years)}")
        print(f"Примеры: {unique_years[:10]}")
    print()
    
    print("8. ПОИСК ИМЕН АВТОРОВ")
    print("Регулярное выражение: r'\\bby\\s+([A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*)'")
    print("Описание: Ищет имена авторов после слова 'by'")
    authors = results['patterns_found']['authors']
    print(f"Найдено: {len(authors)} имен авторов")
    if authors:
        unique_authors = list(set(authors))
        print(f"Уникальных авторов: {len(unique_authors)}")
        print(f"Примеры: {unique_authors[:5]}")
    print()

def main():
    """Главная функция"""
    try:
        # Загрузка датасета
        print("Загрузка датасета...")
        data = load_dataset('books_scraper.extracted_books.json')
        
        # Анализ с помощью регулярных выражений
        print("Анализ данных с помощью регулярных выражений...")
        results = analyze_dataset_with_regex(data)
        
        # Вывод результатов
        print_analysis_results(results)
        
        # Сохранение результатов в файл
        with open('regex_analysis_results.txt', 'w', encoding='utf-8') as f:
            f.write("РЕЗУЛЬТАТЫ АНАЛИЗА ДАТАСЕТА КНИГ С ПОМОЩЬЮ РЕГУЛЯРНЫХ ВЫРАЖЕНИЙ\n\n")
            f.write(f"Всего книг: {results['total_books']}\n\n")
            
            for pattern_type, matches in results['patterns_found'].items():
                f.write(f"{pattern_type.upper()}: {len(matches)} совпадений\n")
                if matches:
                    unique_matches = list(set(matches))
                    f.write(f"Уникальных: {len(unique_matches)}\n")
                    f.write(f"Примеры: {unique_matches[:10]}\n")
                f.write("\n")
        
        print("Результаты сохранены в файл 'regex_analysis_results.txt'")
        
    except FileNotFoundError:
        print("Ошибка: Файл 'books_scraper.extracted_books.json' не найден")
    except json.JSONDecodeError:
        print("Ошибка: Некорректный формат JSON файла")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()
