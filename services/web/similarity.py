import utils
from sklearn.feature_extraction.text import TfidfVectorizer
import textract


def pairwise(file_list):
    documents = []
    for f in file_list:
        documents.append(textract.process(f))

    tfidf = TfidfVectorizer(tokenizer=utils.apply_all).fit_transform(documents)

    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity.toarray()


if __name__ == "__main__":
    pairwise(['./lorem1.txt', './lorem2.txt', './lorem3.txt'])
