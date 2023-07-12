from searcher import Searcher, GoogleSearcher, SearcherSettings
from input_interpreter import InputInterpreter, ExampleInterpreter
from link import Link
from typing import List
from parser_html import ParserHTML
from database_manager import save_search_result
from search_result import SearchResult
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
import dash_bootstrap_components as dbc

web_app: object = None

#app = dash.Dash(external_stylesheets=[dbc.themes.GRID])
#external_stylesheets=['assets/typography.css']
app = dash.Dash()
# app.css.config.serve_locally = True
# external_scripts = True
# app.css.append_css({
#     'external_url': app.get_asset_url('header.css')
# })
#external_stylesheets=app.get_asset_url['assets/typography.css']



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


# AcSearcher класс для описания программы, ее инициализации и запуска работы
class AcSearcher:
    # Используем лист для того, чтобы было возможно использовать несколько поисковиков
    searchers = []
    interpreter = InputInterpreter
    parser_html = ParserHTML
    config = dict
    parsed_links = []

    # Инициализация главного класса приложения. На вход подается конфигурация, от конфигурации мы меняем некоторые настройки
    # классов инициализируемых далее
    # TODO: Разобраться с инициализацией Dash так, чтобы он был внутри этого класса. И даш можно было бы запускать на основе его.
    def __init__(self, config):
        self.interpreter = ExampleInterpreter()
        searcher_settings = SearcherSettings(postfixes=config["cities"], pages=config["pages_to_scan"])
        self.searchers.append(GoogleSearcher(searcher_settings))
        self.parser_html = ParserHTML(config)

    # Метод запуска даш.
    # TODO: В этом методе мы должны запустить даш. Это основная точка входа в наше приложение. Реализовать запуск даша.
    # TODO: Она должна быть подготовлена к любым неожиданностям. Должна был логика обработки критических ошибок приложения
    def run(self):
        global web_app
        web_app = self
        app.run_server(debug=True)

    def process_query(self, n_clicks, query):
        if n_clicks is None:
            return dash.no_update

        # через метод process мы отправляем пользовательский запрос на дальнейшую обработку
        parsed_links = self.process(query)
        # data = app.run(query)
        # print(f"Finished parsing links, total results: {len(self.parsed_links)}")
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
        app.css.append_css({
            'external_url': app.get_asset_url('assets/typography.css')
        })
        data = {
           'URL-адрес': [],
            'Фото': [],
           'Регион': [],
            'Актуальность': [],
            'Ключевые слова': []
        }

        for link in parsed_links:
           data['URL-адрес'].append(link.url)
           data['Фото'].append(link.photo)
           data['Регион'].append(link.region)
           data['Актуальность'].append(link.relevance)
           data['Ключевые слова'].append("Coming later")

        # TODO: переписать получение данных. Пример как я обрабатывал входные данные выше. Метод веренем вам массив из SearchResultModel
        # Лучше научиться отрисовывать на основе его. Можете придумать что-то новое, можете использовать мой код, но лучше новое, крассивое
        df = pd.DataFrame(data)

        # TODO: исправить таблицу и ее позиционирование и размер
        # TODO: таблица должна показывать фотографии
        return html.Div(
            children=html.Div([
                # html.H2("Результат"),
                # html.P(result)
                dash_table.DataTable(
                    id='table',
                    columns=[{'name': col, 'id': col} for col in df.columns],
                    data=df.to_dict('records'),
                    style_header={
                        'textAlign': 'left',
                        'fontWeight': 'bold',
                        'font-family':'Calibri',
                        'background': '#f1f0fe',
                        'padding-top': '40px',
                        'overflow':'hidden',
                        'table-layout': 'fixed',
                    },
                    style_cell={
                        'textAlign': 'left',
                        'font-family': 'Calibri',
                        'background': 'white',
                        'border-radius': '5px',
                        'border': '1px solid #e0dfed',
                        'background': '#f1f0fe',
                        'padding': '40px',
                        'table-layout': 'fixed',
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)',
                            'table - layout': 'fixed',
                        },
                        {
                            'if': {'row_index': 'even'},
                            'backgroundColor': 'white',
                            'table - layout': 'fixed',
                        },
                        {
                            'if': {'column_id': 'URL-адрес'},
                            'width': '220%',
                            'table - layout': 'fixed',
                        },
                        {
                            'if': {'column_id': 'Фото'},
                            'width': '20%',
                            'table - layout': 'fixed',
                        },
                        {
                            'if': {'column_id': 'Регион'},
                            'width': '20%',
                            'table - layout': 'fixed',
                        },
                        {
                            'if': {'column_id': 'Актуальность'},
                            'width': '20%',
                            'table - layout': 'fixed',
                        },
                        {
                            'if': {'column_id': 'Ключевые слова'},
                            'width': '30%',
                            'table - layout': 'fixed',
                        },
                    ]
                )
            ],
                style={'margin': '0 auto', 'background': 'white', 'border-radius': '5px', 'border': '25px solid #ffffff',
                   'background': '#f1f0fe', 'height': '100%', 'right': '10px', 'left': '10px', 'table-layout':'fixed'}
            )
        )

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
                print("error during parsing link", e)
                # записб в бд

        # for link in parsed_links:
        #     save_search_result(link)

        # TODO: Нужна обработка полученных ссылок, анализ на их релевантность

        return parsed_links

    # def callback(self, app):

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
                html.Td(id='result-container', className="style-for-table"),
            ]
        )