from src.ac_searcher.searcher import Searcher, GoogleSearcher, SearcherSettings
from src.ac_searcher.input_interpreter import InputInterpreter, ExampleInterpreter
from src.ac_searcher.link import Link
from typing import List
from src.ac_searcher.parser_html import HTMLParser
from src.ac_searcher.database_manager import DatabaseManager
from src.ac_searcher.search_result import SearchResult
from src.ac_searcher.task import Task
from concurrent.futures import ThreadPoolExecutor

TASK_STATUS_CREATED = 'created'
TASK_STATUS_IN_PROGRESS = "working"
TASK_STATUS_DONE = "done"
TASK_STATUS_FAILED = "failed"
# AcSearcher класс для описания программы, ее инициализации и запуска работы
class AcSearcher:

    # Инициализация главного класса приложения. На вход подается конфигурация, от конфигурации мы меняем некоторые настройки
    # классов инициализируемых далее
    def __init__(self, config):
        self.interpreter = ExampleInterpreter()
        searcher_settings = SearcherSettings(postfixes=config["cities"], pages=config["pages_to_scan"])

        self.searchers = []
        self.searchers.append(GoogleSearcher(searcher_settings))
        self.parser_html = HTMLParser(config)

        self.database_manager = DatabaseManager()

        self.config = config

        self.executor = ThreadPoolExecutor(max_workers=1)
        
    # Метод обработки входного запроса нашем приложением. 
    # На вход подается запрос пользователя - на выход выдаются полностью проработанные ссылки полностью.
    def process(self, user_request, query_id) -> List[SearchResult]:
        try:
            self.database_manager.update_task_status(query_id, TASK_STATUS_IN_PROGRESS)
            links = []
            for searcher in self.searchers:
                searcher_links = searcher.process(user_request)
                links.extend(searcher_links)

            print(f"Finished parsing searchers, total links: {len(links)}\nStariting parsing them...")

            unique_links = self.get_uniquie_link_list(links)

            parsed_links = []
            for link in unique_links:
                try:
                    searchresultmodel = self.parser_html.analyze(link, user_request)
                    if searchresultmodel != None:
                        searchresultmodel.set_query_id(query_id)
                        parsed_links.append(searchresultmodel)
                except Exception as e:
                    print("error during parsing link", e)


            for link in parsed_links:
                self.database_manager.save_search_result(link)

            self.database_manager.update_task_status(query_id, TASK_STATUS_DONE)

            # TODO: Нужна обработка полученных ссылок, анализ на их релевантность
            
            return parsed_links
        except Exception as e:
            print("Error during process", e)
            self.database_manager.update_task_status(query_id, TASK_STATUS_FAILED)

    def create_task(self, query, postive, negative): 
        user_request = self.interpreter.analyse_input(query, postive, negative)
        
        query_id = self.database_manager.create_task(user_request)

        if query_id == None:
            return None

        self.executor.submit(self.process, user_request, query_id)

        return query_id
    
    def check_for_task(self, task_id):
        task_db = self.database_manager.get_task_from_database(task_id)
        
        if task_db is not None:
            task = Task(task_db)
        else:
            return None

        # If task exists and done add result
        if task.status == TASK_STATUS_DONE:
            result = self.database_manager.get_task_result(task_id)
            task.set_result(result=result)
        
        return task

    # Получить уникальные ссылки
    @staticmethod
    def get_uniquie_link_list(links: List[Link]) -> List[Link]:
        unique_links = []
        unique_searcher_links = []
        for link in links:
            if link.url not in unique_links:
                unique_searcher_links.append(link)
                unique_links.append(link.url)
        return unique_searcher_links