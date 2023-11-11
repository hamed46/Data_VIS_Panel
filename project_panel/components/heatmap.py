import pandas as pd
import plotly.graph_objects as go
import numpy as np
from sklearn import preprocessing
from collections import defaultdict


class Heatmap:
    def __init__(self, df: pd.DataFrame) -> None:
        d = defaultdict(preprocessing.LabelEncoder)
        # Only select columns with numerical data
        numerical_df = df.select_dtypes(include=[np.number])
        # Apply LabelEncoder to each column
        numerical_df = numerical_df.apply(lambda x: d[x.name].fit_transform(x))
        self.corr = numerical_df.corr()
        self.fig = go.Figure(
            data=go.Heatmap(
                x=self.corr.index,
                y=self.corr.columns,
                z=self.corr.values,
                type='heatmap',
                colorscale='blues',
                zmin=0,
                zmax=1,
                showscale=False,
                hovertemplate='%{z}<extra></extra>',
                hoverlabel=dict(
                    bgcolor='rgba(49, 99, 149, 1.)',
                    font_size=12,
                    font_family='montserrat'
                )
            ),
        )
        self.fig.update_layout(
            title='Correlation Map',
            title_font={'size': 20, 'family': 'montserrat'},
            width=1000,
            height=600,
            yaxis=dict(
                tickfont=dict(size=12, family='montserrat'),
                tickangle=0
            ),
            xaxis=dict(
                tickfont=dict(size=12, family='montserrat'),
            ),
        )
        # Adjust font size of the annotations if present
        if hasattr(self.fig.layout, 'annotations'):
            for i in range(len(self.fig.layout.annotations)):
                self.fig.layout.annotations[i].font.size = 20
