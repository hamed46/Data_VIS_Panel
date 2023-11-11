import pandas as pd
import plotly.graph_objects as go


class TopGenresHistogram:
    def __init__(self, df: pd.DataFrame) -> None:
        genre_popularity = df.groupby('track_genre').mean()
        sorted_genres = genre_popularity.sort_values(by='popularity', ascending=False)[:10]
        top10_genres = sorted_genres.reset_index()

        self.fig = go.Figure()
        for feature in ['valence', 'energy', 'danceability', 'acousticness']:
            self.fig.add_trace(
                go.Bar(
                    y=top10_genres['track_genre'],
                    x=top10_genres[feature],
                    name=feature,
                    orientation='h'
                )
            )

        self.fig.update_layout(
            barmode='group',
            yaxis_title='Genres',
            xaxis_title='Values',
            title='Top 10 Popular Genres and their Features',
            legend_title='Features',
            yaxis=dict(autorange="reversed", categoryorder='total ascending'),
            xaxis=dict(tickangle=-45),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
