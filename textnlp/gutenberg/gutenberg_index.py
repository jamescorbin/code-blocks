"""
"""

import os
import sys
import logging
import re

import pandas as pd

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
import __init__ as pkg
import load_text

default_index = pkg.default_index
index_header = "\s*<==LISTINGS==>"
footer = "<==End of GUTINDEX.ALL==>"

list_title = "TITLE and AUTHOR"
title_re = re.compile(list_title)
skip_2 = 2

ebook_re = re.compile('\d+\w{0,1}\Z')
split_char = '\r\n'

illustrator_re = re.compile("(?<=\[Illustrator:\s)[^\]]+(?=\])")
subtitle_re = re.compile("(?<=\[Subtitle:\s)[^\]]+(?=\])")
language_re = re.compile("(?<=\[Language:\s)[^\]]+(?=\])")
title_author_split = ', by '
ta_split_re = re.compile(title_author_split)


def load_index(fn=default_index):
    """
    """
    text = load_text.load_text(fn, header=index_header, footer=footer)
    text_lines = text.split(split_char)

    skip_to = 0
    for i, x in enumerate(text_lines):
        if title_re.match(x):
            skip_to = i
            break

    title_info = []
    author_info = []
    ebook_no = []
    subtitle_info = []
    illustrator_info = []
    language_info = []

    title_buffer = ''
    ebook_buffer = ''

    for line in text_lines[skip_to+skip_2:]:
        if len(line)>0:
            reg = ebook_re.search(line)
            if len(ebook_buffer)==0 and reg is not None:
                ebook_buffer = reg.group()
                title_buffer += ebook_re.sub('', line)
            else:
                title_buffer += line
        else:
            if len(title_buffer)+len(ebook_buffer)>0:
                title_buffer = ' '.join(title_buffer.split())
                illustrator_match = illustrator_re.search(title_buffer)
                if illustrator_match:
                    illustrator_info.append(illustrator_match.group())
                    title_buffer = (
                        title_buffer[
                            :illustrator_match.start()-len("[Illustrator: ")
                        ]
                        + title_buffer[
                            illustrator_match.end()+len("]"):
                        ]
                    )
                else:
                    illustrator_info.append('')
                subtitle_match = subtitle_re.search(title_buffer)
                if subtitle_match:
                    subtitle_info.append(subtitle_match.group())
                    title_buffer = (
                        title_buffer[
                            :subtitle_match.start()-len("[Subtitle: ")
                        ]
                        + title_buffer[
                            subtitle_match.end()+len("]"):
                        ]
                    )
                else:
                    subtitle_info.append('')

                language_match = language_re.search(title_buffer)
                if language_match:
                    language_info.append(language_match.group())
                    title_buffer = (
                        title_buffer[
                            :language_match.start()-len("[Language: ")
                        ]
                        + title_buffer[
                            language_match.end()+len("]"):
                        ]
                    )
                else:
                    language_info.append('')

                if ta_split_re.search(title_buffer):
                    sp = title_buffer.split(title_author_split)
                    title_buffer = sp[0]
                    author_info.append(sp[1])
                else:
                    author_info.append('')

                title_info.append(title_buffer)
                ebook_no.append(ebook_buffer)
            title_buffer = ''
            ebook_buffer = ''

    df = pd.DataFrame(
            {
                "Title": title_info,
                "Author": author_info,
                "Subtitle": subtitle_info,
                "Illustrator": illustrator_info,
                "Language": language_info,
                "EBOOK NO.": ebook_no,
            }
        )

    return df
