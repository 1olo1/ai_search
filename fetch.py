import requests
from bs4 import BeautifulSoup
import re
import os

visited_links = set()  # Уже посещённые ссылки
output_file = 'scrapped_data.txt'

def scrape_page(url):
    """Получает содержание страницы"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.find_all(['h1', 'h2', 'h3', 'p'])
        cleaned_texts = '\n'.join(text.get_text(strip=True) for text in texts)
        return cleaned_texts
    except Exception as e:
        print(f"Ошибка при обработке страницы {url}: {e}")
        return ""

def extract_internal_links(soup, base_url):
    """Возвращает все внутренние ссылки текущего раздела"""
    links = []
    for link in soup.findAll('a'):
        href = link.get('href')
        if href and href.startswith('/for-students'):  # Оставляем только нужные ссылки
            full_link = base_url.rstrip('/') + href
            links.append(full_link)
    return links

def crawl_and_save(start_url, base_url):
    """Рекурсивно собирает данные с сайта"""
    global visited_links
    queue = [start_url]

    while queue:
        current_url = queue.pop(0)
        if current_url not in visited_links:
            visited_links.add(current_url)
            print(f"Переходим по ссылке: {current_url}")
            content = scrape_page(current_url)
            with open(output_file, 'a+', encoding='utf-8') as f:
                f.write(f"{current_url}_ЭТО_РАЗДЕЛИТЕЛЬ_{content}\n")

            # Новые ссылки
            new_links = extract_internal_links(BeautifulSoup(requests.get(current_url).content, 'html.parser'), base_url)
            queue.extend(new_links)

if __name__ == '__main__':
    start_url = "https://www.fa.ru/for-students/"
    base_url = "https://www.fa.ru"
    crawl_and_save(start_url, base_url)