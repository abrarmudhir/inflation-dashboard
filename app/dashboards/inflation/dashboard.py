import time
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import requests
from dash import Dash
from dash_bootstrap_components import themes
from plotly.subplots import make_subplots

dashboard = Dash(__name__, requests_pathname_prefix="/dashboard/", external_stylesheets=[themes.BOOTSTRAP])

FASTAPI_URL = "http://localhost:8050"


def fetch_data(url, max_retries=5, retry_delay=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return pd.DataFrame(data['data'])
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data from {url}. Retrying ({attempt + 1}/{max_retries})...")
            time.sleep(retry_delay)
    raise Exception(f"Failed to fetch data from {url} after {max_retries} retries.")


def create_inflation_dashboard():
    au_data = fetch_data(f"{FASTAPI_URL}/api/annualised_cpi/au")
    uk_data = fetch_data(f"{FASTAPI_URL}/api/annualised_cpi/uk")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=au_data['time_period'], y=au_data['annualised_cpi'] * 100, mode='lines', name='AU CPI',
                   line=dict(color='red')),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=uk_data['time_period'], y=uk_data['annualised_cpi'] * 100, mode='lines', name='UK CPI',
                   line=dict(color='blue')),
        secondary_y=False
    )

    # Update layout
    fig.update_layout(
        title='Inflation (CPI)',
        xaxis_title='Date',
        yaxis_title='%',
        legend=dict(
            title="variable",
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="right",
            x=1.05
        )
    )

    return fig


dashboard.layout = html.Div(children=[
    html.Div(id='inflation-graph-container'),
    html.Div(id='refresh-container', style={'textAlign': 'right', 'margin': '10px'}),
    html.Button('Refresh Data', id='refresh-data-button', n_clicks=0, style={'float': 'right', 'marginRight': '10px'})
])


@dashboard.callback(
    [dash.dependencies.Output('inflation-graph-container', 'children'),
     dash.dependencies.Output('refresh-container', 'children')],
    [dash.dependencies.Input('refresh-data-button', 'n_clicks')]
)
def load_inflation_data(n_clicks):
    if n_clicks > 0:
        fig = create_inflation_dashboard()
        refresh_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        refresh_text = html.P(f"Refreshed at {refresh_time}", style={'marginRight': '20px', 'fontSize': '12px'})
        return dcc.Graph(id='inflation-graph', figure=fig), refresh_text
    else:
        return html.Div(), html.Div()


if __name__ == "__main__":
    dashboard.run()
