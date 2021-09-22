import dash
from dash_bootstrap_components._components.Col import Col
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
champion_types = ['Assassin', 'Fighter', 'Mage', 'Marksman', 'Support', 'Tank']

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.DARKLY])

PAGE_SIZE = 5

app.layout = html.Div(children=[
    html.Div(children=[
        html.H2('League of Legends Champions'),
        dcc.Dropdown(id='champ-select', options=[{'label': champ_type, 'value': champ_type} for champ_type in champion_types], value='Mage'),
        html.P(id='champ-info'),
        dash_table.DataTable(
            id='champions-table',
            columns=[
                {"name": col, "id": col, 'presentation': 'markdown'} for col in champions_stats.columns
            ],
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
            },
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',
            markdown_options={'link_target': '_self'}),
        dcc.Location(id='location'),
        dbc.Row(id='selected-champion'),
        dbc.Row(id='selected-champion-type')
    ], style={'margin': '2rem 8rem'})
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
    champion = app.strip_relative_path(pathname)
    card1 = dbc.Card(
            [
                dbc.CardImg(src=f"assets/img/champion/{champion}_0.jpg", top=True),
            ],
    style={"width": "10rem"}
    )
    card2 = dbc.CardBody(
            [
                html.H4(f"{champion}", className="card-title"),
                html.P(data['data'][champion]['title']),
                html.P(
                    data['data'][champion]['blurb'],
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="primary"),
            ]
        )
    cards = dbc.Row([dbc.Col(card1, width='auto'), dbc.Col(card2)])

    return cards

@app.callback(
    Output('selected-champion-type', 'children'),
    Input('champ-select', 'value')
)
def update_selected_champions_by_type(selected_type):
    champions_tags = utils.get_champions_with_tags(data)
    return html.H4(utils.get_champions_by_type(selected_type, champions_tags)[selected_type])
    


if __name__ == '__main__':
    app.run_server(debug=True)



