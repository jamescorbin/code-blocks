"""
"""

import sys
import os
import logging
import re
import collections
import json

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)
import textnlp as pkg
import pretokenize
import gutenberg.load_text as load_text

logger = logging.getLogger(name=__name__)

logger.info(f"Project path: {proj_path}")


def main(
        ids=[],
        indir=pkg.default_ascii_dir,
        outdir=pkg.default_preprocessed_dir,
        auxdir=pkg.default_ancillary_dir,
        stemming=False,
):
    """
    """
    logger.info(f"Input directory file://{indir}")
    logger.info(f"Output directory file://{outdir}")
    logger.info(f"Ancillary directory file://{auxdir}")
    if len(ids) == 0:
        ids = [x[:-len(pkg.TXT)] for x in os.listdir(indir)]
    fns = [os.path.join(indir, f"{x}{pkg.TXT}") for x in ids]

    for i, _id in enumerate(ids):
        outfn = os.path.join(outdir, f"{_id}{pkg.TXT}")
        auxfn = os.path.join(auxdir, f"{_id}{pkg.JSON}")
        if os.path.exists(outfn) and os.path.exists(auxfn):
            continue
        text = load_text.load_text(fns[i], write=False)
        new_text, counts = (
            pretokenize.main(text, stemming=stemming, return_counts=True)
        )

        with open(outfn, 'w') as f:
            f.write('\n'.join(new_text.split()))

        with open(auxfn, 'w') as f:
            json.dump(
                counts,
                f,
                sort_keys=True,
                indent='\t',
                separators=(',', ': '),
            )
        logger.info(f"Wrote files: file://{outfn} \nand file://{auxfn}.")

    return 0
