import os
import sys
import logging

import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

logger = logging.getLogger(name=__name__)

proj_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
if not os.path.exists(proj_path):
    raise OSError()
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)

import textnlp.gutenberg.gutenberg_dl as gutenberg_dl


def make_div_gutenberg_index(app, df):
    """
    """
    div_index_table = dash_table.DataTable(
        id='div_index_table',
        page_size=20,
        style_cell = dict(
            whiteSpace='normal',
            height='auto'
        ),
        columns=[dict(name=i, id=i) for i in df.columns],
        data=df.to_dict('records'),
    )

    ebook_input = dcc.Input(
        id="ebook_input",
        type='text',
        placeholder='ebook no.',
    )

    confirm_ebook_button = html.Button(
            'Download Text',
            id='confirm_ebook_button',
            n_clicks=0,
    )

    div_ebook_button_dummy = html.Div(id='div_ebook_button_dummy')

    div_download_status = html.Div(
            id='div_download_status',
            children="Awaiting catalogue selection.",
        )

    div_index = (
        html.Div(
            className='section',
            id='div_index',
            children=[
                div_index_table,
                ebook_input,
                confirm_ebook_button,
                div_download_status,
                div_ebook_button_dummy,
            ],
        )
    )

    @app.callback(
        Output("div_ebook_button_dummy", 'children'),
        Output('div_download_status', 'children'),
        [
            Input("confirm_ebook_button", "n_clicks"),
            State("ebook_input", "value"),
        ]
    )
    def download(n_clicks, _id):
        gutenberg_dl.fetch_unpack(_id)
        out_message = (
            f"Succesfully downloaded {_id}"
                if _id is not None else "Awaiting catalogue selection."
        )
        return '', out_message

    return div_index
