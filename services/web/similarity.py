import utils
from sklearn.feature_extraction.text import TfidfVectorizer
import textract
import numpy as np


def pairwise(file_list, round_decimals=None):
    documents = []
    for f in file_list:
        documents.append(textract.process(f))

    tfidf = TfidfVectorizer(tokenizer=utils.apply_all).fit_transform(documents)

    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T

    if round_decimals is not None:
        pairwise_similarity.data = np.round(pairwise_similarity.data, round_decimals)

    return pairwise_similarity.toarray()
