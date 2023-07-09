from ac_searcher import AcSearcher
from config import config
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd

# TODO: ИНИЦИАЛИЗИРОВАТЬ В МЕЙНЕ, И ТАМ ЖЕ ЗАПУСКАТь ЧЕРЕЗ .run()
a = AcSearcher(config)

# TODO: УБРАТЬ, ИНИЦИАЛИЗРОВАТЬ В ОДНОМ МЕСТЕ, ИСПОЛЬЗОВАТЬ В КЛАССЕ AC_SEARCHER
app = dash.Dash(__name__)

# TODO: УБРАТЬ, ИНИЦИАЛИЗРОВАТЬ В ОДНОМ МЕСТЕ, ИСПОЛЬЗОВАТЬ В КЛАССЕ AC_SEARCHER
app.layout = html.Div(
    className="app-header",
    children=[
        html.H1("Наборы данных"),
        html.Span(
            className="headerr",
            children = [
            dcc.Input(id='query-input', type='text', placeholder='Введите запрос',
                      style={'width': '450px', 'textAlign': 'center', 'height': '30px', 'margin-top': '20px', 'background':'#f1f0fe',
                             'border':'1px solid #e0dfed', 'border-radius': '5px'}),
            html.Button('Найти', id='submit-button', style={'margin-left':'30px','height': '35px', 'textAlign': 'center',
                                                            'border-radius': '5px','border':'1px solid #e0dfed','background':'#f1f0fe' }),
        ]),
        html.Div(id='result-container', className="app-header--title"),
    ]
)

# TODO: УБРАТЬ, ИНИЦИАЛИЗРОВАТЬ В ОДНОМ МЕСТЕ, ИСПОЛЬЗОВАТЬ В КЛАССЕ AC_SEARCHER
@app.callback(
    Output('result-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('query-input', 'value')]
)
def process_query(n_clicks, query):
    if n_clicks is None:
        return dash.no_update
    
    # через метод process мы отправляем пользовательский запрос на дальнейшую обработку
    data = a.process(query)

    
    # print(f"Finished parsing links, total results: {len(parsed_links)}")

    # data = {
    #     'URL-адрес': [],
    #     'Фото': [],
    #     'Регион': [],
    #     'Актуальность': [],
    #     'Ключевые слова': []
    # }

    # for link in parsed_links:
    #     data['URL-адрес'].append(link.url)
    #     data['Фото'].append(link.photo)
    #     data['Регион'].append(link.region)
    #     data['Актуальность'].append(link.relevance)
    #     data['Ключевые слова'].append("Comming later")
    
    # TODO: переписать получение данных. Пример как я обрабатывал входные данные выше. Метод веренем вам массив из SearchResultModel
    # Лучше научиться отрисовывать на основе его. Можете придумать что-то новое, можете использовать мой код, но лучше новое, крассивое
    df = pd.DataFrame(data)
    
    # TODO: исправить таблицу и ее позиционирование и размер
    # TODO: таблица должна показывать фотографии
    return html.Div(
        children=html.Div([
            #html.H2("Результат"),
            # html.P(result)
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in df.columns],
                data=df.to_dict('records'),
                style_header={
                    'textAlign': 'center',
                    'fontWeight': 'bold'
                },
                style_cell={
                    'textAlign': 'center'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'white'
                    },
                    {
                        'if': {'column_id': 'URL-адрес'},
                        'width': '40%'
                    },
                    {
                        'if': {'column_id': 'Фото'},
                        'width': '40%'
                    },
                    {
                        'if': {'column_id': 'Регион'},
                        'width': '40%'
                    },
                    {
                        'if': {'column_id': 'Актуальность'},
                        'width': '20%'
                    },
                    {
                        'if': {'column_id': 'Ключевые слова'},
                        'width': '45%'
                    },
                ]
            )
        ],
            style={'maxWidth': '600px', 'margin': '0 auto'}
        )
    )

# TODO: после исправления, мейн должен выглядить как в комментарии больше ничего в файле мейн не должно быть
def main():
    # app = AcSearcher(config)
    # app.run()

    app.run_server(debug=True)

if __name__ == "__main__": 
    main()