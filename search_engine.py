from transformers import pipeline
from elasticsearch import Elasticsearch

# Класс для поиска
class CustomSearcher:
    def __init__(self):
        self.es = Elasticsearch(hosts=["http://localhost:9200"])
        self.question_answering_pipe = pipeline("question-answering", model="deepset/roberta-base-squad2")

    def search(self, query):
        """
        Ищем информацию по всему содержанию страницы, связанной с конкретным URL
        """
        search_body = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"content": query}}
                    ]
                }
            }
        }

        # Выполняем поиск
        res = self.es.search(index="fa_university", body=search_body)
        hits = res['hits']['hits']
        return [(hit['_source']['url'], hit['_source']['content']) for hit in hits[:3]]

# Демонстрация работы поисковика
if __name__ == "__main__":
    searcher = CustomSearcher()
    query = input("Введите ваш запрос: ")
    results = searcher.search(query)
    if len(results) > 0:
        print("Найденные результаты:")
        for url, content in results:
            print(f"Ссылка: {url}, Контент: {content[:100]}...")
    else:
        print("По данному запросу ничего не найдено.")