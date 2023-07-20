from abc import ABC, abstractmethod
from src.ac_searcher.search_result import SearchResult
from typing import List


# Интерфейс для работы с базой данных
# Испоьзуется для инициаозиации подключения и работы.
# Применяется шаблон Фасад.
# Реализация варируется взависимсоти от БД.
class IDatabaseManager(ABC):
    # Метод для сохранения результата поиска в базе данных
    @abstractmethod
    def save_search_result(self, search_result: SearchResult) -> bool:
        pass

    # Метод для получения результата поиска из базы данных по идентификатору
    @abstractmethod
    def get_search_result_from_database(self, search_result_id) -> SearchResult:
        pass

    # Метод для получения всех результатов поиска из базы данных
    @abstractmethod
    def get_all_search_results_from_database(self) -> List[SearchResult]:
        pass

    # Метод для создания объекта сессии для взаимодействия с базой данных
    @abstractmethod
    def create_session(self):
        pass

    # Метод для закрытия объекта сессии
    @abstractmethod
    def close_session(self, session):
        pass
