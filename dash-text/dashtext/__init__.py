import sys
import os
import logging
import tempfile
import datetime

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)

TXT = '.txt'
JSON = '.json'

logging_dir = tempfile.TemporaryDirectory()
now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
log_fp = os.path.join(logging_dir.name, f'{now}.txt')

root = logging.getLogger()
root.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
root.addHandler(stream_handler)

file_handler = logging.FileHandler(log_fp)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
root.addHandler(file_handler)
