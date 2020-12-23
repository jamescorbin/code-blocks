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
