
style_header = {
    'textAlign': 'left',
    'fontWeight': 'bold',
    'font-family':'Calibri',
    'background': '#f1f0fe',
    'padding-top': '40px',
    'overflow':'hidden',
    'table-layout': 'fixed',
}

style_cell= {
    'textAlign': 'left',
    'font-family': 'Calibri',
    'background': 'white',
    'border-radius': '5px',
    'border': '1px solid #e0dfed',
    'background': '#f1f0fe',
    'padding': '40px',
    'table-layout': 'fixed',
    'whiteSpace': 'pre-wrap',
}


style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)',
        'table - layout': 'fixed',
        'whiteSpace': 'pre-wrap',
    },
    {
        'if': {'row_index': 'even'},
        'backgroundColor': 'white',
        'table - layout': 'fixed',
        'whiteSpace': 'pre-wrap',
    },
    {
        'if': {'column_id': 'URL-адрес'},
        'width': '220%',
        'table - layout': 'fixed',
        'whiteSpace': 'pre-wrap',
    },
    {
        'if': {'column_id': 'Фото'},
        'width': '20%',
        'table - layout': 'fixed',
        'whiteSpace': 'pre-wrap',
    },
    {
        'if': {'column_id': 'Регион'},
        'width': '20%',
        'table - layout': 'fixed',
        'whiteSpace': 'pre-wrap',
    },
    {
        'if': {'column_id': 'Актуальность'},
        'width': '20%',
        'table - layout': 'fixed',
        'whiteSpace': 'pre-wrap',
    },
    {
        'if': {'column_id': 'Ключевые слова'},
        'width': '30%',
        'table - layout': 'fixed',
        'whiteSpace': 'pre-wrap',
    },
]

style = {'margin': '0 auto', 'background': 'white', 'border-radius': '5px', 'border': '25px solid #ffffff', 'background': '#f1f0fe', 'height': '100%', 'right': '10px', 'left': '10px', 'table-layout':'fixed', 'whiteSpace': 'pre-wrap'}