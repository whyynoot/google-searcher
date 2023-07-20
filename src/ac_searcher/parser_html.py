from src.ac_searcher.iparser_html import IHtmlParser
import re
from bs4 import BeautifulSoup
from src.ac_searcher.search_result import SearchResult
import requests
from src.ac_searcher.headers import Headers
from src.ac_searcher.link import Link
from src.ac_searcher.input_interpreter import UserRequest
from urllib.parse import urlsplit, urljoin, urlparse
from collections import Counter
import os
import uuid
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Реализация интерфейса HTML Parser
class HTMLParser(IHtmlParser):
    # Атрибуты, например класс Header
    # Реализация на основе конфигурации
    # В конфигурации идут, как и по какому признаку индицировать регион.
    def __init__(self, config) -> None:
        self.headers = Headers()
        self.config = config
        nltk.download('stopwords')  # Загрузка стоп-слов
        nltk.download('punkt')  # Загрузка ресурсов для токенизации

    # Основной метод для работы с классом. Делает запрос, поиск фотографии, сохранение,
    # контекст анализ, анализ региона и актуальности (через мета-теги)
    def analyze(self, link: Link, user_request: UserRequest) -> SearchResult:
        html = self._request(link.url)
        photo = ""
        search_region = ""
        perform_content_analysis = ""
        if html != "":
            soup = BeautifulSoup(html, 'lxml')
            link_photo = self._search_photo(soup, user_request.object, link.url)

            if link_photo != "":
                photo = self._download_photo(link_photo)
            else:
                photo = self._take_screenshot(link.url)

            search_region = self._search_region(soup, user_request, link)
            perform_content_analysis = self._perform_content_analysis(soup)

        search_result = SearchResult(url=link.url, photo=photo, region=search_region,
                                     content_analysis=perform_content_analysis)

        return search_result

    # Метод запроса страницы, на вход подается ссылка куда делать запрос, на выходе текст ответа (html) МЕТОД ПРИВАТНЫЙ
    def _request(self, url: str) -> str:
        try:
            response = requests.get(url,
                                    headers=self.headers.get_headers())  # Отправляем GET-запрос по указанной ссылке
            html = response.text  # Получаем HTML-код страницы
            return html
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {str(e)}")
            return ""

    # На вход подается объект soup в которой уже засунули html и он готов для работы,
    # на выход мы получаем 1 фотографию (ссылку на нее). МЕТОД ПРИВАТНЫЙ
    def _search_photo(self, soup, user_request, url) -> str:
        images = soup.find_all('img')
        base_url = self._get_base_url(url)
        max_similarity = 0
        result = ""
        keywords = user_request.lower().split()
        for image in images:
            alt_text = image.get('alt', '').lower()
            similarity = self._calculate_similarity(alt_text, keywords)
            if similarity > max_similarity:
                max_similarity = similarity
                image_src = image.get('src', '')
                absolute_src = self._get_absolute_url(base_url, image_src)
                if self._is_valid_extension(absolute_src):
                    result = absolute_src
        return result

    # Функция загрузки, на вход мы получаем ссылку на файл, который надо загрузить,
    # на выход мы отдаем сгенерированное название нашей фотографии в файловой системе МЕТОД ПРИВАТНЫЙ
    def _download_photo(self, link: str) -> str:
        try:
            response = requests.get(link, stream=True)
            if response.status_code != 200:
                return ""
            filename = os.path.basename(link)
            if not filename or os.path.exists(os.path.join('media', filename)):
                filename = f"{uuid.uuid4()}.jpg"
            filepath = os.path.join('media', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filepath
        except Exception as e:
            print("Error with download file", e)
            return ""

    # Поиск региона, пытаемся удостовериться что регион из user_request был верный и тд.
    def _search_region(self, soup, user_request: UserRequest, link: Link) -> str:
        page_text = soup.get_text().lower()

        present_cities = [city for city in self.config['cities'] if city.lower() in page_text]
        if present_cities:
            city_count = Counter()

            for city in present_cities:
                count = page_text.count(city.lower())
                city_count[city] = count

            most_common_city = city_count.most_common(1)
            return most_common_city[0][0]
        else:
            return link.postfix

    # Произвести контекст анализ страницы, на выходе результаты контент анализа.
    # На вход поступает объект супа МЕТОД ПРИВАТНЫЙ
    def _perform_content_analysis(self, soup) -> str:
        result = ""
        stop_words = set(stopwords.words('russian'))
        word_counter = Counter()
        separator = ' '  # Разделитель между текстовыми элементами
        for element in soup.find_all(text=True):
            text = element.strip()

            words = nltk.word_tokenize(text)
            filtered_words = [word.lower() for word in words if self._is_cyrillic_word(word)
                              and word.isalpha() and word not in stop_words]

            word_counter.update(filtered_words)

        most_common_words = word_counter.most_common(5)
        result = separator.join(word for word, count in most_common_words)
        return result

    def _get_base_url(self, url):
        parts = urlsplit(url)
        base_url = f"{parts.scheme}://{parts.netloc}"
        return base_url

    def _get_absolute_url(self, base_url, url, ):
        absolute_url = urljoin(base_url, url)
        return absolute_url

    def _calculate_similarity(self, text, keywords):
        similarity = 0
        for keyword in keywords:
            if keyword in text:
                similarity += 1
        return similarity

    def _is_valid_extension(self, link: str) -> bool:
        valid_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']
        ext = os.path.splitext(link)[1].lower()
        return ext in valid_extensions

    def _take_screenshot(self, url: str) -> str:
        try:
            chrome_driver_path = os.path.join("drivers", "chromedriver")  # Путь к ChromeDriver
            chrome_binary_path = os.path.join("drivers", "chrome", "chrome")  # Путь к исполняемому файлу Google Chrome

            # Устанавливаем права на исполнение для ChromeDriver
            os.chmod(chrome_driver_path, 0o755)

            options = Options()
            options.add_argument("--headless")  # Запуск браузера в режиме без графического интерфейса
            options.binary_location = chrome_binary_path  # Указываем путь к исполняемому файлу Google Chrome

            # Устанавливаем права на исполнение для исполняемого файла Google Chrome
            os.chmod(chrome_binary_path, 0o755)

            service = Service(chrome_driver_path)
            service.start()

            driver = webdriver.Remote(service.service_url, options=options)
            driver.get(url)

            media_folder = 'media'
            screenshot_path = os.path.join(media_folder, f"{uuid.uuid4()}.png")
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

            driver.save_screenshot(screenshot_path)
            driver.quit()

            return screenshot_path

        except Exception as e:
            print("Error taking screenshot:", e)
            return ""

    # Функция для проверки, является ли слово кириллическим
    def _is_cyrillic_word(self, word):
        return bool(re.match('^[а-яё]+$', word, re.IGNORECASE))
