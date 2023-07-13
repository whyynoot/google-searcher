import uuid
from typing import List

import sqlalchemy_utils
from sqlalchemy import create_engine, Column, Date, func, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError

from dotenv import load_dotenv
import os

from search_result import SearchResult
from idatabase_manager import IDatabaseManager


# Класс предоставляет функциональность для управления базой данных,
# включая инициализацию, сохранение и извлечение данных.
class DatabaseManager(IDatabaseManager):
    def __init__(self):
        self.engine = None
        self.Base = None
        self.session = None
        self.database_url = None
        self.is_initialized = False

        try:
            self.initialize_database()
            self.is_initialized = True
        except OperationalError as e:
            # Обработка ошибок при подключении
            self.is_initialized = False
            print("Error when connecting to database:", e)
        except Exception as e:
            # Обработка ошибок при инициализации
            self.is_initialized = False
            print("Database initialization error:", e)

    def initialize_database(self):
        self.get_database_config()
        self.engine = create_engine(self.database_url)
        # Проверка существует ли база данных
        if not sqlalchemy_utils.database_exists(self.engine.url):
            sqlalchemy_utils.create_database(self.engine.url, encoding='utf8mb4')
            print(f"The new database has been created: {self.engine}")
        else:
            print("The database already exists")

        self.Base = declarative_base()
        self.define_model()
        # Создание таблицы в базе данных
        self.Base.metadata.create_all(self.engine)

    def get_database_config(self):
        load_dotenv()
        self.database_url = os.getenv("DATABASE_URL")
        if self.database_url is None:
            raise Exception("Failed to retrieve database URL from .env file.")

    def define_model(self):
        # Определение модели таблицы
        class SearchResultDB(self.Base):
            __tablename__ = 'search_results'
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

        self.SearchResultDB = SearchResultDB

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def save_search_result(self, search_result):
        try:
            if not self.is_initialized:
                print("Error: DatabaseManager is not initialized")
            else:
                self.create_session()
                new_result = self.SearchResultDB(search_result)
                self.session.add(new_result)
                self.session.commit()
        except Exception as e:
            print("Error occurred during save_search_result():", e)
            return False
        finally:
            self.close_session()

        return True

    def get_search_result_from_database(self, search_result_id):
        try:
            if not self.is_initialized:
                print("Error: DatabaseManager is not initialized")
            else:
                self.create_session()
                result = self.session.query(self.SearchResultDB).filter_by(id=search_result_id).first()
                if result:
                    search_result = SearchResult(result)
                    return search_result
                else:
                    return None
        finally:
            self.close_session()

    def get_all_search_results_from_database(self):
        try:
            if not self.is_initialized:
                print("Error: DatabaseManager is not initialized")
            else:
                self.create_session()
                results = self.session.query(self.SearchResultDB).all()
                listings = []
                for result in results:
                    listing = SearchResult(result)
                    listings.append(listing)
                return listings
        finally:
            self.close_session()

    def close_session(self):
        if self.session is not None:
            self.session.close()
