import panel as pn
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.io import curdoc
from bokeh.settings import settings
from panel.widgets import Tabulator

from components.artist import ArtistTopTracksBarPlot
from components.barplot import TopTracksHistogram
from components.scatterplot import ScatterPlot
from components.affichage import Table
from components.dataread import read_csv
from components.heatmap import Heatmap
from components.radarplot import RadarChart
from components.scatterplot1 import ScatterPlot1
from components.scatterplot2 import ScatterPlot2
from components.topgenrehist import TopGenresHistogram

settings.resources = 'cdn'
settings.resources = 'inline'

pn.extension(sizing_mode="stretch_width")
with open('templates/dashboard.jinja2', 'r') as html:
    template = pn.Template('\n'.join(html.readlines()))
template.add_variable('app_title', 'Genre Track Data Visualization')

dataset = read_csv('data/dataset.csv')
features_for_radar = ['danceability', 'energy', 'valence', 'tempo', 'liveness']

liste = ['artists', 'album_name', 'track_name', 'popularity', 'duration_ms', 'danceability', 'energy', 'loudness',
         'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo', 'liveness', 'track_genre']

data = Table(dataset.reset_index(names=''), liste, title='Dataset Exploration',
             height=600)

# Nos Figures
artist = ArtistTopTracksBarPlot(dataset, 'XXXTENTACION')
top_genres_histogram = TopGenresHistogram(df=dataset)
barplot = TopTracksHistogram(dataset)
scatter = ScatterPlot(dataset, 'acoustic')
scatter1 = ScatterPlot1(dataset, 'acoustic')
scatter2 = ScatterPlot2(dataset, 'acoustic')
radar_chart = RadarChart(dataset, features_for_radar)
heatmap = Heatmap(dataset)

df = dataset[dataset['artists'].str.contains(r'^\b\w+\b$', regex=True, na=False)]

selectors_dict = {

    'Artists': ['All'] + ['2Pac', '6ix9ine', 'ADELE', 'BLACKPINK', 'BTS', 'Dio', 'Eminem', 'Future', 'GIMS', 'ICO',
                          'Indila', 'Sia', 'Wizkid', 'XXXTENTACION'],  # df['artists'].unique().tolist(),
    'Album': ['All'] + ['Anchor', 'Bad Liar', 'Bad Love', 'Beautiful Disaster', 'Black Bear', 'Golden Hour', 'Hold On',
                        'La Negra', 'The Soul', 'Without Me'],  # dataset['album_name'].unique().tolist(),
    'Genre': ['All'] + dataset['track_genre'].unique().tolist()[:10],
}

selectors = [pn.widgets.Select(name=name, options=options) for name, options in selectors_dict.items()]

widgets = [
    *selectors,

]


# Modifications
@pn.depends(*selectors, watch=True)
def filter(*selectors):
    # subset = dataset.copy()
    subset = selectors[0] if selectors[0] != 'All' else 'XXXTENTACION'
    subset2 = selectors[2] if selectors[2] != 'All' else 'acoustic'

    artist.update(dataset, subset)
    scatter.update(dataset, subset2)
    scatter1.update(dataset, subset2)
    scatter2.update(dataset, subset2)


# Ajout des graphiques à notre dashboars
template.add_panel('sidebar', pn.Column(*widgets, css_classes=''.split()))
template.add_panel('data', data.fig)
template.add_panel('barplot', barplot.fig)
template.add_panel('genrehist', top_genres_histogram.fig)
template.add_panel('artist', artist.fig)
template.add_panel('heatmap', heatmap.fig)
template.add_panel('scatter', scatter.fig)
template.add_panel('scatter1', scatter1.fig)
template.add_panel('scatter2', scatter2.fig)
template.add_panel('radar_chart', radar_chart.fig)

template.servable()
