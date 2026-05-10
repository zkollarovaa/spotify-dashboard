from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# --- 1. LOAD AND PREPARE DATA ---
try:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_PATH = BASE_DIR / "data" / "most-streamed-spotify-songs-2024-clean.csv"
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    try:
        df = pd.read_csv("most-streamed-spotify-songs-2024-clean.csv")
    except FileNotFoundError:
        df = pd.read_csv(Path(__file__).resolve().parent / "most-streamed-spotify-songs-2024-clean.csv")

# Data Cleaning
df = df.fillna(0)
if 'explicit_track' in df.columns:
    df['explicit_label'] = df['explicit_track'].map({0: 'Clean', 1: 'Explicit'})
else:
    df['explicit_label'] = 'Unknown'

METRIC_OPTIONS =[
    {'label': 'Track Score (Overall)', 'value': 'track_score'},
    {'label': 'Spotify Streams', 'value': 'spotify_streams'},
    {'label': 'Spotify Popularity', 'value': 'spotify_popularity'},
    {'label': 'YouTube Views', 'value': 'youtube_views'},
    {'label': 'TikTok Views', 'value': 'tiktok_views'},
    {'label': 'TikTok Posts (User Videos)', 'value': 'tiktok_posts'},
    {'label': 'Apple Music Playlists', 'value': 'apple_music_playlist_count'},
    {'label': 'Airplay Spins (Radio)', 'value': 'airplay_spins'}
]

def get_label(value):
    return next((item['label'] for item in METRIC_OPTIONS if item['value'] == value), value)

# --- 2. INITIALIZE APP ---
app = Dash(__name__)
server = app.server

# --- 3. APP LAYOUT ---
app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'padding': '15px', 'backgroundColor': '#f4f6f9', 'height': '100vh', 'boxSizing': 'border-box'},
    children=[
        html.H2("Producer Insights: Cross-Platform Market Analysis", style={'textAlign': 'center', 'margin': '0 0 5px 0'}),
        html.P("Use the Lasso tool on Chart 1 to highlight tracks. See how they perform in context across other charts.", 
               style={'textAlign': 'center', 'color': '#1DB954', 'fontWeight': 'bold', 'margin': '0 0 15px 0', 'fontSize': '14px'}),
        
        html.Div(
            style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px', 'justifyContent': 'center', 'height': 'calc(100vh - 90px)'},
            children=[
                
                # BOX 1: Master Scatter Plot
                html.Div([
                    html.Div([
                        html.Strong("1. Master Comparison", style={'fontSize':'14px'}),
                        html.Div([
                            dcc.Dropdown(id='s1-y', options=METRIC_OPTIONS, value='track_score', clearable=False, style={'width': '48%', 'fontSize':'12px'}),
                            html.Span(" vs ", style={'paddingTop':'5px', 'fontSize':'12px'}),
                            dcc.Dropdown(id='s1-x', options=METRIC_OPTIONS, value='spotify_popularity', clearable=False, style={'width': '48%', 'fontSize':'12px'})
                        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop':'5px'})
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="master-scatter", style={'height': '280px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px'}),
                
                # BOX 2: Leaderboard (Top 10 Tracks by Selected Metric)
                html.Div([
                    html.Div([
                        html.Strong("2. Leaderboard: Top 10 Tracks", style={'fontSize':'14px'}),
                        dcc.Dropdown(id='dist-metric', options=METRIC_OPTIONS, value='track_score', clearable=False, style={'width': '100%', 'marginTop':'5px', 'fontSize':'12px'})
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="dist-chart", style={'height': '280px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px'}),
                
                # BOX 3: Explicit vs Clean Analysis (dynamic container for multiple chart types)
                html.Div([
                    html.Div([
                        html.Strong([
                            "3. Explicit vs. Clean Analysis ",
                            # Hover Tooltip Icon with Explanation
                            html.Span("ⓘ", 
                                      title="Explicit: Tracks contain strong language or mature themes (Orange). Clean: No explicit content (Purple).",
                                      style={'cursor': 'help', 'color': '#888', 'fontSize': '14px', 'marginLeft': '5px'})
                        ], style={'fontSize':'14px', 'display': 'flex', 'alignItems': 'center'}),
                        # dynamic tool dropdown for chart type selection
                        dcc.Dropdown(
                            id='c3-type', 
                            options=[
                                {'label': '100% Stacked Bar (Proportions)', 'value': 'stacked'},
                                {'label': 'Pie Chart (At-a-Glance Composition)', 'value': 'pie'},
                                {'label': 'Box Plot (Streams Distribution)', 'value': 'box'}
                            ], 
                            value='box', 
                            clearable=False, 
                            style={'width': '100%', 'marginTop':'5px', 'fontSize':'12px'}
                        )
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="explicit-analysis-chart", style={'height': '280px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px'}),
               
                # BOX 4: Playlist Strategy (Count vs Reach)
                html.Div([
                    html.Div([
                        html.Strong("4. Playlist Strategy: Niche vs. Mega-Hits", style={'fontSize':'14px', 'display':'block', 'marginBottom':'5px'}),
                        html.P("Volume of Playlists vs Total Playlist Follower Reach", 
                            style={'fontSize':'11px', 'margin':'0', 'color':'#777'})
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="playlist-scatter", style={'height': '270px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px'})
            ]
        )
    ]
)

# --- 4. CALLBACKS ---

# Callback 1: Master Scatter Plot
@app.callback(
    Output("master-scatter", "figure"),
    [Input("s1-x", "value"), Input("s1-y", "value")]
)
def update_master_scatter(x_col, y_col):
    fig1 = px.scatter(
        df, x=x_col, y=y_col, 
        hover_name="track", hover_data=["artist"],
        color="spotify_popularity", color_continuous_scale="Plasma",
        custom_data=[df.index] 
    )
    fig1.update_layout(
        dragmode="lasso", template="plotly_white", margin=dict(l=30, r=20, t=20, b=20),
        xaxis_title=get_label(x_col), yaxis_title=get_label(y_col)
    )
    return fig1

# Callback 2: Linked Charts
@app.callback([Output("dist-chart", "figure"),
     Output("explicit-analysis-chart", "figure"),
     Output("playlist-scatter", "figure")],[Input("master-scatter", "selectedData"),
     Input("dist-metric", "value"),
     Input("c3-type", "value")]
)
def update_linked_charts(selectedData, dist_metric, c3_type):
    
    # 1. Handle Selection
    if selectedData and 'points' in selectedData:
        selected_indices = [point['customdata'][0] for point in selectedData['points']]
        target_df = df.iloc[selected_indices].copy()
        chart_title_prefix = "Selection"
    else:
        selected_indices = None 
        target_df = df.copy()
        chart_title_prefix = "Global"

    unselected_style = dict(marker=dict(opacity=0.05, color='lightgrey'))
    color_map = {'Clean': '#6A00A8', 'Explicit': '#FCA636'} 

    # ---------------------------------------------------------
    # 2. Dynamic Top 10 Bar Chart (Chart 2)
    # ---------------------------------------------------------
    top_10 = target_df.nlargest(10, dist_metric).copy()
    top_10 = top_10.sort_values(by=dist_metric, ascending=True)
    
    max_chars = 22
    top_10['track_short'] = top_10['track'].apply(lambda x: str(x)[:max_chars] + '...' if len(str(x)) > max_chars else str(x))

    fig2 = px.bar(
        top_10, x=dist_metric, y="track_short", orientation='h',
        text="artist", color=dist_metric, color_continuous_scale=["#3b73b9", "#04295e"], 
        hover_name="track" 
    )
    fig2.update_layout(
        template="plotly_white", margin=dict(l=10, r=20, t=30, b=20),
        xaxis_title=get_label(dist_metric), yaxis_title=None, 
        title=dict(text=f"{chart_title_prefix} Top 10", font=dict(size=12)),
        coloraxis_showscale=False 
    )
    fig2.update_traces(textposition='inside', textfont=dict(color='white'), hovertemplate="<b>%{hovertext}</b><br>Artist: %{text}<br>Value: %{x}<extra></extra>")

    # ---------------------------------------------------------
    # 3. Dynamic Explicit vs Clean Analysis (Chart 3)
    # ---------------------------------------------------------
    if c3_type == 'stacked':
        # 100% Stacked Bar using Plotly Histogram with percent norm
        target_df['Category'] = 'All Tracks' # Dummy column to group them on one bar
        fig3 = px.histogram(
            target_df, y="Category", color="explicit_label", 
            color_discrete_map=color_map, barnorm='percent', orientation='h',
            text_auto='.1f' # Shows the actual percentage text inside the bar
        )
        fig3.update_layout(
            barmode='stack', xaxis_title="Percentage (%)", yaxis_title=None,
            template="plotly_white", margin=dict(l=10, r=20, t=30, b=20),
            title=dict(text=f"{chart_title_prefix} Proportions", font=dict(size=12))
        )
        
    elif c3_type == 'pie':
        # Pie Chart
        counts = target_df['explicit_label'].value_counts().reset_index()
        counts.columns = ['explicit_label', 'count']
        fig3 = px.pie(
            counts, names='explicit_label', values='count', 
            color='explicit_label', color_discrete_map=color_map, hole=0.3
        )
        fig3.update_layout(
            template="plotly_white", margin=dict(l=20, r=20, t=30, b=20),
            title=dict(text=f"{chart_title_prefix} Composition", font=dict(size=12))
        )

    elif c3_type == 'box':
        # Box Plot showing distributions
        fig3 = px.box(
            target_df, x="explicit_label", y="spotify_streams", 
            color="explicit_label", color_discrete_map=color_map, points="all" # Shows individual dots beside the box
        )
        fig3.update_layout(
            template="plotly_white", margin=dict(l=30, r=20, t=30, b=20),
            xaxis_title="Content Rating", yaxis_title="Spotify Streams",
            title=dict(text=f"{chart_title_prefix} Stream Distribution", font=dict(size=12))
        )

    # ---------------------------------------------------------
    # 4. Playlist Strategy Scatter (Chart 4 - Visual Filtering)
    # ---------------------------------------------------------
    fig4 = px.scatter(
        df, x="spotify_playlist_count", y="spotify_playlist_reach",
        hover_name="track", hover_data=["artist"], color="spotify_streams", 
        color_continuous_scale="Plasma", custom_data=[df.index]
    )
    
    if not selected_indices:
        fig4.update_traces(selectedpoints=None, unselected=dict(marker=dict(opacity=0.7)))
    else:
        for trace in fig4.data:
            local_indices =[i for i, df_idx in enumerate(trace.customdata) if df_idx[0] in selected_indices]
            trace.selectedpoints = local_indices
            trace.unselected = unselected_style

    fig4.update_layout(
        template="plotly_white", margin=dict(l=30, r=20, t=20, b=20),
        xaxis_title="Playlist Count (Volume)", yaxis_title="Playlist Reach (Followers)",
        uirevision='constant'
    )

    return fig2, fig3, fig4