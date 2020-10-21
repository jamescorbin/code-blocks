import re
import os
import numpy as np

TXT = '.txt'
NPY = '.npy'

###############################################################################

###############################################################################

def write_dictionary(fns, outpt):
    '''
    '''
    sets = []
    for fn in fns:
        with open(fn, 'r') as f:
            sets.append(set([x.strip() for x in f]))

    combined_words = set()
    for s in sets:
        combined_words = combined_words | s
    combined_words = sorted(combined_words)
    with open(outpt, 'w') as f:
        f.write('\n'.join(combined_words))
    return combined_words

###############################################################################

###############################################################################

def binary_search_index(ord_list, val, index=0):
    '''
    '''
    middle_ind = len(ord_list)//2
    if len(ord_list) == 1:
        return_val = index
    else:
        if val < ord_list[middle_ind]:
            new_list = ord_list[:middle_ind]
            new_index = index
        else:
            new_list = ord_list[middle_ind:]
            new_index = index + middle_ind
        return_val = binary_search_index(new_list, val, index=new_index)
    return return_val

###############################################################################

###############################################################################

def categorical_encoding(data, dictionary):
    '''
    '''
    return np.array(
                [binary_search_index(dictionary, x.strip()) for x in data])

###############################################################################

###############################################################################

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(
            description="Counts unique words in Project Gutenburg text.")
    parser.add_argument("--file_names", nargs="+", help='')
    parser.add_argument("--dictionary_pt")
    args = parser.parse_args()

    file_names = args.file_names
    outpt = args.dictionary_pt

    dictionary = write_dictionary(file_names, outpt)
    for fn in file_names:
        with open(fn, 'r') as f:
            text = categorical_encoding(f.readlines(), dictionary)
        with open(re.sub(TXT, '', fn)+NPY, 'wb') as f:
            np.save(f, text)
