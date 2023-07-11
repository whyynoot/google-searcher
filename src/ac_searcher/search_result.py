from datetime import datetime
from typing import List

# Класс, для описания результата поиска
# Содержит в себе контент анализ, фотографию по наличии, регион, актуальность
class SearchResult:
    # TODO: add source (откуда пришла ссылка)
    
    # TODO: Разобраться с конструкторами
    def __init__(self, SearchResultDB):
        self.id = SearchResultDB.id
        self.url = SearchResultDB.url
        self.photo = SearchResultDB.photo
        self.region = SearchResultDB.region
        self.relevance = SearchResultDB.relevance
        self.content_analysis = ""

    def __init__(self, url, photo, region, content_analysis):
        self.url = url
        self.photo = photo
        self.region = region
        self.relevance = datetime.now()
        self.content_analysis = content_analysis
    
    def __str__(self) -> str:
        return f'[Search result] URL: {self.url} | Photo: {self.photo} | Region {self.region}'


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