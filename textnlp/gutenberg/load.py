"""
"""

import sys
import os
import logging
import re

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
import __init__ as pkg

TXT = pkg.TXT

footer = "[*][*][*]\s*END OF"
header = "[*][*][*]\s*START OF"
width_newline = 2

logger = logging.getLogger(name=__name__)


def load_text(
    fn,
    write=False,
    write_pt=None,
    header=header,
    use_header=True,
    footer=footer,
    use_footer=True,):
    """
    This method opens a Project Guetenberg Ebook
        and cuts off the header and footer.
        See ${footer} and ${header}.
    Args:
            -- fn, file path
    Returns:
            -- data, string (utf-8)
    """
    if not os.path.exists(fn):
        msg = f"File {fn} not found."
        logger.error(msg)
        raise FileNotFoundError(msg)

    start_position = 0
    end_position = -1

    if use_header and header is not None:
        try:
            header_re = re.compile(header)
        except:
            logger.error('Code later')
        with open(fn, 'r') as f:
            header_found = False
            eof_check = False
            while (not header_found) and (not eof_check):
                line = f.readline()
                eof_check = (line is None) | (line=='')
                if header_re.match(line):
                    header_found = True
                    start_position = f.tell()
                elif eof_check:
                    logger.warning(
                        f"No header {header} found in {fn}."
                    )

    if use_footer and footer is not None:
        try:
            footer_re = re.compile(footer)
        except:
            logger.error('Invalid footer')
        footer_found = False
        eof_check = False
        gen_rev_lines = _reversed_readline(fn)
        while (not footer_found) and (not eof_check):
            try:
                line, i = gen_rev_lines.__next__()
            except StopIteration:
                logger.warning(
                    f"No footer {footer} found in {fn}."
                )
                line = ''
                eof_check = True
            if footer_re.match(line):
                footer_found = True
                end_position = i

    with open(fn, 'rb') as f:
        try:
            f.seek(start_position)
            try:
                data = f.read(end_position - start_position)
            except (ValueError, OverflowError) as e:
                logger.error(
                    f"{e}\nStart position {end_position}\t"
                    f"System maxsize {sys.maxsize}"
                )
                data = f.read()
        except (ValueError, OverflowError) as e:
            logger.error(
                f"{e}\nStart position {start_position}\t"
                f"System maxsize {sys.maxsize}"
            )
            data = f.read()

    data = data.decode('utf-8')
    if write:
        if write_pt is None:
            write_fn = (
                os.path.join(
                    pkg.default_truncated_dir, os.path.basename(fn)
                )
            )
        else:
            write_fn = write_pt
        if os.path.exists(write_fn):
            pass
        else:
            with open(write_fn, 'w') as f:
                f.write(data)

    return data


def _reversed_readline(fn, buffer=32000):
    """
    Generator which reads lines from the end of a file.
        The file is buffered and the index counting from the back
        end of the file is also returned.
    Args:
        -- {fn}, file name
        -- {buffer}=32000, buffer size
    Returns:
        -- line, string
        -- line_number, integer; lines from end of file
    """
    with open(fn, 'r') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        l_pointer = file_size
        r_pointer = file_size
        buffer_text = ''
        fragment = None
        position = file_size

        while l_pointer > 0:
            r_pointer = l_pointer
            l_pointer = max(f.tell() - buffer, 0)
            f.seek(l_pointer)
            buffer_text = (f.read(r_pointer-l_pointer) + fragment
                           if fragment
                           else f.read(r_pointer-l_pointer)
                           )
            lines = buffer_text.splitlines()

            if fragment is not None:
                if lines[0] == '':
                    fragment = None
                else:
                    fragment = lines[0]

            for i in range(len(lines)-1, 0, -1):
                if lines[i]:
                    pos_change = len(lines[i]) + width_newline
                    position -= pos_change
                    yield lines[i], position
                else:
                    position -= width_newline

            if l_pointer == 0:
                yield lines[0], 0

        if file_size == 0:
            yield '', 0
