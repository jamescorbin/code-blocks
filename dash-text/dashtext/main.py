"""
"""

import os
import sys

proj_path = os.path.dirname(os.path.dirname(__file__))
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)
from dashtext import app
import dashtext.index as index


if __name__ == '__main__':
    index.make()
    app.run_server(debug=True)
