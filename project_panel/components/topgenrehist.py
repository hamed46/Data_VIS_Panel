import pandas as pd
import plotly.graph_objects as go


class TopGenresHistogram:
    def __init__(self, df: pd.DataFrame) -> None:
        top10_genres = df.nlargest(10, 'popularity')

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
