from searcher import Searcher, GoogleSearcher, SearcherSettings
from input_interpreter import InputInterpreter, ExampleInterpreter
from link import Link
from typing import List
from parser_html import ParserHTML
from database_manager import save_search_result
from search_result import SearchResult


# AcSearcher класс для описания программы, ее инициализации и запуска работы
class AcSearcher:
    # Инициализация главного класса приложения. На вход подается конфигурация, от конфигурации мы меняем некоторые настройки
    # классов инициализируемых далее
    # TODO: Разобраться с инициализацией Dash так, чтобы он был внутри этого класса. И даш можно было бы запускать на основе его.
    def __init__(self, config):
        self.interpreter = ExampleInterpreter()

        searcher_settings = SearcherSettings(postfixes=config["cities"], pages=config["pages_to_scan"])
        
        # Используем массив из классов типа сеарчер, чтобы можно было использовать несколько поисковых систем
        self.searchers = []
        self.searchers.append(GoogleSearcher(searcher_settings))
        self.parser_html = ParserHTML(config)
    
    # Метод запуска даш. 
    # TODO: В этом методе мы должны запустить даш. Это основная точка входа в наше приложение. Реализовать запуск даша.
    # TODO: Она должна быть подготовлена к любым неожиданностям. Должна был логика обработки критических ошибок приложения
    def run(self): 
        pass


    # Метод обработки входного запроса нашем приложением. На вход подается запрос пользователя - на выход выдаются полностью проработанные ссылки полностью.
    # TODO: упростить содержание кода, сделать его более читаемым. Извлечь некоторые циклы в методы (например поиск уникальных ссылок)
    def process(self, user_input) -> List[SearchResult]: 
        user_request = self.interpreter.analyse_input(user_input)

        links = []
        for searcher in self.searchers:
            searcher_links = searcher.process(user_request)
            links.extend(searcher_links)

        print(f"Finished parsing searchers, total links: {len(links)}")

        unique_links = []
        unique_searcher_links = []
        for link in links:
            if link.url not in unique_links:
                unique_searcher_links.append(link)
                unique_links.append(link.url)
        
        parsed_links = []
        for link in unique_searcher_links:
            try:
                searchresultmodel = self.parser_html.analyze(link, user_request)
                if searchresultmodel != None:
                    parsed_links.append(searchresultmodel)
                    print(searchresultmodel)
            except Exception as e:
                pass
                #print("error during parsing link", e)
                #записб в бд

        for link in parsed_links: 
            save_search_result(link)

        # TODO: Нужна обработка полученных ссылок, анализ на их релевантность
        
        return parsed_links        
