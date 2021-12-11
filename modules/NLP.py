import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import List, Set
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from modules.Word import Word


# def extract_lemmatized_words(audio_transcription: str) -> List[str]:
#
#
#     stop_words = set(stopwords.words("english"))
#     filtered_words = [
#         word for word in words_in_sentence if word.casefold() not in stop_words
#     ]
#
#     lemmatizer = WordNetLemmatizer()
#     lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
#     return lemmatized_words


def extract_named_entities(words: Word) -> List[str]:
    try:
        nltk.data.find("chunkers/maxent_ne_chunker")
    except LookupError:
        nltk.download("maxent_ne_chunker")

    try:
        nltk.data.find("corpora/words")
    except LookupError:
        nltk.download("words")

    try:
        nltk.data.find("taggers/averaged_perceptron_tagger")
    except LookupError:
        nltk.download("averaged_perceptron_tagger")

    words_in_sentence = word_tokenize(audio_transcription)
    tags = nltk.pos_tag(words_in_sentence)
    tree = nltk.ne_chunk(tags, binary=True)
    return list(
        " ".join(i[0] for i in t)
        for t in tree
        if hasattr(t, "label") and t.label() == "NE"
    )
