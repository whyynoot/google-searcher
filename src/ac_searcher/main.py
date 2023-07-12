from ac_searcher import AcSearcher
from config import config


a = AcSearcher(config)
# TODO: после исправления, мейн должен выглядить как в комментарии больше ничего в файле мейн не должно быть
def main():

    a.run()
    #a.app.run_server(debug=True)

# @a.app.callback(
#        Output('result-container', 'children'),
#        [Input('submit-button', 'n_clicks')],
#        [State('query-input', 'value')]
# )
# def func(n_clicks, query):
#     return a.process_query(n_clicks, query)

if __name__ == "__main__":
    main()