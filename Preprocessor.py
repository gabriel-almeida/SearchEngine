import unicodedata
import re

__author__ = 'gabriel'

acceptable = re.compile('[^A-Z ]')
spaces = re.compile('[ ]+')


def preprocessor_tokenizer(txt):
    txt = txt.upper()
    txt = unicodedata.normalize('NFD', txt)
    txt = acceptable.sub(" ", txt)
    tokens = spaces.split(txt)
    return [t for t in  tokens if len(t) >= 2]
