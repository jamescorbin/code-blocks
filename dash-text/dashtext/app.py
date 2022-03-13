"""
Contains global attributes like the Dash app object
    as well as cached data
"""

import logging

import dash

logger = logging.getLogger(name=__name__)


app = dash.Dash(
        __name__,
        update_title=None,
        suppress_callback_exceptions=True,)
server = app.server
cached = dict()
