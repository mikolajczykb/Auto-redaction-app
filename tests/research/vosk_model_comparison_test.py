import json
from modules.AudioFile import AudioFile, create_wav_from_mp4
from modules.speech_to_text import speech_to_words
from timeit import default_timer as timer
from vosk import Model

MODEL_DIRECTORY = r"C:\Users\uncha\Desktop\Auto redaction app\models"
NONPORTABLE_MODEL_NAME = r"vosk-model-en-us-0.22"
PORTABLE_MODEL_NAME = r"vosk-model-small-en-us-0.15"

VIDEO_DIRECTORY = r"C:\Users\uncha\Desktop\Auto redaction app\sound_files\mp4_files"
# LONG_VIDEO_PATH = r"C:\Users\uncha\Desktop\Auto redaction app\sound_files\mp4_files\High Speed Chase _ Criminal Apprehension"
# MEDIUM_VIDEO_PATH = r"C:\Users\uncha\Desktop\Auto redaction app\sound_files\mp4_files\VID_20170428_234922.344 - Inside Store"
LONG_VIDEO_PATH = VIDEO_DIRECTORY + "\\" + "PWC_VID_20160809_084137.114"
MEDIUM_VIDEO_PATH = VIDEO_DIRECTORY + "\\" + "VID_20170428_234922.344 - Inside Store"
SHORT_VIDEO_PATH = VIDEO_DIRECTORY + "\\" + "short_test_file"

if __name__ == "__main__":
    create_wav_from_mp4(LONG_VIDEO_PATH)
    create_wav_from_mp4(MEDIUM_VIDEO_PATH)

    print("TEST MODEL LOADING SPEED")
    model1_path = MODEL_DIRECTORY + "\\" + NONPORTABLE_MODEL_NAME
    model2_path = MODEL_DIRECTORY + "\\" + PORTABLE_MODEL_NAME

    start_1 = timer()
    model1 = Model(MODEL_DIRECTORY + "\\" + NONPORTABLE_MODEL_NAME)
    end_1 = timer()
    print("NONPORTABLE MODEL LOADING SPEED:", end_1 - start_1)

    start_2 = timer()
    model2 = Model(MODEL_DIRECTORY + "\\" + PORTABLE_MODEL_NAME)
    end_2 = timer()
    print("PORTABLE MODEL LOADING SPEED:", end_2 - start_2)


    print("TEST TRANSCRIPTION SPEED")
    long_audio_file = AudioFile(LONG_VIDEO_PATH)
    medium_audio_file = AudioFile(MEDIUM_VIDEO_PATH)
    short_audio_file = AudioFile(SHORT_VIDEO_PATH)

    # print("LONG FILE TRANSCRIPTION TIMES:")
    print("SPEECH TO TEXT FUNCTION OVERALL TIMES")
    start = timer()
    list_of_words_long_1 = speech_to_words(long_audio_file, model1)
    end = timer()
    print("SPEECH TO TEXT FUNCTION OVERALL TIME (LONG 1):", end - start)

    start = timer()
    list_of_words_long_2 = speech_to_words(long_audio_file, model2)
    end = timer()
    print("SPEECH TO TEXT FUNCTION OVERALL TIME (LONG 2):", end - start)

    start = timer()
    list_of_words_medium_1 = speech_to_words(medium_audio_file, model1)
    end = timer()
    print("SPEECH TO TEXT FUNCTION OVERALL TIME (MEDIUM 1):", end - start)

    start = timer()
    list_of_words_medium_2 = speech_to_words(medium_audio_file, model2)
    end = timer()
    print("SPEECH TO TEXT FUNCTION OVERALL TIME (MEDIUM 2):", end - start)

    start = timer()
    list_of_words_short_1 = speech_to_words(short_audio_file, model1)
    end = timer()
    print("SPEECH TO TEXT FUNCTION OVERALL TIME (SHORT 1):", end - start)

    start = timer()
    list_of_words_short_2 = speech_to_words(short_audio_file, model2)
    end = timer()
    print("SPEECH TO TEXT FUNCTION OVERALL TIME (SHORT 2):", end - start)

    with open('list_of_words_long_1.txt', 'w') as outfile:
        outfile.truncate(0)
        print("LIST OF WORDS LONG 1 LENGTH:", len(list_of_words_long_1))
        for word in list_of_words_long_1:
            json.dump(str(word), outfile)
            outfile.write('\n')

    with open('list_of_words_long_2.txt', 'w') as outfile:
        outfile.truncate(0)
        print("LIST OF WORDS LONG 2 LENGTH:", len(list_of_words_long_2))
        for word in list_of_words_long_2:
            json.dump(str(word), outfile)
            outfile.write('\n')

    with open('list_of_words_medium_1.txt', 'w') as outfile:
        outfile.truncate(0)
        print("LIST OF WORDS MEDIUM 1 LENGTH:", len(list_of_words_medium_1))
        for word in list_of_words_medium_1:
            json.dump(str(word), outfile)
            outfile.write('\n')

    with open('list_of_words_medium_2.txt', 'w') as outfile:
        outfile.truncate(0)
        print("LIST OF WORDS MEDIUM 2 LENGTH:", len(list_of_words_medium_2))
        for word in list_of_words_medium_2:
            json.dump(str(word), outfile)
            outfile.write('\n')

    with open('list_of_words_short_1.txt', 'w') as outfile:
        outfile.truncate(0)
        print("LIST OF WORDS SHORT 1 LENGTH:", len(list_of_words_short_1))
        for word in list_of_words_short_1:
            json.dump(str(word), outfile)
            outfile.write('\n')

    with open('list_of_words_short_2.txt', 'w') as outfile:
        outfile.truncate(0)
        print("LIST OF WORDS SHORT 2 LENGTH:", len(list_of_words_short_2))
        for word in list_of_words_short_2:
            json.dump(str(word), outfile)
            outfile.write('\n')
