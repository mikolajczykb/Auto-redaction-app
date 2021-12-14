import os
import platform
import subprocess
import wave
import time
from modules.Word import Word, TimeSegment
from typing import List
from tkinter import messagebox

WAV = '.wav'

FFMPEG = "ffmpeg"


def create_wav_from_mp4(filepath: str):
    subprocess.call(f'ffmpeg -y -i "{filepath}.mp4" "{filepath}.wav"')


def get_mp4_path(mp4_path: str):
    return mp4_path[:-4] if mp4_path.endswith('.mp4') else "error"


def get_directory_path(path: str):
    return path[:path.rfind('/')]


def get_final_time(all_times: List[TimeSegment]) -> List[TimeSegment]:
    all_times_length = len(all_times)
    if all_times_length == 0:
        return []
    i = 0

    while i < all_times_length - 2:
        if all_times[i].end.value >= all_times[i + 1].start.value:
            all_times[i].end.value = all_times[i + 1].end.value
            all_times.pop(i + 1)
            all_times_length -= 1
        i += 1
    return all_times


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    try:
        if platform.system() == 'Windows':
            return os.path.getmtime(path_to_file)
        else:
            stat = os.stat(path_to_file)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return stat.st_mtime
    except:
        return -1


def check_if_file_created(path_to_file: str):
    current_time = time.time()
    try:
        when_created = creation_date(path_to_file)
        if when_created == -1 or current_time < when_created:
            return False
        else:
            return True
    except:
        return False


class AudioFile:

    def __init__(self, filepath):
        # path of the file without the .mp4 extension
        self.filepath = filepath
        # path of the directory the file is in
        self.directory_path = get_directory_path(self.filepath)
        self.audio = None
        self.chunk = 1024
        # list of words we load into the audiofile
        self.list_of_words: List[Word] = None
        # self.additional_times: List[TimeSegment] = []

        # close PyAudio
        # p.terminate()

    def get_output_file_name(self, file_save_name=''):
        if file_save_name == '':
            file_save_name = self.filepath + '_output.mp4'
        else:
            file_save_name = f'{self.directory_path}/{file_save_name}'
        return file_save_name

    def export(self, additional_times: List[TimeSegment], file_save_name=''):
        inside = self.create_ffmpeg_string(additional_times)
        # if file_save_name == '':
        #     file_save_name = self.filepath + '_output.mp4'
        # else:
        #     file_save_name = f'{self.directory_path}/{file_save_name}'
        file_save_name = self.get_output_file_name(file_save_name)
        # current_time = time.time()
        print(self.filepath + ".mp4")
        print(inside)
        print(file_save_name + ".mp4")
        subprocess \
            .call(f'ffmpeg -y -i "{self.filepath + ".mp4"}" -af "{inside}" "{file_save_name + ".mp4"}"')
        if not check_if_file_created(file_save_name + ".mp4"):
            messagebox.showerror("Export error!",
                                 "There was an error when trying to export the redacted file. Please try again.")
            return ""
        messagebox.showinfo("Export success!")
        return file_save_name

        # try:
        #     when_created = creation_date(file_save_name)
        #     if current_time > when_created:
        #         return 'Ffmpeg didnt export file'
        #     else:
        #         return 'File exported successfully'
        # except:
        #     return 'Ffmpeg didnt export file'
        # return f'ffmpeg -y -i {self.filepath + ".mp4"} -af "{inside}" {file_save_name}'

    def load_words(self, list_of_words):
        self.list_of_words = list_of_words

    def get_words(self):
        return self.list_of_words

    def create_ffmpeg_string(self, additional_times: List[TimeSegment]) -> str:
        all_times: List[TimeSegment] = [word.time_segment for word in self.list_of_words if word.is_censored] \
                                       + additional_times
        all_times.sort(key=lambda x: x.start.value)

        final_times = get_final_time(all_times)

        # inside = "volume=enable='between(t,5,10)':volume=0, volume=enable='between(t,45,55)':volume=0"

        return ", ".join(["volume=enable='between(t,{start},{end})':volume=0"
                         .format(start=time_segment.start.value, end=time_segment.end.value)
                          for time_segment in final_times])
