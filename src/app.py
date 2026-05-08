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
                        html.Strong("1. Master Comparison (Brush Here)", style={'fontSize':'14px'}),
                        html.Div([
                            dcc.Dropdown(id='s1-y', options=METRIC_OPTIONS, value='tiktok_views', clearable=False, style={'width': '48%', 'fontSize':'12px'}),
                            html.Span(" vs ", style={'paddingTop':'5px', 'fontSize':'12px'}),
                            dcc.Dropdown(id='s1-x', options=METRIC_OPTIONS, value='spotify_streams', clearable=False, style={'width': '48%', 'fontSize':'12px'})
                        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop':'5px'})
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="master-scatter", style={'height': '280px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px'}),
                
                # BOX 2: Leaderboard (Top 10 Tracks by Selected Metric)
                html.Div([
                    html.Div([
                        html.Strong("2. Leaderboard: Top 10 Tracks", style={'fontSize':'14px'}),
                        dcc.Dropdown(id='dist-metric', options=METRIC_OPTIONS, value='spotify_popularity', clearable=False, style={'width': '100%', 'marginTop':'5px', 'fontSize':'12px'})
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="dist-chart", style={'height': '280px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px'}),
                
                # BOX 3: Discovery Engine (Radio vs Organic)
                html.Div([
                    html.Div([
                        html.Strong([
                            "3. Discovery Engine: Radio vs. Shazam ",
                            # Hover Tooltip Icon with Explanation
                            html.Span("ⓘ", 
                                      title="Explicit: Tracks colored in red contain strong language or mature themes. Clean tracks are green.", 
                                      style={'cursor': 'help', 'color': '#888', 'fontSize': '14px', 'marginLeft': '5px'})
                        ], style={'fontSize':'14px'}),
                        html.P("Traditional push (Airplay) vs Organic fan discovery (Shazam)", 
                            style={'fontSize':'11px', 'margin':'0', 'color':'#777'})
                    ], style={'padding': '10px 10px 0 10px'}),
                    dcc.Graph(id="discovery-scatter", style={'height': '280px'})
                ], style={'width': '48%', 'backgroundColor': 'white', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderRadius': '8px'}),
                
                # BOX 4: Playlist Strategy (Count vs Reach)
                html.Div([
                    html.Div([
                        html.Strong([
                            "4. Playlist Strategy: Niche vs. Mega-Hits ",
                            # Hover Tooltip Icon with Explanation
                            html.Span("ⓘ", 
                                      title="Volume: Total number of individual playlists featuring the song.\nFollowers (Reach): The combined audience size of all those playlists.\nTop-Left: Label pushed (huge reach, few playlists).\nBottom-Right: Organic fan growth (many small user playlists).\nLighter yellow dots = higher actual streams.", 
                                      style={'cursor': 'help', 'color': '#888', 'fontSize': '14px', 'marginLeft': '5px'})
                        ], style={'fontSize':'14px', 'display':'block', 'marginBottom':'5px'}),
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

# Callback 1: Only updates Chart 1 when you change the Dropdowns
@app.callback(
    Output("master-scatter", "figure"),[Input("s1-x", "value"), 
     Input("s1-y", "value")]
)
def update_master_scatter(x_col, y_col):
    fig1 = px.scatter(
        df, x=x_col, y=y_col, 
        hover_name="track", hover_data=["artist"],
        color="spotify_popularity", color_continuous_scale="Viridis",
        custom_data=[df.index] # Crucial for linking
    )
    fig1.update_layout(
        dragmode="lasso", template="plotly_white", margin=dict(l=30, r=20, t=20, b=20),
        xaxis_title=get_label(x_col), yaxis_title=get_label(y_col)
    )

    return fig1

@app.callback([Output("dist-chart", "figure"),
     Output("discovery-scatter", "figure"),
     Output("playlist-scatter", "figure")],[Input("master-scatter", "selectedData"),
     Input("dist-metric", "value")]
)
def update_linked_charts(selectedData, dist_metric):
    
    # Extract indices of selected points
    if selectedData and 'points' in selectedData:
        selected_indices = [point['customdata'][0] for point in selectedData['points']]
    else:
        selected_indices = None # None means no active selection

    # Dictionary applied to the scatters to dim unselected points
    unselected_style = dict(marker=dict(opacity=0.05, color='lightgrey'))

    # 2. Dynamic Top 10 Bar Chart
    if selected_indices:
        target_df = df.iloc[selected_indices]
        chart_title = "Top Songs in Selection"
    else:
        target_df = df
        chart_title = "Global Top 10"

    # Get the Top 10 (using .copy() to prevent pandas warnings)
    top_10 = target_df.nlargest(10, dist_metric).copy()
    
    # Sort ascending so the #1 song is at the top of the chart
    top_10 = top_10.sort_values(by=dist_metric, ascending=True)

    # truncate track names for better display, but keep full names in hover
    max_chars = 22
    top_10['track_short'] = top_10['track'].apply(
        lambda x: str(x)[:max_chars] + '...' if len(str(x)) > max_chars else str(x)
    )

    fig2 = px.bar(
        top_10, 
        x=dist_metric, 
        y="track_short", # Use truncated names for display
        orientation='h',
        text="artist", 
        color=dist_metric, 
        color_continuous_scale=["#3b73b9", "#04295e"], 
        hover_name="track" # Pass the full name into the graph for the hover tool
    )
    
    fig2.update_layout(
        template="plotly_white", 
        margin=dict(l=10, r=20, t=30, b=20),
        xaxis_title=get_label(dist_metric), 
        yaxis_title=None, 
        title=dict(text=chart_title, font=dict(size=12)),
        coloraxis_showscale=False 
    )
    
    # Style the text labels inside the bars and the hover box
    fig2.update_traces(
        textposition='inside', 
        textfont=dict(color='white'),
        # This formats the hover box: <b>Full Track Name</b>, Artist, Value. 
        # <extra></extra> hides the ugly secondary "trace" label plotly adds by default.
        hovertemplate="<b>%{hovertext}</b><br>Artist: %{text}<br>Value: %{x}<extra></extra>"
    )

    # 3. Discovery Scatter (Airplay vs Shazam)
    fig3 = px.scatter(
        df, x="airplay_spins", y="shazam_counts", size="spotify_popularity",
        hover_name="track", hover_data=["artist"], color="explicit_label",
        color_discrete_map={'Clean': '#2ca02c', 'Explicit': '#d62728'},
        custom_data=[df.index]
    )
    fig3.update_layout(
        template="plotly_white", margin=dict(l=30, r=20, t=20, b=20),
        xaxis_title="Airplay Spins (Radio)", yaxis_title="Shazams (Organic Discovery)",
        uirevision='constant' # Prevents zoom reset
    )
    fig3.update_traces(selectedpoints=selected_indices, unselected=unselected_style)

    # 4. Playlist Strategy Scatter (Count vs Reach)
    fig4 = px.scatter(
        df, x="spotify_playlist_count", y="spotify_playlist_reach",
        hover_name="track", hover_data=["artist"], color="spotify_streams", 
        color_continuous_scale="Plasma", custom_data=[df.index]
    )
    fig4.update_layout(
        template="plotly_white", margin=dict(l=30, r=20, t=20, b=20),
        xaxis_title="Playlist Count (Volume)", yaxis_title="Playlist Reach (Followers)",
        uirevision='constant' # Prevents zoom reset
    )
    fig4.update_traces(selectedpoints=selected_indices, unselected=unselected_style)

    for fig in [fig3, fig4]:
        if not selected_indices:
            # If nothing is selected, make sure everything is full opacity
            fig.update_traces(selectedpoints=None, unselected=dict(marker=dict(opacity=0.7)))
        else:
            # Loop through every trace in the figure (Clean, Explicit, etc.)
            for trace in fig.data:
                # Find which points in this trace match the global selected indices
                # trace.customdata contains the original DF indices we passed in px.scatter
                local_indices = [
                    i for i, df_idx in enumerate(trace.customdata) 
                    if df_idx[0] in selected_indices
                ]
                # Apply selection to this specific trace
                trace.selectedpoints = local_indices
                trace.unselected = unselected_style

        fig.update_layout(
            template="plotly_white", margin=dict(l=30, r=20, t=20, b=20),
            uirevision='constant'
        )

    return fig2, fig3, fig4