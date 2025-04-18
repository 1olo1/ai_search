from elasticsearch import Elasticsearch
import json
import sys

# Настройки подключения к локальному Elasticsearch
es = Elasticsearch(hosts=["http://localhost:9200"])

# Структура индекса с поддержкой русского языка
mapping = {
    "settings": {
        "analysis": {
            "analyzer": {
                "ru_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "russian_stop", "russian_keywords", "russian_stemmer"]
                }
            },
            "filter": {
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_keywords": {
                    "type": "keyword_marker",
                    "keywords": []  # Ключевые слова, если нужны
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "url": {"type": "keyword"},
            "content": {"type": "text", "analyzer": "ru_analyzer"}
        }
    }
}

# Чтение данных из файла и заполнение индекса
def index_data(file_path):
    pages = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('_ЭТО_РАЗДЕЛИТЕЛЬ_', maxsplit=1)
            if len(parts) != 2:
                continue
            url, content = parts
            pages.append({"url": url, "content": content})

    # Создание нового индекса
    index_name = "fa_university"
    try:
        es.indices.delete(index=index_name)
    except Exception:
        pass

    es.indices.create(index=index_name, body=mapping)

    # Занесение данных в индекс
    for idx, page in enumerate(pages):
        es.index(index=index_name, id=idx, document={
            "url": page["url"],
            "content": page["content"]
        })

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: python elasticsearch_indexer.py путь/до/scrapped_data.txt")
        exit(1)

    file_path = sys.argv[1]
    index_data(file_path)