import logging
import tempfile
import datetime
import os

TXT = '.txt'
NPY = '.npy'

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
