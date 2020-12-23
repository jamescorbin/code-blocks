import sys
import os
import logging
import tempfile
import datetime

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
import gutenberg

TXT = '.txt'
JSON = '.json'
ZIP = '.zip'
NPY = '.npy'

default_text_dir = gutenberg.default_text_dir
default_index = gutenberg.default_index
default_ascii_dir = gutenberg.default_ascii_dir
default_truncated_dir = gutenberg.default_truncated_dir
default_preprocessed_dir = os.path.join(default_text_dir, 'preprocessed')
default_ancillary_dir = os.path.join(default_text_dir, 'ancillary')

logging_dir = tempfile.TemporaryDirectory()
now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
log_fp = os.path.join(logging_dir.name, f'{now}.txt')

root = logging.getLogger()
root.setLevel(logging.INFO)
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
root.addHandler(stream_handler)

file_handler = logging.FileHandler(log_fp)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
root.addHandler(file_handler)
