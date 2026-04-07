# from dash import Dash, html, dcc

# app = Dash(__name__)
# app.layout = html.Div([
#     html.H1("Spotify Dashboard"),
#     dcc.Graph(id="example-graph")
# ])

from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- LOAD DATA ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "most-streamed-spotify-songs-2024-clean.csv"

# Load the cleaned CSV
df = pd.read_csv(DATA_PATH)

# Sort by streams to get a nice chart
df_sorted = df.sort_values("spotify_streams", ascending=False).head(10)

# --- CREATE PLOTS ---
# 1. Bar Chart: Top 10 Streamed Songs
bar_fig = px.bar(
    df_sorted, 
    x="track", 
    y="spotify_streams", 
    color="artist",
    title="Top 10 Most Streamed Songs"
)

# 2. Scatter Plot: Streams vs Popularity
scatter_fig = px.scatter(
    df, 
    x="spotify_streams", 
    y="spotify_popularity", 
    hover_name="track",
    color="artist",
    title="Streams vs. Popularity"
)

# --- APP LAYOUT ---
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Spotify 2024 Analytics Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Graph(id="bar-chart", figure=bar_fig),
    ], style={'width': '100%'}),
    
    html.Div([
        dcc.Graph(id="scatter-plot", figure=scatter_fig),
    ], style={'width': '100%'})
])