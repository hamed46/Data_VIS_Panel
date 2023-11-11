import panel as pn
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.io import curdoc
from bokeh.settings import settings
from panel.widgets import Tabulator

from components.affichage import Table
from components.dataread import read_csv
from components.tsne import TSNEPlot2D
from components.umaplot import UMAPPlot
from components.recommendation import MusicRecommender

settings.resources = 'cdn'
settings.resources = 'inline'

pn.extension(sizing_mode="stretch_width")
with open('templates/ml.jinja2', 'r') as html:
    template = pn.Template('\n'.join(html.readlines()))
template.add_variable('app_title', 'Music Track Data Visualization')

dataset = read_csv('data/dataset.csv')

# Nos Figures
recommender = MusicRecommender('data/dataset.csv')
hybrid = recommender.content_based_recommendations('Sad')
hybrid_data = Table(hybrid, title='Recommendation',
                    height=600)

#tsne_plot_2d = TSNEPlot2D(dataset)
music_umap_plot = UMAPPlot(df=dataset, n_neighbors=15, n_clusters=5, title='3D UMAP Visualization with Clustering')

recommendation = {

    'Types of recommendation systems': ['Default'] + ['hybrid_recommendations', 'content_based_recommendations'],
    'Title Listened': ['Default'] + ['Bad Liar', 'Hold On', 'Sad', 'Mask Off', "I'm Good (Blue)", 'Bella', 'Rap God',
                                     'Dynamite', 'Dernière danse', 'GOOBA'],
}
sliders = [
    pn.widgets.IntSlider(name='Number of recommendations', start=5, end=20, step=1, value=5, bar_color='#316395',
                         height=50),
    pn.widgets.IntSlider(name='Number of neighbors', start=5, end=20, step=1, value=10, bar_color='#316395',
                         height=50),
]
selectors = [pn.widgets.Select(name=name, options=options) for name, options in recommendation.items()]
spinner = pn.indicators.LoadingSpinner(value=True, width=25, height=25, bgcolor='light', color='success', visible=False)
button = pn.widgets.Button(name='Update', button_type='primary')
widgets = [
    *selectors,
    *sliders,
    button,
]


@pn.depends(*selectors, sliders[0], sliders[1], watch=True)
def filter(*selectors):
    subset = selectors[0] if selectors[0] != 'Default' else 'content_based_recommendations'
    subset1 = selectors[1] if selectors[1] != 'Default' else 'Sad'

    if subset == 'content_based_recommendations':
        hd = recommender.content_based_recommendations(subset1, sliders[0].value)
    else:
        hd = recommender.hybrid_recommendations(subset1, sliders[0].value)

    hybrid_data.update(hd)
    # music_umap_plot.update(dataset, sliders[1].value)


@pn.depends(button, watch=True)
def filter_umap(button):
    spinner.visible = True
    music_umap_plot.update(dataset, sliders[1].value)
    spinner.visible = False


# Ajout des graphiques à notre dashboars
template.add_panel('sidebar', pn.Column(*widgets, css_classes=''.split()))
template.add_panel('data', hybrid_data.fig)
template.add_panel('umap', music_umap_plot.fig)
# template.add_panel('tsne', tsne_plot_2d.fig)

template.servable()
