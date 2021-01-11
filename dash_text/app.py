import os
import sys
import logging
import filecmp

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
import dash_text.pages.catalogue_index as catalogue_index
import dash_text.pages.text_window as text_window
import dash_text.pages.word_cloud as word_cloud
import textnlp.gutenberg.gutenberg_index as gutenberg_index

css_dir = pkg.css_dir
asset_dir = pkg.asset_dir

logger = logging.getLogger(name=__name__)


def update_css(css_dir):
    match, mismatch, error = (
        filecmp.cmpfiles(css_dir, asset_dir, os.listdir(css_dir))
    )
    to_copy = mismatch+error
    if len(to_copy) > 0:
        import shutil
    for bn in to_copy:
        src = os.path.join(css_dir, bn)
        dst = os.path.join(asset_dir, bn)
        shutil.copy(src, dst)
        logger.info(f"Copied {src} to {dst}.")

update_css(css_dir)

app = dash.Dash(
        __name__,
        update_title=None,
        suppress_callback_exceptions=True,
    )


def main():
    """
    """
    df = gutenberg_index.load_index()
    div_index = catalogue_index.make_div_gutenberg_index(app, df)
    div_text = text_window.main(app)
    div_word_cloud = word_cloud.main(app)

    catalogue_tab = dcc.Tab(
            id="catalogue_tab",
            label="Catalogue",
            value='tab-1',
        )
    text_window_tab = dcc.Tab(
            id="text_window_tab",
            label="View Text",
            value="tab-2",
        )
    top_tabs = dcc.Tabs(
            id='top_tabs',
            children=[
                catalogue_tab,
                text_window_tab,
                dcc.Tab(label='Markov Text', value='tab-3')
            ],
        )
    tabs_content = html.Div(id='tabs_content')

    app.layout = (
        html.Div(
            id='body',
            children=[
                top_tabs,
                tabs_content,
            ],
        )
    )

    @app.callback(
        Output('tabs_content', 'children'),
        Input('top_tabs', 'value'),
    )
    def render_content(tab):
        if tab=='tab-1':
            return div_index
        elif tab=='tab-2':
            #return div_text
            return html.Div(children=[div_text, div_word_cloud])
        else:
            return html.Div('hello world')


if __name__ == '__main__':
    main()
    app.run_server(debug=True)
