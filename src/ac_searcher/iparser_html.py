from abc import ABC, abstractmethod
from src.ac_searcher.link import Link
from src.ac_searcher.input_interpreter import UserRequest
from src.ac_searcher.search_result import SearchResult


class IHtmlParser(ABC):
    @abstractmethod
    def analyze(self, link: Link, user_request: UserRequest) -> SearchResult:
        pass
