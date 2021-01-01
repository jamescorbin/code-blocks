import os
import sys
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

import dash_text as pkg
import textnlp.gutenberg
import textnlp.gutenberg.load_text as load_text

text_dir = pkg.text_dir


def _fetch_data(fbn):
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
    div_text_files = (
        html.Div(
            id='div_text_files',
            children="",
            hidden=True,
        )
    )

    div_text_dir = (
        html.Div(
            id='div_text_dir',
            children=text_dir,
            hidden=True,
        )
    )

    div_dd_wrapper = [
        html.Div(
            id="div_dd_wrapper_0",
            children=(
                dcc.Dropdown(
                    id='text-dd-l',
                    value='',
                    options=[
                        {'label': x, 'value': x}
                        for x in os.listdir(text_dir)
                    ],
                )
            )
        ),
        html.Div(id="div_dd_wrapper_1",
            children=(
                dcc.Dropdown(
                    id='text-dd-r',
                    value='',
                    options=[
                        {'label': x, 'value': x}
                        for x in os.listdir(text_dir)
                    ],
                )
            )
        ),
    ]

    @app.callback(
        Output('div_dd_wrapper_0', 'children'),
        Output('div_dd_wrapper_1', 'children'),
        Input('div_text_files', 'children'),
        State('div_text_dir', 'children')
    )
    def _update_book_dd(_, tdir):
        text_files = os.listdir(tdir)
        return (
            dcc.Dropdown(
                id='text-dd-l',
                value='',
                options=[{'label': x, 'value': x} for x in text_files],
            ),
            dcc.Dropdown(
                id='text-dd-r',
                value='',
                options=[{'label': x, 'value': x} for x in text_files],
            ),
        )

    textboxes = [
        dcc.Textarea(
            id='textbox_l',
            rows=20,
            cols=80,
        ),
        dcc.Textarea(
            id='textbox_r',
            rows=20,
            cols=80,
        ),
    ]

    @app.callback(
        Output(component_id='textbox_l', component_property='value'),
        Input('text-dd-l', 'value'),
    )
    def _update_left_textbox(fbn):
        return (
            _fetch_data(fbn)
        )

    @app.callback(
        Output(component_id='textbox_r', component_property='value'),
        Input('text-dd-r', 'value'),
    )
    def _update_right_textbox(fbn):
        return _fetch_data(fbn)


    coll = (
        html.Div(
            className='column',
            children=[
                html.Div(id='lt', children='Left'),
                div_dd_wrapper[0],
                textboxes[0],
            ],
        )
    )

    colr = (
        html.Div(
            className='column',
            children=[
                html.Div(id='rt', children='Right'),
                div_dd_wrapper[1],
                textboxes[1],
            ],
        )
    )

    columns = (
        html.Div(
            id='div_columns',
            children=[
                div_text_dir,
                coll,
                colr,
            ],
        )
    )


    return columns
