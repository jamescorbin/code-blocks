"""
"""

import os
import sys
import re
import logging
import collections

import numpy as np
import matplotlib
import wordcloud
import plotly.graph_objects as go

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)
import textnlp as pkg


def plot_wordcloud(counts, title='', wc_size=(12, 12)):
    """
    """
    try:
        counts.pop('.')
    except:
        pass
    try:
        counts.pop('p')
    except:
        pass
    sm = sum(counts.values())
    frequency_dict = {k: v/sm for k, v in counts.items()}

    wc = (
        wordcloud.WordCloud(
            width=1000, height=1000,
            background_color='white',
            min_font_size=10
        ).generate_from_frequencies(frequency_dict)
    )
    fig = matplotlib.figure.Figure(figsize=wc_size, facecolor=None)
    fig.suptitle("Wordcloud")
    ax = fig.add_subplot()
    ax.set_title(f"{title}")
    _ = ax.imshow(wc)

    return fig


def plot_bigrams(text, title='', take=100, **kwargs):
    """
    """
    tokens = text.split('\n')
    counts = (
        collections.Counter(
            [' '.join((tokens[i], tokens[i+1]))
                for i in range(len(tokens)-1)
                if tokens[i] != '.' and tokens[i+1] != '.'
        ])
    )

    select = counts.most_common(take)
    bigrams, values = zip(*select)

    fig = go.Figure()
    bar = go.Bar(
            name=title,
            x=list(bigrams),
            y=list(values),
        )
    fig.add_trace(bar)
    fig.update_layout(barmode='group')

    fig.update_layout(
        go.Layout(
            xaxis = dict(rangeslider={'visible': True}),
            width=1200,
            height=800,
            paper_bgcolor="LightSteelBlue",
        )
    )
    return fig

