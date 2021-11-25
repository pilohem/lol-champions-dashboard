import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
import os
import pandas as pd
from dash.dependencies import Input, Output, State
import json

from app import app

from pages import app1, champion, home


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
    ]
)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page_content(pathname):
    path = app.strip_relative_path(pathname)
    if not path:
        return home.layout()
    elif "champion" in path:
        champion_str = path.split('-')[1]
        return champion.layout(champion_str)
    else:
        return home.layout()


if __name__ == '__main__':
    app.run_server(debug=True)