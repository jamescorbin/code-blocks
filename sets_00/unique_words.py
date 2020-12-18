"""
"""

import sys
import os
import logging
import re

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
import __init__ as pkg
import load_text

TXT = pkg.TXT

logger = logging.getLogger(name=__name__)


def replace(data):
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
    data = re.sub('[^\w|^\s]', ' ', data)
    data = data.lower()

    return data


def write(data, fn, out_fn):
    """
    parameters:
            -- data, string
            -- fn, filename
            -- out_fn, output filename
    returns:
            -- none
    description:
            Writes output into two files.
            The first is the stripped down text
            placed in out_fn
            and the second of which contains all unique words
            and is in a file with the suffix "_unique".
    """
    with open(out_fn, 'w') as f:
        f.writelines(data)
    unique_words = "_unique"
    data = data.split()
    data = set(data)
    with open(f'{out_fn[:-len(TXT)]}{unique_words}{TXT}', 'w') as f:
        f.writelines('\n'.join(data))


if __name__=="__main__":
    import argparse
    parser = (
        argparse.ArgumentParser(
            description="Counts unique words in Project Gutenburg text."
        )
    )
    parser.add_argument("--file_names", nargs="+", help='')
    parser.add_argument("--output_path", nargs="+", help='')
    args = parser.parse_args()

    file_names = args.file_names
    output_path = args.output_path
    logger.info(f"Input files {file_names}\n Output files {output_path}")

    if len(file_names) != len(output_path):
        my_str = (
            "Specify output path to files."
                f"\nInput files:{file_names}"
                f"\nOutput paths:{output_path}"
        )
        raise Exception(my_str)
    fns = zip(file_names, output_path)

    for fn, out in fns:
        data = load_text.load_text(fn)
        data = replace(data)
        write(data, fn, out)
