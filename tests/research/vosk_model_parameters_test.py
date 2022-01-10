import json
from modules.AudioFile import AudioFile, create_wav_from_mp4
from modules.speech_to_text import speech_to_words
from timeit import default_timer as timer
from vosk import Model

MODEL_DIRECTORY = r"C:\Users\uncha\Desktop\Auto redaction app\models"
PORTABLE_MODEL_NAME = r"vosk-model-small-en-us-0.15"
NON_PORTABLE_MODEL_NAME = r"vosk-model-en-us-0.22"

VIDEO_DIRECTORY = r"C:\Users\uncha\Desktop\Auto redaction app\sound_files\mp4_files"
# LONG_VIDEO_PATH = VIDEO_DIRECTORY + "\\" +

SHORT_VIDEO_PATH = VIDEO_DIRECTORY + "\\" + "short_test_file"

if __name__ == "__main__":
    audio_file = AudioFile(SHORT_VIDEO_PATH)
    model = Model(MODEL_DIRECTORY + "\\" + NON_PORTABLE_MODEL_NAME)

    with open('parameters_framerate_tests_result01.txt', 'w') as outfile:
        for framerate in range(1000, 16001, 1000):
            outfile.write(f"TRY NUMBER {framerate / 1000}\n")
            list_of_words = speech_to_words(audio_file, model, framerate)
            for word in list_of_words:
                outfile.write(str(word))
                outfile.write("\n")

    with open('parameters_chunk_tests_result01.txt', 'w') as outfile:
        for chunk in range(500, 4001, 500):
            outfile.write(f"TRY NUMBER {chunk / 500}\n")
            list_of_words = speech_to_words(audio_file, model, chunk=chunk)
            for word in list_of_words:
                outfile.write(str(word))
                outfile.write("\n")
