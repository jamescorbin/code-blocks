import os
import sys
import json
import base64
import tempfile

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

gutenberg_proj = "/home/jamescorbin/GIT/code_blocks"
if not os.path.exists(gutenberg_proj):
    raise OSError()
sys.path.insert(1, gutenberg_proj)
import textnlp.gutenberg
import textnlp.gutenberg.gutenberg_index as gutenberg_index
import textnlp.gutenberg.gutenberg_dl as gutenberg_dl
import textnlp.gutenberg.load_text as load_text
import textnlp.visualization as visualization

import plotly.graph_objects as go

import div_index_header
import div_text_display

import matplotlib.pyplot as plt

JSON = '.json'
TXT = '.txt'
text_dir = "/home/jamescorbin/Desktop/texts"
text_dir = os.path.join(text_dir, "ascii")
text_files = os.listdir(text_dir)


def _plot_wordcloud(_id):
    fn = os.path.join(textnlp.default_ancillary_dir, f"{_id[:-len(TXT)]}{JSON}")
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


app = dash.Dash(
        __name__,
        update_title=None,
    )


def main():
    """
    """
    df = gutenberg_index.load_index()

    div_index = div_index_header.make_div_gutenberg_index(df)

    div_columns = div_text_display.main(app)

    div_wc_l = html.Div(id='div_wc_l')

    @app.callback(
        Output('div_wc_l', component_property='children'),
        Input('text-dd-l', 'value'),
    )
    def _update_left_textbox(fbn):
        return (
            html.Img(src=_plot_wordcloud(fbn))
        )

    div_wc_r = html.Div(id='div_wc_r')

    @app.callback(
        Output('div_wc_r', component_property='children'),
        Input('text-dd-r', 'value'),
    )
    def _update_left_textbox(fbn):
        return (
            html.Img(src=_plot_wordcloud(fbn))
        )

    div_bigrams_l = dcc.Graph(id='div_bigrams_l')

    @app.callback(
        Output('div_bigrams_l', 'figure'),
        Input('text-dd-l', 'value'),
    )
    def _plot_bigrams_l(txt):
        return _plot_bigrams(txt)



    app.layout = (
        html.Div(
            id='body',
            children=[
                div_index,
                div_columns,
                div_wc_l,
                div_wc_r,
                div_bigrams_l,
            ],
        )
    )





if __name__ == '__main__':
    main()
    app.run_server(debug=True)
