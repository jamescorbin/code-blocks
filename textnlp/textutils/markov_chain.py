"""
"""

import sys
import os
import logging
import collections

import numpy as np

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)
import textnlp as pkg
import data_science_utilities.preprocessing.encoder_ext as encoder_ext

logger = logging.getLogger(name=__name__)


def _encode(tokens, counts, count_thresh=10):
    """
    """
    enc = encoder_ext.LabelEncoderExt(count_thresh=count_thresh)
    enc.fit(counts, from_counts=True)

    enc_tokens = enc.transform(tokens)

    return enc_tokens, enc


def _stack(token_arr, ts_len=3):
    """
    """
    X = []
    Y = token_arr
    for i in range(1, ts_len+1):
        X.append(np.roll(token_arr, ts_len+1-i))
    X = np.array(X).transpose()

    return X, Y


def _transition_matrix(X, Y, ts_len=3):
    """
    """
    T = TransitionMatrix(X, Y)
    return T


class TransitionMatrix():
    """
    """
    DEFAULT = 0

    def __init__(self, X, Y):
        self.T = collections.defaultdict(collections.Counter)
        Xp = list(map(tuple, X))
        for i, x in Xp:
            self.T[x][Y[i]] += 1


    def get(self, x):
        """
        """
        if not isinstance(x, tuple):
            try:
                x = tuple(x)
            except TypeError as e:
                logger.error(e)
        mc = self.T[x].most_common(1)
        if len(mc) > 0:
            val = mc[0][0]
        else:
            #Pass enumerate value of [UNK] here
            val = self.DEFAULT
        return val
