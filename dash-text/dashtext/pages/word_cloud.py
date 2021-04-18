import sys
import os
import logging
import json
import tempfile
import base64

import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(proj_path):
    raise OSError()
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)

import dash_text as pkg
import textnlp
import textnlp.visualization as visualization

logger = logging.getLogger(name=__name__)

TXT = pkg.TXT
JSON = pkg.JSON


def _plot_wordcloud(_id):
    fn = os.path.join(
            textnlp.default_ancillary_dir,
            f"{_id[:-len(TXT)]}{JSON}",
        )
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            counts = json.load(f)
        fig = visualization.plot_wordcloud(counts, os.path.basename(fn))
        tdir = tempfile.TemporaryDirectory()
        fig_fn = os.path.join(tdir.name, 'a.png')
        fig.savefig(fig_fn)

        with open(fig_fn, 'rb') as f:
            bs = f.read()
        bs64 = base64.b64encode(bs)
        src = 'data:image/png;base64,{}'.format(bs64.decode('ascii'))
    else:
        src = ''
    return src


def _plot_bigrams(_id):
    fn = os.path.join(textnlp.default_preprocessed_dir, f"{_id}")
    if os.path.exists(fn) and os.path.isfile(fn):
        with open(fn, 'r') as f:
            text = f.read()
        fig = visualization.plot_bigrams(text)
    else:
        fig = go.Figure()
    return fig


def main(app):
    div_wc = html.Div(id='div_wc')
    div_bigrams = dcc.Graph(id='div_bigrams')

    div_plots = html.Div(
            id='div_plots',
            children=[
                div_wc,
                div_bigrams,
            ],
        )

    @app.callback(
        Output('div_wc', component_property='children'),
        Input('text_dd', 'value'),
    )
    def _update_left_textbox(fbn):
        return (
            html.Img(src=_plot_wordcloud(fbn))
        )

    @app.callback(
        Output('div_bigrams', 'figure'),
        Input('text_dd', 'value'),
    )
    def _plot_bigrams_l(txt):
        return _plot_bigrams(txt)

    return div_plots
