import panel as pn

pn.extension(sizing_mode="stretch_width")
with open('templates/index.html', 'r') as html:
    template = pn.Template('\n'.join(html.readlines()))

template.servable()
