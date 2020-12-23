import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go



def make_div_gutenberg_index(df):
    """
    """
    table = (
        go.Table(
            header=dict(values=df.columns),
            cells=dict(values=df.iloc[:200].values.T.tolist()),
        )
    )
    go_table = go.Figure(data=table)
    div_go_table = dcc.Graph(id='go_table', figure=go_table)

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

    div_text_files = (
        html.Div(
            id='div_text_files',
            children="",
            hidden=True,
        )
    )

    div_index = (
        html.Div(
            className='section',
            id='div_index',
            children=[
                div_go_table,
                div_index_table,
                #fig_div,
                ebook_input,
                confirm_ebook_button,
                div_ebook_button_dummy,
                div_text_files,
            ],
        )
    )

    return div_index
