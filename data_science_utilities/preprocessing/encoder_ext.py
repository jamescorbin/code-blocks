"""
An extension to sklearn.preprocessing.LabelEncoder
that safely handles an unknown word represented by ${UNK}
in the encoded classes.

Attributes:
    LabelEncoderExt (class):

TODO:
    Add ${top_n} encoding.
"""

import logging

import numpy as np
import sklearn.preprocessing

log = logging.getLogger(name=__name__)

UNK = "[UNK]"
RANK = "rank"
NUMBER = "number"
FREQUENCY = "frequency"
STRLEN = "U20"


class LabelEncoderExt(sklearn.preprocessing.LabelEncoder):
    """
    """

    def __init__(self, top_n=None, count_thresh=None, freq_thresh=None):
        """
        """
        super(LabelEncoderExt, self).__init__()
        if top_n is not None:
            self.criterion = RANK
            try:
                self.c_value = int(top_n)
            except ValueError as e:
                log.error(e)
        elif count_thresh is not None:
            self.criterion = NUMBER
            try:
                self.c_value = int(count_thresh)
            except ValueError as e:
                log.error(e)
        elif freq_thresh is not None:
            self.criterion = FREQUENCY
            try:
                self.c_value = float(freq_thresh)
            except ValueError as e:
                log.error(e)
        else:
            self.criterion = ""
            self.c_value = None


    def fit(self, x, from_counts=False):
        """
        """
        if from_counts:
            y = []
            if isinstance(x, dict):
                y = np.array(
                        [k for k, v in x.items() if v>=self.c_value]
                    )
            else:
                raise TypeError("Must pass dictionary of counts.")
        else:
            try:
                x = np.array(x)
            except ValueError as e:
                log.error(e)
            assert (len(x.shape)==1), "Require 1D array"

            x = x.astype(str)

            unique_elem, unique_indices, elem_locs, elem_counts = (
                np.unique(
                    x,
                    return_index=True,
                    return_inverse=True,
                    return_counts=True,
                )
            )

            y = np.full(x.shape, "", dtype=STRLEN)

            if self.criterion == RANK:
                a = np.argpartition(elem_counts, self.c_value)
                for t in a:
                    y[np.where(elem_locs==t)] = unique_elem[t]
            elif self.criterion == NUMBER:
                for i, t in np.ndenumerate(elem_counts):
                    if t >= self.c_value:
                        y[np.where(elem_locs==i)] = unique_elem[i]
            elif self.criterion == FREQUENCY:
                for i, t in np.ndenumerate(elem_counts):
                    if t/x.shape[0] >= self.c_value:
                        y[np.where(elem_locs==i)] = unique_elem[i]
            else:
                y = x
            y[np.where(y=="")] = UNK

        y = np.concatenate((y, np.array([UNK])))
        super(LabelEncoderExt, self).fit(y)

        return 0


    def transform(self, x, **kwargs):
        """
        """
        try:
            x = np.array(x)
        except ValueError as e:
            log.error(e)
        x = x.astype(str)
        x[~np.isin(x, self.classes_)] = UNK

        return super(LabelEncoderExt, self).transform(x)


    def fit_transform(self, x, **kwargs):
        """
        """
        self.fit(x, **kwargs)

        return self.transform(x, **kwargs)


class OrdinalEncoderExt(sklearn.preprocessing.OrdinalEncoder):
    """
    """

    def __init__(self,
                 top_n=None,
                 count_thresh=None,
                 freq_thresh=None,
                 categories="auto",
                 **kwargs,
    ):
        """
        """
        super(OrdinalEncoderExt, self).__init__(
            categories=categories,
            **kwargs
        )
        if top_n is not None:
            self.criterion = RANK
            try:
                self.c_value = int(top_n)
            except ValueError as e:
                log.error(e)
        elif count_thresh is not None:
            self.criterion = NUMBER
            try:
                self.c_value = int(count_thresh)
            except ValueError as e:
                log.error(e)
        elif freq_thresh is not None:
            self.criterion = FREQUENCY
            try:
                self.c_value = float(freq_thresh)
            except ValueError as e:
                log.error(e)
        else:
            self.criterion = ""
            self.c_value = None


    def fit(self, X):
        """
        """
        try:
            X = np.array(X)
        except ValueError as e:
            log.error(e)
        assert (len(X.shape)==2), "Require 2D array"

        X = X.astype(str)

        Y = np.full(X.shape, "", dtype=STRLEN)
        for j in range(X.shape[1]):
            unique_elem, unique_indices, elem_locs, elem_counts = (
                np.unique(
                    X[:, j],
                    return_index=True,
                    return_inverse=True,
                    return_counts=True,
                )
            )

            if self.criterion == RANK:
                a = np.argpartition(elem_counts, self.c_value)
                for t in a:
                    Y[np.where(elem_locs==t), j] = unique_elem[t]
            elif self.criterion == NUMBER:
                for i, t in np.ndenumerate(elem_counts):
                    if t >= self.c_value:
                        Y[np.where(elem_locs==i), j] = unique_elem[i]
            elif self.criterion == FREQUENCY:
                for i, t in np.ndenumerate(elem_counts):
                    if t/X.shape[0] >= self.c_value:
                        Y[np.where(elem_locs==i), j] = unique_elem[i]
            else:
                Y[:, j] = X[:, j]
            Y[np.where(Y[:, j]==''), j] = UNK

        tmp = np.full(X.shape[1], UNK).reshape((1, -1))
        Y = np.append(Y, tmp, axis=0)

        super(OrdinalEncoderExt, self).fit(Y)

        return 0


    def transform(self, X):
        """
        """
        X = X.astype(str)
        for i in range(X.shape[1]):
            X[~np.isin(X[:, i], self.categories_[i]), i] = UNK

        return super(OrdinalEncoderExt, self).transform(X)


    def fit_transform(self, X):
        """
        """
        self.fit(X)

        return self.transform(X)
