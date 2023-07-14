from urllib.parse import urlencode, urljoin
from link import Link
from input_interpreter import UserRequest
from typing import List, Tuple
import requests
from headers import Headers
from bs4 import BeautifulSoup
import re
from proxy import get_random_proxy

# Searcher интрейфес для обращения с разными поисковыми системами на основе формирования и отправки запроса
class Searcher: 
    def process(self, user_request: UserRequest) -> List[Link]:
        raise NotImplemented
 
# SearcherSettings настройки необходимые для работы сеарчера
class SearcherSettings:
    # Anything to be added, for example
    # user_agents = []
    postfixes = []

    def __init__(self, postfixes: List[str]=[""], pages: int=10) -> None:
        # Лист возможных постфиксов для добавления в запрос
        self.postfixes = postfixes
        # Количество страниц, нужных для поиска
        self.pages_to_scan = pages

# GoogleSearcher класс для поиска в гугле, работает на основе интерфейса Searcher
class GoogleSearcher(Searcher):
    BASE_URL = "https://google.com/search"
    SEARCHES_NEEDED = 100
    POSTFIXES = []

    def __init__(self, settings: SearcherSettings) -> None:
        if settings.pages_to_scan != None: 
            self.PAGES_NEEDED = settings.pages_to_scan * 10
        if settings.postfixes != None:
            self.POSTFIXES.extend(settings.postfixes)
        self.headers = Headers()

    # основной метод, который на основе запроса пользователя возвращает все найденные результаты
    def process(self, user_request: UserRequest) -> List[Link]:
        # Requesting for each postfixs, could be empty string
        links_array = []
        # Для каждого уточняющего делаем запросы
        for postfix in self.POSTFIXES:
            # Проходим по всем результатам поиска от 0 до количества, которое нам нужно
            current_search, result = 0, 10
            for start in range(int(self.SEARCHES_NEEDED / 10)):
                if current_search <= result:
                    # Формируем запрос к поисковой системе на основе входных данных и постфикса
                    query = self.form_google_reuqest(user_request, postfix)
                    try:
                        # Получение html и его анализ
                        html = self._request(query, start)
                        links, result = self._parse_html(html)

                        # добавляем в ссылку регион откуда она пришла
                        for link in links:
                            link.set_postfix(postfix)
                        links_array.extend(links)

                    except Exception as e:
                        print("error ocured during search", e)
                        # На данном этапе пусть это будет вот так. 
                        pass
                        # При больших запросах он уже в рейтлимит кидает и так далее
                        # Дальше в реквест и настройки можно будет добавить прокси для избежания такиких историй
                    current_search += 10

        return links_array
    
    # Выполняет запрос к гуглу, кидает ошибку, если что-то не так 
    # query - текст запроса 
    # start - с какого запроса мы работаем
    def _request(self, query: str, start: int) -> str:
        query_params = {
            "q": query,
            'start': start 
        }
        encoded_params = urlencode(query_params)
        request_url = urljoin(self.BASE_URL, "?" + encoded_params)

        try:
            response = requests.get(request_url, headers=self.headers.get_headers())
            #print(response)
            if response.status_code == requests.codes.ok: 
                return response.text
            else:
                raise Exception(f"{self.BASE_URL} request error")
        except Exception as e:
            raise Exception("network error", e)

    # Происходит парсинг HTML, который возврашщает результаты, и количество возможных результатов.
    def _parse_html(self, html) -> Tuple[List[Link], int]:
        soup = BeautifulSoup(html, 'lxml')
        links = []
        try:
            
            results_div = soup.find("div", id="search")
            
            if results_div is None:
                # No results 
                return links, 0
            
            results_div = results_div.find("div", id="rso")

            if results_div is None:
                # No results 
                return links, 0

            for child in results_div.children:
                # 3 nextes for each chiled is the div with href, not for translate and etc
                try:
                    search_div = child.next.next.next.next
                    url = search_div.find('a')['href']
                    name = search_div.find('h3').text
                    links.append(Link(url, name, self.BASE_URL))
                except:
                    # skipping if not search result
                    pass
            
            navigation_div = soup.find("div", id="result-stats").text
            pattern = r'(\d+(?:,\d+)*)\s*(?:results|\(.*\))'

            num_results = re.search(pattern, navigation_div).group(1).replace(',', '')

            return links, int(num_results)
        except:
            raise Exception("not valid html provided")
    
    # Формиурем запрос на основе пользовательского запроса 
    # object берется в кавычки так как обязательно должен присутсвовать
    # Добавляем постфикс, позитивные и негативные кейворды
    @staticmethod
    def form_google_reuqest(user_input: UserRequest, postfix: str) -> str:
        #print(f'"{user_input.obejct}" {postfix} {", ".join(user_input.positive)} {" ".join("-{}".format(x) for x in user_input.negative)}')
        return f'"{user_input.object}" {postfix} {", ".join(user_input.positive)} {" ".join("-{}".format(x) for x in user_input.negative)}'

