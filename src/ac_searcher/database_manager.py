from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, func, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from search_result import SearchResult
from typing import List

# Создание подключения к базе данных
# TODO: Перенести ссылку в config, а еще лучше в .env или в переменные окружения. Она не должна быть в таком формате здесь.
# TODO: Инициализацию engine нужно проводить в инициализации класса-менджера. Используем шаблон фасад, ограничвающий взаимодействие с БД. 
# [подключение и тд приватные переменные] есть методы для работы с объектами, огранчивающие программный функционал
engine = create_engine('postgresql://postgres:y5D6jGIf8XGQoKkr@10.220.75.63:5432/postgres')

# Создание базового класса моделей
Base = declarative_base()

# Определение модели таблицы
# TODO: рассказать побольше про класс
class SearchResultDB(Base):
    __tablename__ = 'search_results0'
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                nullable=False,
                unique=True,
                )
    url = Column(Text, nullable=False)
    photo = Column(Text, nullable=True)
    region = Column(Text, nullable=False)
    relevance = Column(Date, nullable=False, server_default=func.current_date())
    content_analysis = Column(Text, nullable=True)

    def __init__(self, SearchResultModel):
        self.url = SearchResultModel.url
        self.photo = SearchResultModel.photo
        self.region = SearchResultModel.region
        self.content_analysis = SearchResultModel.content_analysis


# Создание таблицы в базе данных
# TODO: перенос в конуструктор, проверка на ошибки создания, подключения, и так далее. Все ошибки нужно прокинуть на иницализации.
Base.metadata.create_all(engine)

# Создание сессии для работы с базой данных
# TODO: Перенос в бд
Session = sessionmaker(bind=engine)
session = Session()

# TODO: перенести в методы
def save_search_result(search_result):
    new_result = SearchResultDB(search_result)
    session.add(new_result)
    session.commit()


def get_search_result_from_database(search_result_id):
    result = session.query(SearchResultDB).filter_by(id=search_result_id).first()
    if result:
        search_result = SearchResult(result)
        return search_result
    else:
        return None


def get_all_search_results_from_database():
    results = session.query(SearchResultDB).all()
    listings = []
    for result in results:
        listing = SearchResult(result)
        listings.append(listing)
    return listings


# Интерфейс для работы с базой данных 
# Используется для инициаозиации подключения и работы. 
# Применяется шаблон Фасад.
# Реализация варируется взависимсоти от БД.
class DataBaseManagerInterface: 
    # атрибуты нужные для работы

    # Конструктор, в котором происходит реализация
    def __init__(self, config) -> None:
        raise NotImplemented

    # Запись в бд, обработка ошибок, возврат записалось ли и тд. Успешно и тд
    # Класс не должен падать, если ошибочный коммит и тд (вдруг потеряли доступ к БД)
    def save_search_result(self, search_result: SearchResult) -> bool: 
        raise NotImplemented
    
    # Получить все резульататы
    # На возврат идут SearchResultModel массив
    def get_search_results(self) -> List[SearchResult]:
        raise NotImplemented
    
    # Разоварать подклчючение к бд, чтобы не терять данные в случае экстренного завершения и тд.
    def close_connection(self):
        raise NotImplemented
    
# TODO: На основе интрейфейса написать класс
# TODO: Удаляем не нужное и чистим код