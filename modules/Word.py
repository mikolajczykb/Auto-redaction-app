from nltk.stem import WordNetLemmatizer
import re
from math import modf as math_modf
import numpy as np

# move this to class
def convert_seconds_to_timestamp_format(seconds: float) -> str:
    frac, whole = math_modf(seconds)
    minutes = int(whole / 60)
    seconds = int(whole % 60)
    miliseconds = int(round(frac, 3) * 1000)
    return f'{minutes}:{seconds if seconds > 10 else "0" + str(seconds)}:{miliseconds if miliseconds > 0 else "000"}'


def check_if_correct_timestamp_format(timestamp: str) -> bool:
    return True if re.match(r'^(?:\d+):(?:[0-5]\d)(?::\d\d\d)?$', timestamp) else False


# move this to class
def convert_timestamp_to_second_format(timestamp: str) -> float:
    total: float = 0
    if check_if_correct_timestamp_format(timestamp):
        timestamp_length = len(timestamp)
        minutes_index: int = timestamp.find(':')
        total += int(timestamp[:minutes_index]) * 60

        seconds_index = timestamp.find(':', minutes_index + 1, timestamp_length)
        seconds_index = seconds_index if seconds_index > -1 else timestamp_length
        total += int(timestamp[minutes_index + 1:seconds_index])

        milliseconds = timestamp[seconds_index + 1:]
        if milliseconds != '':
            total += int(milliseconds) / 1000
        return round(total, 3)
    return -1


class TimeSegment:

    def __init__(self, config):
        self.start: TimeStamp = TimeStamp(config["start"])
        self.end: TimeStamp = TimeStamp(config["end"])

    def __str__(self):
        return f"{str(self.start)} - {str(self.end)}"


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
        if hasattr(config, 'is_censored'):
            self.is_censored = config['is_censored']
        else:
            self.is_censored = False

    def __str__(self):
        return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%" \
            .format(self.word, self.time_segment.start, self.time_segment.end, self.confidence * 100)


if __name__ == "__main__":
    timestamp1 = '00:01:590'
    print('should return 1.590, ', convert_timestamp_to_second_format(timestamp1))

    timestamp2 = '5:05'
    print('should return 305', convert_timestamp_to_second_format(timestamp2))

    timestamp3 = '00:08:500'
    print('should return 8.5, ', convert_timestamp_to_second_format(timestamp3))

    timestamp3_2 = '01:04:352'
    print('should return 64.352, ', convert_timestamp_to_second_format(timestamp3_2))

    timestamp3_3 = '00:00:000'
    print(timestamp3_3, convert_timestamp_to_second_format(timestamp3_3))

    timestamp4 = 127.54
    print(timestamp4, convert_seconds_to_timestamp_format(timestamp4))

    timestamp5 = 100.00
    print(timestamp5, convert_seconds_to_timestamp_format(timestamp5))