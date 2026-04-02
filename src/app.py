from dash import Dash, html, dcc

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Spotify Dashboard"),
    dcc.Graph(id="example-graph")
])