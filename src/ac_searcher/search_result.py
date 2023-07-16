from datetime import datetime
from typing import List


# Класс, для описания результата поиска.
# Содержит в себе контент анализ, фотографию по наличии, регион, актуальность
class SearchResult:

    def __init__(self, SearchResultDB=None, id="", url="", photo="", region="", relevance="", content_analysis=""):
        if SearchResultDB is not None:
            self.id = str(SearchResultDB.id)
            self.url = SearchResultDB.url
            self.photo = SearchResultDB.photo
            self.region = SearchResultDB.region
            self.relevance = SearchResultDB.relevance
            self.content_analysis = SearchResultDB.content_analysis
        else:
            self.id = id
            self.url = url
            self.photo = photo
            self.region = region
            self.relevance = relevance
            self.content_analysis = content_analysis

    def __repr__(self):
        return f"Listing(id={self.id}, url={self.url}, photo={self.photo}, region={self.region}, " \
               f"relevance={self.relevance}, content_analysis={self.content_analysis})"
    
    def set_query_id(self, query_id):
        self.query_id = query_id
    
    def __json__(self):
        return {
            'url': self.url,
            'photo': self.photo,
            'region': self.region,
            'relevance': self.relevance,
            'content_analysis': self.content_analysis,
        }
    
# Класс предсотавляющий возможность анализа ссылок гугл, на их релеватность таким образом чтобы выдать топ лучших ссылок, на основе уже пропаршенных ссылок
class SearchResultAnalyzerInterface:

    # Метод процесс, который на вход получает массив из ссылок и возвращает ссылки уже лучше, но с отбором
    def process(self, parsed_links: List[SearchResult]) -> List[SearchResult]:
        raise NotImplemented


# TODO: Реализовать класс, и имплементировать его инициализацию и настройку в AcSearcher, а также работу
# Класс предсотавляющий возможность анализа ссылок гугл, на их релеватность таким образом чтобы выдать топ лучших ссылок, на основе уже пропаршенных ссылок
class SearchResultAnalyzer(SearchResultAnalyzerInterface):

    # Конструктор, который должен получить на вход количество возвращаемых ссылок, и другие настройки
    # TODO: Реализовать согласно замсылу
    def __init__(self, config):
        pass

    # Метод процесс, который на вход получает массив из ссылок и возвращает ссылки уже лучше, но с отбором
    # TODO: Реализовать метод
    def process(self, parsed_links: List[SearchResult]) -> List[SearchResult]:
        pass
