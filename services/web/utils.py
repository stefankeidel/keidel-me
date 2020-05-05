import re
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer


def initial_clean(text):
    """
    Function to clean text of websites, email addresess and any punctuation
    We also lower case the text
    """
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    text = re.sub(
        "((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)", " ", text
    )
    text = text.lower()  # lower case the text
    text = text.translate(remove_punctuation_map)
    text = nltk.word_tokenize(text)
    return text


def remove_stop_words(text):
    """
    Function that removes all stopwords from text
    """
    stop_words = stopwords.words("english")
    return [word for word in text if word not in stop_words]


def stem_words(text):
    """
    Function to stem words, so plural and singular are treated the same
    """
    stemmer = PorterStemmer()
    try:
        text = [stemmer.stem(word) for word in text]
        text = [
            word for word in text if len(word) > 1
        ]  # make sure we have no 1 letter words
    except IndexError:  # the word "oed" broke this, so needed try except
        pass
    return text


def apply_all(text):
    """
    This function applies all the functions above into one
    """
    return stem_words(remove_stop_words(initial_clean(text)))
