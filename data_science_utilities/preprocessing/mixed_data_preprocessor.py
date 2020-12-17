"""
"""

import os
import sys
import logging

import pandas as pd
import sklearn
import sklearn.preprocessing

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
import encoder_ext

log = logging.getLogger(name=__name__)


class MixedDataPreprocessor(sklearn.base.TransformerMixin):
    """
    """
    
    def __init__(self, categorical_columns, continuous_columns, **kwargs):
        """
        """
        self.categorical_columns = categorical_columns
        self.continuous_columns = continuous_columns
        self.enc = encoder_ext.OrdinalEncoderExt(**kwargs)
        self.scl = sklearn.preprocessing.StandardScaler()
        self.y_scl = sklearn.preprocessing.StandardScaler()
        
        
    def fit(self, X, y=None):
        """
        """
        cat_feats = self.categorical_columns
        cont_feats = self.continuous_columns
        
        cont_data = X[cont_feats]
        cat_data = X[cat_feats].fillna("")
        
        self.scl.fit(cont_data.values)
        self.enc.fit(cat_data.values)
        
        if y is not None:
            self.y_scl.fit(y)

        return 0 
    
    
    def transform(self, X, y=None):
        """
        """
        cat_feats = self.categorical_columns
        cont_feats = self.continuous_columns
        
        cont_data = X[cont_feats]

        cont_vals = pd.DataFrame(
            self.scl.transform(cont_data.values),
            columns=cont_data.columns,
        )
        
        cat_data = X[cat_feats].fillna("")

        cat_vals = (
            pd.DataFrame(
                self.enc.transform(cat_data.values), 
                columns=cat_data.columns,
            )
        )
        
        cols = [
            f"{cat_data.columns[i]}_{x}" 
                for i, col in enumerate(self.enc.categories_) for x in col
        ]
        
        bin_enc = pd.DataFrame()
        
        for j, cat in enumerate(cat_vals.columns):
            for i, col in enumerate(self.enc.categories_[j]):
                bin_enc[f"{cat}_{col}"] = (
                    cat_vals[cat].apply(lambda x: 1 if x==i else 0)
                )
                
        X_p = cont_vals.join(bin_enc).fillna(0)
        
        if y is not None:
            y_p = self.y_scl.transform(y)
            ret_val = (X_p, y_p)
        else:
            ret_val = X_p

        return ret_val
    
    
    def fit_transform(self, X, y=None):
        """
        """
        self.fit(X, y=y)
        return self.transform(X, y=y)
