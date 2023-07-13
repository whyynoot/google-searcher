from bs4 import BeautifulSoup
from search_result import SearchResult
import requests
from proxy import get_random_proxy
from headers import Headers
import wget
from link import Link
from input_interpreter import UserRequest
from typing import List

# TODO: Переделать это
class ParserHTML:
    headers = Headers

    def __init__(self, config):
        self.headers = Headers()

    # Функция скачивания файла нужного для дальнешей работы
    def download(self, url, filename):
        print("Starting Downloading...")
        try:
            wget.download(url, f'{filename}.png')
            print("Successfully Downloaded.")
        except:
            print("Eror on download")

    # оснавная точка входа в класс парсера, на вход подается ссылка, и запрос пользователя (используется для обработки и анализа)
    # делает запрос на ссылку, и после парсит и анализирует
    def analyze(self, link: Link, user_request: UserRequest):
        text = ""
        #headers=self.headers.get_headers()
        try:
            #response = requests.get(link.url, proxies=get_random_proxy())
            response = requests.get(link.url, self.headers.get_headers(), timeout=2)
            print(response)
            if response.status_code == requests.codes.ok: 
                 text = response.text
            else:
                pass
        except Exception as e:
            pass
            #print("network error dutring parsing html")
            #raise Exception("network error", e)
        
        if text:
            soup = BeautifulSoup(response.text, 'lxml')
        else: 
            pass
            raise Exception("not valid html returned")
        
        photo = ""
        first_strs = user_request.object.lower().split(' ')
        flag_img = 1
        try:
            # flag_img = 0
            counter = 0
            # first_strs = user_request.object.lower().split(' ')
            # imgs = soup.find_all("img")
            #
            # for img in imgs:
            #     second_strs = img['alt'].lower().split(' ')

                # for str1 in first_strs
                #     for str2 in second_strs
                #         if str1 == str2
                #         counter++
                        
                # if counter > 0
                #     url_download = " "
                #     url = img['src']
                #     if url[0] == '/'
                #         url_new = ""
                #         counter_s = 0
                #         for char in link.url

                #             if char == '/'
                #                 counter_s += 1
    
                #             if counter_s < 3
                #                 url_new += char
                #             else
                #                 break
                
                #         url_download = url_new + url
                #     else
                #         url_download = url

                #     download(url_download, first_strs):
                #     flag_img = 1
        except Exception as e:
            pass
            #print("error finding image")

        region = link.request_region
        
        content_analysis = ""
        try:
            divs = soup.find_all('div')
            for div in divs:
                ps = div.find_all('p')
                for p in ps:
                    content_analysis += " " + p.get_text()
        except:
            pass
            #print("error during content analysis")

        if content_analysis == "" and flag_img == 0 and region == "" and photo == "":
            return None
        else:
            return SearchResult(link.url, photo, region, content_analysis)

# Интрефейс для работы с парсером страниц     
# HTML парсер делает запрос на страницу, обрабатывает HTML и возвращает пропаршенные ссылки
class HTMLParserInterface:
    
    # основной метод для работы с классом. 
    def analyze(self, link: Link, user_request: UserRequest) -> SearchResult:
        raise NotImplemented

# Реализация интерйфейса HTML Parser
# TODO: Сделать реализацию 
class HTMLParser(HTMLParserInterface):
    # Атрибуты, например класс Header
    # Реализация на основе конфигурации
    # В конфигурации идут как и по какому признаку индефицировать регион.
    def __init__(self, config) -> None:
        pass

    # основной метод для работы с классом. Делает запрос, поиск фотографии, сохранение, контект анализ, анализ региона и актуальности (через мета-теги)
    # TODO: Нормально оформить
    def analyze(self, link: Link, user_request: UserRequest) -> SearchResult:
        pass

    # Метод запроса страницы, на вход подается ссылка куда делать запрос, на выходе текст ответа (html) МЕТОД ПРИВАТНЫЙ
    # TODO: Нормально оформить
    def _request(self, url: str) -> str:
        pass
    
    # На вход подается объект soup в которой уже засунули html и он готов для работы, на выход мы получаем 1 фотографию (ссылку на нее). МЕТОД ПРИВАТНЫЙ
    # TODO: Сделать нормально, не как говно и так далее
    def _search_photo(self, soup) -> str:
        pass

    # Функция загрзуки, на вход мы получаем ссылку на файл, который надо загрузить, на выход мы отдаем сгенированное название нашей фотографии в файловой системе МЕТОД ПРИВАТНЫЙ
    def _download_photo(self, link: str) -> str:
        pass

    # Поиск региона, пытаемся удостовериться что регион из user_request был верный и тд.
    # TODO: Реализовать поиск, а не просто по дефолту делать регион
    def _search_region(self, soup, user_request: UserRequest, link: Link) -> str:
        pass

    # Произвести контект анализ страницы, на выходе результаты контент анализа. На вход поступает объект супа МЕТОД ПРИВАТНЫЙ
    # TODO: Сделать нормальный, буду спрашивать Вадима, о результатах отпишу
    def _perform_content_analysis(self, soup) -> str:
        pass