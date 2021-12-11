from nltk.stem import WordNetLemmatizer


def convert_seconds_to_timestamp_format(seconds: float):
    return f'{int(seconds // 60)}:{int(seconds % 60)}:{int(round(seconds % 1, 2) * 100)}'


class TimeSegment:

    def __init__(self, config):
        self.start: TimeStamp = TimeStamp(config["start"])
        self.end: TimeStamp = TimeStamp(config["end"])


class TimeStamp:

    def __init__(self, start):
        self.value: float = start

    def __str__(self):
        return convert_seconds_to_timestamp_format(self.value)


class Word:
    def __init__(self, config):
        self.confidence = config["conf"]
        self.time_segment = TimeSegment(config)
        self.word: str = config["word"]
        lemmatizer = WordNetLemmatizer()
        self.lemmatized_word: str = lemmatizer.lemmatize(self.word)
        self.is_censored = False

    def __str__(self):
        return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%, lemmatized = {}" \
            .format(self.word, self.time_segment.start, self.time_segment.end, self.confidence * 100, self.lemmatized_word)
