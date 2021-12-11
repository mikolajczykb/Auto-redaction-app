from nltk.data import find
from nltk import download


class SetUpModule:
    def __init__(self):
        # self.language = self.get_language()
        self.download_nltk_packages()

    def download_nltk_packages(self):
        try:
            find("corpora/stopwords")
        except LookupError:
            download("stopwords")

        try:
            find('tokenizers/punkt')
        except LookupError:
            download('punkt')

        try:
            find('corpora/wordnet')
        except LookupError:
            download('wordnet')

        try:
            find("chunkers/maxent_ne_chunker")
        except LookupError:
            download("maxent_ne_chunker")

        try:
            find("corpora/words")
        except LookupError:
            download("words")

        try:
            find("taggers/averaged_perceptron_tagger")
        except LookupError:
            download("averaged_perceptron_tagger")

