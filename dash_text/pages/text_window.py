import os
import sys
import logging
import json
import base64

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

proj_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
if not os.path.exists(proj_path):
    raise OSError()
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)

logger = logging.getLogger(name=__name__)

import dash_text as pkg
import textnlp.gutenberg
import textnlp.gutenberg.load_text as load_text

text_dir = pkg.text_dir


def _fetch_data(fbn, text_dir):
    """
    """
    fn = os.path.join(text_dir, fbn)
    if os.path.exists(fn) and len(fbn) > 0:
        with open(fn, 'r') as f:
            text = f.read()
    else:
        text = "Select text."
    return text


def main(app):
    """
    """
    div_text_files = html.Div(
            id='div_text_files',
            children=os.listdir(text_dir),
            hidden=True,
        )

    div_text_dir = html.Div(
            id='div_text_dir',
            children=text_dir,
            hidden=True,
        )

    text_dd = dcc.Dropdown(
            id='text_dd',
            value='',
            options=[
                {'label': x, 'value': x}
                for x in os.listdir(text_dir)
            ],
        )

    div_dd_wrapper = html.Div(
            id="div_dd_wrapper",
            children=text_dd,
        )

    textbox = dcc.Textarea(
            id='textbox',
            style={'width': '100%', 'height': 300},
#            cols=80,
#            rows=40,
            value='Select text.',
        )

    columns = html.Div(
            id='div_columns',
            children=[
                div_dd_wrapper,
                div_text_dir,
                div_text_files,
                textbox,
            ],
        )

    @app.callback(
        Output('div_dd_wrapper', 'children'),
        Input('div_text_files', 'children'),
        State('div_text_dir', 'children')
    )
    def _update_book_dd(_, tdir):
        text_files = os.listdir(tdir)
        return (
            dcc.Dropdown(
                id='text_dd',
                value='',
                options=[{'label': x, 'value': x} for x in text_files],
            )
        )

    @app.callback(
        Output(component_id='textbox', component_property='value'),
        Input('text_dd', 'value'),
        State('div_text_dir', 'children'),
    )
    def _update_textbox(fbn, txt_dir):
        return _fetch_data(fbn, txt_dir)

    return columns
