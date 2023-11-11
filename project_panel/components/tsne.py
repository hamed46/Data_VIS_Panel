import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.manifold import TSNE
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
import numpy as np


class TSNEPlot2D:
    def __init__(self, df: pd.DataFrame, perplexity=30, n_clusters=10, **kwargs):
        # Encoding categorical data
        le = LabelEncoder()
        df_enc = df.copy()
        df_enc['track_genre_encoded'] = le.fit_transform(df_enc['track_genre'])

        # Selecting numeric features
        X = df_enc.select_dtypes(include=[np.number])

        # Creating a pipeline for clustering
        self.cluster_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('kmeans', KMeans(n_clusters=n_clusters, random_state=0))
        ])
        self.cluster_pipeline.fit(X)
        df_enc['cluster'] = self.cluster_pipeline['kmeans'].labels_

        # Dimension reduction with t-SNE
        self.tsne_reducer = TSNE(n_components=2, verbose=1, perplexity=perplexity)
        X_proj = self.tsne_reducer.fit_transform(X)

        # Creating the 2D scatter plot using Plotly Express
        self.fig = px.scatter(
            x=X_proj[:, 0],
            y=X_proj[:, 1],
            color=df_enc['cluster'],
            labels={'color': 'Cluster'},
            title='2D t-SNE Music Data Visualization'
        )
        self.fig.update_traces(marker=dict(size=5))
        self.fig.update_layout(**kwargs)

