"""
"""

import sys
import os
import logging
import re
import collections

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)
import textnlp as pkg
import textnlp.porter_stemmer as porter_stemmer

TXT = pkg.TXT

logger = logging.getLogger(name=__name__)


def standardize_char_set(data):
    """
    parameters:
            -- {data}, string
    returns:
            -- {data}, string
    description
            Removes apostrophes, replaces other
            non-alphanumeric characters with spaces,
            and applies lowercase to all letters.
    """
    data = re.sub("'", '', data)
    data = re.sub('[^\.\w\s]', ' ', data)
    data = re.sub('\.{3}', ' ', data)
    data = re.sub('\.', ' . ', data)
    data = re.sub('_', ' ', data)
    data = re.sub('\s+', ' ', data)
    data = data.lower()

    return data


def download_nltk():
    """
    """
    import nltk
    try:
        nltk.download('stopwords')
    except:
        logger.error("Download Failed.")


def filter_stopwords(data):
    """
    """
    import nltk
    stopwords = nltk.corpus.stopwords.words("english")
    data = ' '.join([x for x in data.split() if x not in stopwords])
    return data


def stem(data, **kwargs):
    """
    """
    ps = porter_stemmer.PorterStemmer()
    new_data = ' '.join(ps.run(data.split()))
    return new_data


def main(data, stemming=False, return_counts=False):
    """
    """
    data = standardize_char_set(data)
    try:
        data = filter_stopwords(data)
    except:
        download_nltk()
        data = filter_stopwords(data)
    if stemming:
        data = stem(data)
    if return_counts:
        val = (data, collections.Counter(data.split()))
    else:
        val = data

    return val
