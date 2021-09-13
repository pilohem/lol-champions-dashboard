import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import json
import utils

f = open('data/lol_champion.json')
data = json.load(f)

available_champions = list(data['data'].keys())
champions_stats = utils.get_all_champion_stats(data, available_champions)

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

PAGE_SIZE = 5

app.layout = html.Div(children=[
    html.Div(children=[
        html.H2('League of Legends Champions'),
        dcc.Dropdown(id='champ-select', options=[{'label': champ, 'value': champ} for champ in available_champions], value='Ahri'),
        html.P(id='champ-info'),
        dash_table.DataTable(
            id='champions-table',
            columns=[
                {"name": col, "id": col, 'presentation': 'markdown'} for col in champions_stats.columns
            ],
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',
            markdown_options={'link_target': '_self'}
        ),
        dcc.Location(id='location'),
        html.H4(
            id='selected-champion'
        )
        
    ])
])

@app.callback(
    Output('champions-table', 'data'),
    [Input('champions-table', 'page_current'),
    Input('champions-table', 'page_size')]
)
def update_table(page_current, page_size):
    current_champions = champions_stats.iloc[page_current*page_size:(page_current + 1)*page_size].to_dict('records')
    return current_champions

@app.callback(
    Output('selected-champion', 'children'),
    Input('location', 'pathname')
)
def update_selected_champion(pathname):
    return app.strip_relative_path(pathname)

if __name__ == '__main__':
    app.run_server(debug=True)



