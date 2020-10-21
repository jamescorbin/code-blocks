import numpy as np
import os
import re

NPY = '.npy'
TXT = '.txt'

###############################################################################

###############################################################################

def unique_pairings(fns, out_fp):
    '''
    '''
    pairs = None
    for fn in fns:
        with open(fn, 'rb') as f:
            ar = np.load(f, allow_pickle=True)
        stack_ar = np.array([ar[:-1], ar[1:]])
        stack_ar = np.array(
                    [np.min(stack_ar, axis=0), np.max(stack_ar, axis=0)]).T
        unique_pairs = np.unique(stack_ar, axis=0)
        if pairs is None:
            pairs = unique_pairs
        else:
            pairs = np.concatenate([pairs, unique_pairs])
    pairs = np.unique(pairs, axis=0)
    with open(out_fp, 'wb') as f:
        np.save(f, pairs)
    return pairs

###############################################################################

###############################################################################

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(
            description="Counts unique words in Project Gutenburg text.")
    parser.add_argument("--file_names", nargs="+", help='')
    parser.add_argument("--unique_pairs_pt")
    args = parser.parse_args()

    file_names = args.file_names
    out_fp = args.unique_pairs_pt

    pairs = unique_pairings(file_names, out_fp)
