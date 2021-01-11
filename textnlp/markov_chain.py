"""
"""

import sys
import os
import logging

import numpy as np

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)
import textnlp as pkg
import data_science_utilities.preprocessing.encoder_ext as encoder_ext

logger = logging.getLogger(name=__name__)


def _encode(tokens, counts):
    """
    """
    enc = encoder_ext.LabelEncoderExt(count_thresh=10)
    enc.fit(counts, from_counts=True)

    enc_tokens = enc.transform(text)

    return enc_tokens, enc


def _stack(token_arr, ts_len=3):
    """
    """
    X = []
    Y = token_arr
    for i in range(1, ts_len+1):
        X.append(np.roll(token_arr, i))

    return X, Y
