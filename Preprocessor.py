__author__ = 'gabriel'
import unicodedata
import re

acceptable = re.compile('[^A-Z ]')
spaces = re.compile('[ ]+')

def preprocessor_tokenizer(txt):
    txt = txt.upper()
    txt = unicodedata.normalize('NFD', txt)
    txt = acceptable.sub(" ", txt)
    tokens = spaces.split(txt)
    return [t for t in  tokens if len(t) >= 2]

if __name__ == "__main__":
    print(preprocessor_tokenizer("olá, mundão! hu3     hu3"))