import nltk
import re

###############################################################################

###############################################################################

def download_nltk():
    '''
    '''
    try:
        nltk.download('stopwords')
    except:
        print("Download Failed.")

###############################################################################

###############################################################################

def filter_stopwords(data):
    '''
    '''
    stopwords = nltk.corpus.stopwords.words("english")
    data = data.split()
    data = [x for x in data if x not in stopwords]
    return data

###############################################################################

###############################################################################

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(
            description="Removes stopwords from file.")
    parser.add_argument("--file_names", nargs="+", help='')
    args = parser.parse_args()

    file_names = args.file_names
    download_nltk()

    for fn in file_names:
        with open(fn, 'r') as f:
            data = f.read()
        data = filter_stopwords(data)
        with open(fn, 'w') as f:
            f.write('\n'.join(data))
