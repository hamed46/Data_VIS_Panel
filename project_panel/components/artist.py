import plotly.graph_objects as go
import pandas as pd


class ArtistTopTracksBarPlot:
    def __init__(self, df: pd.DataFrame, artist_name: str):
        self.df = df[df['artists'].str.contains(artist_name, case=False, na=False)]

        artist_tracks_unique = self.df.drop_duplicates(subset=['track_name'])

        top_tracks = artist_tracks_unique.sort_values(by='popularity', ascending=False).head(10)

        title = f'Top Tracks for {artist_name}'

        # Create the figure for a bar plot
        self.fig = go.Figure(
            data=go.Bar(
                x=top_tracks['popularity'],
                y=top_tracks['track_name'],
                orientation='h',
                marker=dict(color='#1DB954')
            ),
            layout=go.Layout(
                title=title,
                xaxis_title='Popularity',
                yaxis_title='Track Name',
                yaxis=dict(autorange="reversed")
            )
        )

    def update(self, df: pd.DataFrame, artist_name: str):

        self.df = df[df['artists'].str.contains(artist_name, case=False, na=False)]

        artist_tracks_unique = self.df.drop_duplicates(subset=['track_name', 'popularity'])

        top_tracks = artist_tracks_unique.sort_values(by='popularity', ascending=False).head(10)

        self.fig.update_traces(
            {'x': top_tracks['popularity'], 'y': top_tracks['track_name']},
            selector=dict(type='bar')
        )

        self.fig.update_layout(
            title=f'Top Tracks for {artist_name}'
        )
