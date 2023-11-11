import plotly.graph_objects as go
import pandas as pd


# Define the ScatterPlot class
class ScatterPlot:
    def __init__(self, df: pd.DataFrame, selected_genre=None):
        # Filter the DataFrame based on the selected genre if provided
        if selected_genre:
            self.df = df[df['track_genre'] == selected_genre]
        else:
            self.df = df

        # Set the title
        title = f'Danceability vs. Energy for {selected_genre or "All Genres"}'

        # Create the figure
        self.fig = go.Figure(
            data=go.Scatter(
                x=self.df['energy'],
                y=self.df['danceability'],
                mode='markers',
                marker=dict(
                    size=10,
                    opacity=0.6,
                    color=self.df['energy'],  # Color scale based on 'energy'
                    colorscale='Viridis',  # You can choose any color scale
                    showscale=True,  # Shows color scale legend
                    line=dict(width=1, color='DarkSlateGrey')
                ),
                text=self.df['track_name'],  # tooltip will show the track name
                hoverinfo='text+x+y'
            ),
            layout=go.Layout(
                title=title,
                xaxis_title='Energy',
                yaxis_title='Danceability',
                hovermode='closest'
            )
        )

    def update(self, df: pd.DataFrame, selected_genre=None):
        # Update the DataFrame based on the selected genre if provided
        if selected_genre:
            updated_df = df[df['track_genre'] == selected_genre]
        else:
            updated_df = df

        # Update the figure's data for energy and danceability
        self.fig.update_traces(
            {'x': updated_df['energy'], 'y': updated_df['danceability']},
            selector=dict(type='scatter')
        )

        # Update the hover text for each point
        self.fig.update_traces(
            {'text': updated_df['track_name']},
            selector=dict(type='scatter')
        )

        # Optionally, update the title if you want it to reflect the new genre
        self.fig.update_layout(
            title=f'Danceability vs. Energy for {selected_genre or "All Genres"}'
        )
