import pandas as pd
import plotly.graph_objects as go
from sklearn import preprocessing


class RadarChart:
    def __init__(self, df: pd.DataFrame, features: list) -> None:
        # Normalisation des caractéristiques
        min_max_scaler = preprocessing.MinMaxScaler()
        df[features] = min_max_scaler.fit_transform(df[features])

        # Identification de la piste la plus et la moins populaire
        self.most_popular_track = df.loc[df['popularity'].idxmax()]
        self.least_popular_track = df.loc[df['popularity'].idxmin()]

        # Valeurs pour les pistes les plus et les moins populaires
        values_most_popular = self.most_popular_track[features].tolist()
        values_least_popular = self.least_popular_track[features].tolist()

        # Création du graphique radar
        self.fig = go.Figure(
            data=[
                go.Scatterpolar(
                    r=values_most_popular,
                    theta=features,
                    fill='toself',
                    name='Most Popular Track'
                ),
                go.Scatterpolar(
                    r=values_least_popular,
                    theta=features,
                    fill='toself',
                    name='Least Popular Track'
                )
            ]
        )
        self.fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title='Comparison of Most and Least Popular Tracks'
        )
