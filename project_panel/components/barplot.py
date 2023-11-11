import pandas as pd
import plotly.graph_objects as go


class TopTracksHistogram:
    def __init__(self, df: pd.DataFrame) -> None:
        df_unique = df.drop_duplicates(subset=['track_name', 'popularity'])

        top_tracks = df_unique.sort_values(by='popularity', ascending=False).head(10)

        self.fig = go.Figure(
            data=[
                go.Bar(
                    x=top_tracks['popularity'],
                    y=top_tracks['track_name'],
                    orientation='h',
                    marker=dict(color='#1DB954')
                )
            ]
        )
        self.fig.update_layout(
            xaxis_title='Popularity',
            yaxis_title='track_name',
            title='Top 10 Most Listened Tracks',
            yaxis=dict(autorange="reversed")
        )
