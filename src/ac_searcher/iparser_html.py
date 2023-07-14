from abc import ABC, abstractmethod
from link import Link
from input_interpreter import UserRequest
from search_result import SearchResult


class IHtmlParser(ABC):
    @abstractmethod
    def analyze(self, link: Link, user_request: UserRequest) -> SearchResult:
        pass
