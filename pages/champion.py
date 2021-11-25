import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import json

from app import app
f = open('data/lol_champion.json')
data = json.load(f)

def update_selected_champion(champion):
    # champion = app.strip_relative_path(pathname)
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


def layout(champion):
    return [
        html.Div([
            'On Chamion page',
        html.Div(
                dbc.Row([update_selected_champion(champion)], id='selected-champion'), style={"margin": '1rem'}
            )
        ])
    ]

# @app.callback(
#     Output('selected-champion', 'children'),
#     Input('location', 'pathname')
# )

