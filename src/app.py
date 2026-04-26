from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- 1. LOAD AND PREP DATA ---
try:
    # .parent gets 'src', the second .parent gets the root 'spotify-dashboard' folder
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_PATH = BASE_DIR / "data" / "most-streamed-spotify-songs-2024-clean.csv"
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    try:
        # Fallback 1: Maybe it's directly in the root folder next to main.py?
        df = pd.read_csv("most-streamed-spotify-songs-2024-clean.csv")
    except FileNotFoundError:
        # Fallback 2: Maybe it's in the src folder?
        df = pd.read_csv(Path(__file__).resolve().parent / "most-streamed-spotify-songs-2024-clean.csv")

# Clean data
df = df.fillna(0)
if 'explicit_track' in df.columns:
    df['explicit_label'] = df['explicit_track'].map({0: 'Clean', 1: 'Explicit'})
else:
    df['explicit_label'] = 'Unknown'

# Define standard metrics for our dropdowns
METRIC_OPTIONS =[
    {'label': 'Spotify Streams', 'value': 'spotify_streams'},
    {'label': 'YouTube Views', 'value': 'youtube_views'},
    {'label': 'TikTok Views', 'value': 'tiktok_views'},
    {'label': 'Apple Music Playlists', 'value': 'apple_music_playlist_count'},
    {'label': 'Spotify Popularity', 'value': 'spotify_popularity'},
    {'label': 'YouTube Likes', 'value': 'youtube_likes'},
    {'label': 'TikTok Likes', 'value': 'tiktok_likes'},
]

# Helper to get formatted labels
def get_label(value):
    return next((item['label'] for item in METRIC_OPTIONS if item['value'] == value), value)

# --- 2. INITIALIZE APP ---
app = Dash(__name__)

# --- 3. APP LAYOUT (One Window Design - 2x2 Grid with Dropdowns & Tabs) ---
app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'padding': '15px', 'backgroundColor': '#f4f6f9', 'height': '100vh', 'boxSizing': 'border-box'},
    children=[
        html.H2("Cross-Platform Music Analytics", style={'textAlign': 'center', 'margin': '0 0 5px 0'}),
        html.P("Designed for Music Producers: Box/Lasso select tracks on the Top-Left chart. Use Dropdowns/Tabs to change the views.", 
               style={'textAlign': 'center', 'color': '#555', 'margin': '0 0 15px 0', 'fontSize': '14px'}),
        
        # 2x2 Grid Container
        html.Div(
            style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px', 'justifyContent': 'center', 'height': 'calc(100vh - 90px)'},
            children=[
                
                # --- BOX 1: Master Scatter Plot (Brushing Source) ---
                html.Div([
                    html.Div([
                        html.Strong("1. Master Comparison (Brush Here)", style={'fontSize':'14px'}),
                        html.Div([
                            dcc.Dropdown(id='s1-y', options=METRIC_OPTIONS, value='tiktok_views', clearable=False, style={'width': '48%', 'fontSize':'12px'}),
                            html.Span(" vs ", style={'paddingTop':'5px', 'fontSize':'12px'}),
                            dcc.Dropdown(id='s1-x', options=METRIC_OPTIONS, value='spotify_streams', clearable=False, style={'width': '48%', 'fontSize':'12px'})
                        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop':'5px'})
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="master-scatter", style={'height': '280px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px', 'display': 'flex', 'flexDirection': 'column'}),
                
                # --- BOX 2: Dynamic Top 10 Bar Chart ---
                html.Div([
                    html.Div([
                        html.Strong("2. Top 10 Leaderboard", style={'fontSize':'14px'}),
                        dcc.Dropdown(id='bar-metric', options=METRIC_OPTIONS, value='youtube_views', clearable=False, style={'width': '100%', 'marginTop':'5px', 'fontSize':'12px'})
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="top10-bar", style={'height': '280px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px', 'display': 'flex', 'flexDirection': 'column'}),

                # --- BOX 3: Secondary Comparison Plot ---
                html.Div([
                    html.Div([
                        html.Strong("3. Secondary Comparison (Linked)", style={'fontSize':'14px'}),
                        html.Div([
                            dcc.Dropdown(id='s2-y', options=METRIC_OPTIONS, value='spotify_streams', clearable=False, style={'width': '48%', 'fontSize':'12px'}),
                            html.Span(" vs ", style={'paddingTop':'5px', 'fontSize':'12px'}),
                            dcc.Dropdown(id='s2-x', options=METRIC_OPTIONS, value='youtube_views', clearable=False, style={'width': '48%', 'fontSize':'12px'})
                        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop':'5px'})
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="secondary-scatter", style={'height': '280px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px', 'display': 'flex', 'flexDirection': 'column'}),

                # --- BOX 4: Demographics / Distributions (Tabs) ---
                html.Div([
                    html.Div([
                        html.Strong("4. Distribution & Strategy", style={'fontSize':'14px', 'display':'block', 'marginBottom':'5px'}),
                        dcc.Tabs(id='tabs-extra', value='tab-pie', children=[
                            dcc.Tab(label='Content (Explicit/Clean)', value='tab-pie', style={'padding': '5px', 'fontSize':'12px'}, selected_style={'padding': '5px', 'fontSize':'12px', 'fontWeight': 'bold'}),
                            dcc.Tab(label='Popularity Histogram', value='tab-hist', style={'padding': '5px', 'fontSize':'12px'}, selected_style={'padding': '5px', 'fontSize':'12px', 'fontWeight': 'bold'}),
                        ], style={'height': '30px'})
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="extra-chart", style={'height': '270px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px', 'display': 'flex', 'flexDirection': 'column'})
            ]
        )
    ]
)

# --- 4. CALLBACKS ---

# Callback 1: Update Master Scatter Plot (Based on its dropdowns)
@app.callback(
    Output("master-scatter", "figure"),[Input("s1-x", "value"), Input("s1-y", "value")]
)
def update_master_scatter(x_col, y_col):
    fig = px.scatter(
        df, x=x_col, y=y_col, 
        hover_name="track", hover_data=["artist"],
        color="spotify_popularity", color_continuous_scale="Viridis",
        custom_data=[df.index] # Crucial for linking!
    )
    fig.update_layout(
        dragmode="lasso", template="plotly_white", 
        margin=dict(l=30, r=20, t=20, b=20),
        xaxis_title=get_label(x_col), yaxis_title=get_label(y_col)
    )
    return fig

# Callback 2: Update Linked Charts (Based on Master Selection + Local Dropdowns/Tabs)
@app.callback([Output("top10-bar", "figure"), Output("secondary-scatter", "figure"), Output("extra-chart", "figure")],[Input("master-scatter", "selectedData"),
     Input("bar-metric", "value"),
     Input("s2-x", "value"), Input("s2-y", "value"),
     Input("tabs-extra", "value")]
)
def update_linked_charts(selectedData, bar_metric, s2_x, s2_y, tab_choice):
    # 1. Filter dataset based on Master Selection
    if selectedData and 'points' in selectedData:
        selected_indices =[point['customdata'][0] for point in selectedData['points']]
        filtered_df = df.iloc[selected_indices]
    else:
        filtered_df = df

    # 2. Update Top 10 Bar Chart
    top_df = filtered_df.sort_values(bar_metric, ascending=False).head(10)
    bar_fig = px.bar(
        top_df, x=bar_metric, y="track", orientation="h",
        color=bar_metric, color_continuous_scale="Reds"
    )
    bar_fig.update_layout(
        yaxis={'categoryorder':'total ascending'}, template="plotly_white", 
        margin=dict(l=30, r=20, t=20, b=20), 
        xaxis_title=get_label(bar_metric), yaxis_title=""
    )

    # 3. Update Secondary Scatter Chart
    scatter2_fig = px.scatter(
        filtered_df, x=s2_x, y=s2_y, 
        hover_name="track", color_discrete_sequence=["#e377c2"]
    )
    scatter2_fig.update_layout(
        template="plotly_white", margin=dict(l=30, r=20, t=20, b=20),
        xaxis_title=get_label(s2_x), yaxis_title=get_label(s2_y)
    )

    # 4. Update Extra Chart (Tabs)
    if tab_choice == 'tab-pie':
        pie_counts = filtered_df['explicit_label'].value_counts().reset_index()
        pie_counts.columns =['explicit_label', 'count']
        extra_fig = px.pie(
            pie_counts, names="explicit_label", values="count",
            color="explicit_label", color_discrete_map={'Clean': '#2ca02c', 'Explicit': '#1f77b4'}
        )
    else:
        extra_fig = px.histogram(
            filtered_df, x="spotify_popularity", nbins=20,
            color_discrete_sequence=["#ff7f0e"]
        )
        extra_fig.update_layout(xaxis_title="Spotify Popularity Score", yaxis_title="Count")
        
    extra_fig.update_layout(template="plotly_white", margin=dict(l=30, r=20, t=20, b=20))

    return bar_fig, scatter2_fig, extra_fig

# --- 5. RUN SERVER ---
# if __name__ == "__main__":
#     app.run_server(debug=True)