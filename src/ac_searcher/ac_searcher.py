from searcher import Searcher, GoogleSearcher, SearcherSettings
from input_interpreter import InputInterpreter, ExampleInterpreter
from link import Link
from typing import List
from parser_html import HTMLParser
from database_manager import DatabaseManager
from search_result import SearchResult
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from dash_styles import style_header, style_cell, style_data_conditional, style

# главный объект приложения. Объекта класса AcSearcher. Будет проинициализироавн вместе с созданием класса AcSearcher.
# Нужен этот класс для того, чтобы callbackу Dash было к кому обращаться
web_app: object = None

# Инициализируем даш, для последующей работы с ним, настраиваем калбеки даша.
app = dash.Dash()
@app.callback(
    Output('result-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('query-input', 'value')]
)
def func(n_clicks, query):
    if web_app is None:
        print("Webapp not initialized")
    else:
        return web_app.process_query(n_clicks, query)
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
# app.css.append_css({
#     'external_url': app.get_asset_url('typography.css')
# })


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
        # Настраиваем под даш.
        global web_app
        web_app = self

    # Метод запуска даш.
    def run(self):
        try:
            app.run_server(debug=True, port=self.config['server']['port'], host=self.config['server']['host'])
        except Exception as e:
            print(e, type(e))
            print("Fatal dash, server error, restarting...")
            self.run()
        
    # Метод обработки входного запроса нашем приложением. 
    # На вход подается запрос пользователя - на выход выдаются полностью проработанные ссылки полностью.
    def process(self, user_input) -> List[SearchResult]:
        user_request = self.interpreter.analyse_input(user_input)

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
                    parsed_links.append(searchresultmodel)
            except Exception as e:
                print("error during parsing link", e)


        for link in parsed_links:
            self.database_manager.save_search_result(link)

        # TODO: Нужна обработка полученных ссылок, анализ на их релевантность
        
        return parsed_links

    # Метод обрабатывающий входной запрос из фронтенда. И выводящий таблицу, полученную в результате обработки на фронт.
    def process_query(self, n_clicks, query):
        if n_clicks is None:
            return dash.no_update

        print("Starting processing query...")
        # через метод process мы отправляем пользовательский запрос на дальнейшую обработку
        parsed_links = self.process(query)

        data = {
            'URL-адрес': [],
            'Фото': [],
            'Регион': [],
            'Актуальность': [],
            'Ключевые слова': []
        }
        photo_url = 'https://nic-pnb.ru/wp-content/uploads/2014/06/remarchuk.jpg'
        for link in parsed_links:
           data['URL-адрес'].append(link.url)
           data['Фото'].append(link.photo)
           data['Регион'].append(link.region)
           data['Актуальность'].append(link.relevance)
           data['Ключевые слова'].append("Coming later")

        # Лучше научиться отрисовывать на основе его. Можете придумать что-то новое, можете использовать мой код, но лучше новое, крассивое
        df = pd.DataFrame(data)

        return html.Div(
            children=html.Div([
                dash_table.DataTable(
                    id='table',
                    columns=[{'name': col, 'id': col} for col in df.columns],
                    data=df.to_dict('records'),
                    style_header=style_header,
                    style_cell=style_cell,
                    style_data_conditional=style_data_conditional,
                )],
                style=style)
        )

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

app.layout = html.Div(
            className="app-header",
            children=[
                html.H1("Наборы данных"),
                html.Span(
                    className="headerr",
                    children=[
                        dcc.Input(id='query-input', type='text', placeholder='Введите запрос',
                                  className="styleone"),
                        html.Button('Найти', id='submit-button', className="styletwo"),
                    ]),
                dcc.Loading(
                    id='loading',
                    type='circle',
                    children=[
                        html.Td(id='result-container', className="style-for-table")
                    ],
                    style={'font-size': '80px', 'width': '200px', 'height': '200px'}
                )
            ]
)