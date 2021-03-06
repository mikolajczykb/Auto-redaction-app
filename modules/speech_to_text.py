import json
import wave

from modules.AudioFile import AudioFile
from modules.Word import Word
from vosk import Model, KaldiRecognizer
from typing import List
from timeit import default_timer as timer


def speech_to_words(audio_file: AudioFile, model: Model,
                    framerate=-1, chunk=4000) -> List[Word]:
    # model = Model(model_path)
    wf = wave.open(audio_file.filepath + '.wav', "rb")
    if framerate == -1:
        framerate = wf.getframerate()
    rec = KaldiRecognizer(model, framerate)
    rec.SetWords(True)

    # get the list of JSON dictionaries
    results = []
    # recognize speech using vosk model
    start = timer()
    while True:
        data = wf.readframes(chunk)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)
    end = timer()
    print("TIME OF TRANSCRIPTION:", end - start)

    # convert list of JSON dictionaries to list of 'Word' objects
    list_of_words = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            w = Word(obj)  # create custom Word object
            list_of_words.append(w)  # and add it to list

    wf.close()  # close audiofile
    return list_of_words