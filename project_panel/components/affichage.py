import pandas as pd
import plotly.graph_objects as go


class Table:
    def __init__(self, df: pd.DataFrame, header: list = None, selected_row=None, **kwargs) -> None:
        header_vals = header if header else [f'<b>{col}</b>' for col in df.columns]
        df = df.copy()
        if header:
            df = df[header]
        df.iloc[:, 0] = df.iloc[:, 0].apply(lambda v: f'<b>{v}</b>')

        # Determine cell fill colors
        fill_colors = ['rgba(49, 99, 149, .2)' if i != selected_row else 'rgba(255, 255, 0, .5)' for i in
                       range(len(df))]

        self.fig = go.Figure(
            data=[go.Table(
                header=dict(
                    values=header_vals,
                    fill_color='rgba(49, 99, 149, 1.)',
                    align='left',
                    font=dict(color='white', size=12),
                ),
                cells=dict(
                    values=[df[col].astype(str) for col in df.columns],
                    align='left',
                    font=dict(size=12, color='black', family='Arial'),
                    height=30,
                    fill_color=fill_colors,
                )
            )
            ])
        self.fig.update_layout(
            **kwargs,
            title_font={'size': 20, 'color': 'black', 'family': 'Arial'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

    def update(self, df):
        self.fig.update_traces(
            header=dict(values=list(df.columns)),
            cells=dict(values=[df[col] for col in df.columns]),
        )
