import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import umap.umap_ as umap
import plotly.graph_objects as go
from sklearn.cluster import KMeans


class UMAPPlot:
    def __init__(self, df: pd.DataFrame, n_neighbors=15, n_clusters: int = 2, **kwargs) -> None:
        # Encoding categorical data
        le = LabelEncoder()
        df_enc = df.copy()
        df_enc['track_genre_encoded'] = le.fit_transform(df_enc['track_genre'])

        # Selecting and scaling features
        features_to_scale = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                             'instrumentalness', 'liveness', 'valence', 'tempo']
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_enc[features_to_scale])

        # Dimension reduction with UMAP
        reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=0.1, metric='euclidean', n_components=3)
        X_proj = reducer.fit_transform(df_scaled)

        # Clustering with KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto').fit(df_scaled)

        # Creating the 3D scatter plot using Plotly
        self.fig = go.Figure(
            data=go.Scatter3d(
                x=X_proj[:, 0],
                y=X_proj[:, 1],
                z=X_proj[:, 2],
                customdata=df.values,
                hovertemplate=(
                    'Track Name = <b>%{customdata[1]}</b><br>'
                    'Artists = <b>%{customdata[2]}</b><br>'
                    'Album Name = <b>%{customdata[3]}</b><br>'
                    'Popularity = <b>%{customdata[7]}</b><br>'
                    'Genre = <b>%{customdata[8]}</b><br>'
                    '<extra></extra>'
                ),
                hoverlabel=dict(
                    font_size=12,
                    font_family='montserrat'
                ),
                marker=dict(
                    color=kmeans.labels_,
                    size=5,
                    # colorscale=px.colors.qualitative.Plotly,
                    showscale=True
                ),
                mode='markers'
            )
        )
        self.fig.update_layout(
            **kwargs,
            font_family='montserrat',
            title_font={'size': 20},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            scene=dict(
                xaxis=dict(showticklabels=False),
                yaxis=dict(showticklabels=False),
                zaxis=dict(showticklabels=False)
            ),
        )

    def update(self, df: pd.DataFrame, n_neighbors: int):
        le = LabelEncoder()
        df_enc = df.copy()
        df_enc['track_genre_encoded'] = le.fit_transform(df_enc['track_genre'])

        # Selecting and scaling features
        features_to_scale = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                             'instrumentalness', 'liveness', 'valence', 'tempo']
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_enc[features_to_scale])
        reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=0.1, metric='euclidean', n_components=3)
        X_proj = reducer.fit_transform(df_scaled)
        # kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto').fit(df_scaled)
        self.fig.update_traces(
            x=X_proj[:, 0],
            y=X_proj[:, 1],
            z=X_proj[:, 2],
            selector=dict(type='scatter')
        )
