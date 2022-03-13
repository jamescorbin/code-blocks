"""
"""

import os
import sys
import logging
import urllib.error
import urllib.request
import zipfile
import re

path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.insert(1, path)

logger = logging.getLogger(name=__name__)

ZIP = pkg.ZIP
TXT = pkg.TXT
ALT = pkg.ALT
alt_reg = re.compile(ALT)


def fetch_index():
    """
    """
    return 0


def fetch_document(
    id_code,
    mirror_url=pkg.DEFAULT_MIRROR,
    text_or_html='text',
    zip_dir=zip_dir,):
    """
    """
    iterated_id = [x for x in str(id_code)]
    dir_walk = ([mirror_url] + iterated_id[:-1] + [str(id_code)])
    fbn = f"{id_code}{ZIP}"
    fn_out = os.path.join(zip_dir, fbn)
    top_path = os.path.join(*dir_walk)
    path = os.path.join(top_path, fbn)

    if not os.path.exists(fn_out):
        try:
            req = urllib.request.Request(path)
            with urllib.request.urlopen(req) as http:
                with open(fn_out, 'wb') as f:
                    f.write(http.read())
            logger.info(f"Wrote file file://{fn_out} \nfrom {path}.")
        except urllib.error.HTTPError as e:
            logger.error(e)
            try:
                fbn = f"{id_code}{ALT}{ZIP}"
                path = os.path.join(top_path, fbn)
                req = urllib.request.Request(path)
                with urllib.request.urlopen(req) as http:
                    with open(fn_out, 'wb') as f:
                        f.write(http.read())
                logger.info(f"Wrote file file://{fn_out} \nfrom {path}.")
            except urllib.error.HTTPError as e:
                logger.error(e)
                raise
                return 1

        logger.info(
            f"Project Gutenberg text #{id_code}"
            f" downloaded to file://{zip_dir}.")
    else:
        logger.info(
            f"File #{id_code} already downloaded "
            f"located at file://{path}.")
    return 0


def unpack_zip(
    id_code,
    ascii_dir=ascii_dir,
    zip_dir=zip_dir,):
    """
    """
    extracted_files = []
    fn_out = os.path.join(ascii_dir, f"{id_code}{TXT}")
    fn_out_alt = os.path.join(ascii_dir, f"{id_code}{ALT}{TXT}")
    zip_pt = os.path.join(zip_dir, f"{id_code}{ZIP}")
    if os.path.exists(fn_out):
        logger.info(f"File {id_code}{TXT} already exists.")
    elif os.path.exists(fn_out_alt):
        logger.info(
            f"File {id_code}{TXT} already exists "
            f"as {id_code}{ALT}{TXT}.")
    else:
        try:
            with zipfile.ZipFile(zip_pt, mode='r') as zip_file:
                zipped_files = zip_file.infolist()
                for x in zipped_files:
                    xtr_fn = zip_file.extract(x, path=ascii_dir)
                    bn = os.path.basename(xtr_fn)
                    if alt_reg.search(bn):
                        new_bn = alt_reg.sub('', bn)
                        new_fn = os.path.join(ascii_dir, new_bn)
                        os.rename(xtr_fn, new_fn)
                    else:
                        new_fn = xtr_fn
                    logger.info(
                        f"File extracted to file://{new_fn}")
                    extracted_files.append(new_fn)

            logger.info(
                f"Extraction of {id_code} completed "
                f"to directory file://{ascii_dir}.")
        except:
            logger.error('here is an error')
    return extracted_files


def fetch_unpack(
    id_code,
    ascii_dir=ascii_dir,
    zip_dir=zip_dir,
    mirror_url=pkg.DEFAULT_MIRROR,
    text_or_html='text',):
    """
    """
    val = 0
    if id_code is None or len(str(id_code))==0:
        val = 1
    else:
        val = fetch_document(
                id_code,
                mirror_url=mirror_url,
                text_or_html='text',
                zip_dir=zip_dir,
            )
        if val==0:
            val = unpack_zip(id_code, ascii_dir=ascii_dir, zip_dir=zip_dir)
    return val


if __name__=="__main__":
    id_cd = 12433
    fetch_unpack(id_cd)
