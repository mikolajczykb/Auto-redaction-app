from modules.AudioFile import AudioFile, get_path_without_mp4
from modules.Word import TimeSegment
from modules.speech_to_text import speech_to_words
import tkinter as tk
from tkinter import filedialog
import ffmpeg
import subprocess
import sys
from modules.window import App


if __name__ == "__main__":
    app = App()

    # # sys.path.append('./ffmpeg/bin')
    # print(check_ffmpeg())
    # model_path = "models/vosk-model-en-us-0.22"
    # audio_path = "C:/Users/uncha/Desktop/inzynierka/sound_files/mp4_files/VID_20170429_014159.649.mp4"
    # print(get_path_without_mp4(audio_path))
    #
    # # konwersja mp4 do wav
    #
    # # stream = ffmpeg.input(f'{audio_path_mp4}')
    # # a1 = stream.audio.filter("volume=0:enable='between(t,1,2)'")
    # # v1 = stream.video
    # # stream = ffmpeg.output(a1, v1, 'output.mp4')
    #
    # # ffmpeg.run(stream)
    # # inside = "volume=enable='between(t,5,10)':volume=0, volume=enable='between(t,45,55)':volume=0"
    #
    # # subprocess.call(f'ffmpeg -i {audio_path_mp4} -af "{ inside }" ./sound_files/mp4_files/output.mp4')
    #
    # subprocess.call(f'ffmpeg -y -i {get_path_without_mp4(audio_path)}.mp4 {get_path_without_mp4(audio_path)}.wav')
    #
    # #
    # audio_file = AudioFile(f'{get_path_without_mp4(audio_path)}')
    #
    # list_of_words = speech_to_words(audio_file, model_path)
    #
    # audio_file.load_words(list_of_words=list_of_words)
    # audio_file.list_of_words[2].is_censored = True
    # audio_file.list_of_words[4].is_censored = True
    # audio_file.list_of_words[5].is_censored = True
    # audio_file.list_of_words[6].is_censored = True
    #
    # additional_times = [TimeSegment({'start': 0.5, 'end': 1.0}), TimeSegment({'start': 0.7, 'end': 1.2})]
    #
    # # ffmpeg_string = audio_file.create_ffmpeg_string(additional_times=additional_times)
    # ffmpeg_string = audio_file.export(additional_times=additional_times, )
    #
    # # output to the screen
    # for word in list_of_words:
    #     print(str(word))
    # print(ffmpeg_string)

