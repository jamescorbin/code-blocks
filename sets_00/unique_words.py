import sys
import re
import os

TXT = '.txt'
footer = "[*][*][*] END OF THIS PROJECT GUTENBERG EBOOK"
header = "[*][*][*] START OF THIS PROJECT GUTENBERG EBOOK"
width_newline = 2

###############################################################################

###############################################################################

def load_text(fn):
    '''
    parameters:
            -- fn, file path
    returns:
            -- data, string (utf-8)
    description:
            This method opens a Project Guetenberg Ebook
            and cuts off the header and footer.
            See ${footer} and ${header}.
    '''
    footer_re = re.compile(footer)
    header_re = re.compile(header)
    start_position = 0
    with open(fn, 'r') as f:
        found = False
        eof_check = False
        while (not found) and (not eof_check):
            line = f.readline()
            eof_check = line is None
            if header_re.match(line):
                found = True
                start_position = f.tell()

    found = False
    eof_check = False
    gen_rev_lines = reversed_readline(fn)
    end_position = 0
    while (not found) and (not eof_check):
        try:
            line, i = gen_rev_lines.__next__()
        except StopIteration:
            line = ''
            eof_check = True
        if footer_re.match(line):
            found = True
            end_position = i

    with open(fn, 'rb') as f:
        f.seek(start_position)
        data = f.read(end_position - start_position)

    return data.decode("utf-8")

###############################################################################

###############################################################################

def reversed_readline(fn, buffer=32000):
    """
    parameters:
            -- fn, file name
            -- buffer=32000, buffer size
    returns:
            -- line, string
            -- line_number, integer; lines from end of file
    description:
            Generator which reads lines from the end of a file.
            The file is buffered and the index counting from the back
            end of the file is also returned.
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
            l_pointer = min(f.tell() - buffer, 0)
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

###############################################################################

###############################################################################

def replace(data):
    '''
    parameters:
            -- data, string
    returns:
            -- data, string
    description
            Removes apostrophes, replaces other
            non-alphanumeric characters with spaces,
            and applies lowercase to all letters.
    '''
    data = re.sub("'", '', data)
    data = re.sub('[^\w|^\s]', ' ', data)
    data = data.lower()

    return data

###############################################################################

###############################################################################

def write(data, fn, out_fn):
    '''
    parameters:
            -- data, string
            -- fn, filename
            -- out_fn, output filename
    returns:
            -- none
    description:
            Writes output into two files.
            The first is the stripped down text
            placed in out_fn
            and the second of which contains all unique words
            and is in a file with the suffix "_unique".
    '''
    with open(out_fn, 'w') as f:
        f.writelines(data)
    unique_words = "_unique"
    data = data.split()
    data = set(data)
    with open(re.sub(TXT, '', fn)+unique_words+TXT, 'w') as f:
        f.writelines('\n'.join(data))

###############################################################################

###############################################################################

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(
            description="Counts unique words in Project Gutenburg text.")
    parser.add_argument("--file_names", nargs="+", help='')
    parser.add_argument("--output_path", nargs="+", help='')
    args = parser.parse_args()

    file_names = args.file_names
    output_path = args.output_path
    if len(file_names) != len(output_path):
        my_str = ("Specify output path to files." +
                        "\nInput files:" + str(file_names) +
                        "\nOutput paths:" + str(output_path))
        raise Exception(my_str)
    fns = zip(file_names, output_path)

    for fn, out in fns:
        data = load_text(fn)
        data = replace(data)
        write(data, fn, out)
