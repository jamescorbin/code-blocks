import logging
import tempfile
import datetime
import os

TXT = '.txt'
ZIP = '.zip'
NPY = '.npy'

ALT = '-0'

DEFAULT_MIRROR = "https://gutenberg.pglaf.org/"

default_text_dir = "/home/jamescorbin/Desktop/texts"
default_index = os.path.join(default_text_dir, "GUTINDEX.ALL")
default_zip_dir = os.path.join(default_text_dir, 'zips')
default_ascii_dir = os.path.join(default_text_dir, 'ascii')
default_truncated_dir = os.path.join(default_text_dir, 'base')

logger = logging.getLogger(name=__name__)
