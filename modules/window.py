import jsonpickle
import os.path
from tkinter import *
from tkinter import filedialog, messagebox, ttk, font, simpledialog
from pathlib import Path
from modules.AudioFile import get_path_without_mp4, create_wav_from_mp4, check_if_file_created, AudioFile, TimeSegment
from modules.speech_to_text import speech_to_words
from modules.Word import check_if_correct_timestamp_format, convert_timestamp_to_second_format,\
    convert_seconds_to_timestamp_format, Word
from modules.Screen import Screen
from modules.WordTable import WordTable
from modules.TimeTable import TimeTable
from typing import List
from vosk import Model
import subprocess
from enum import Enum
from tkVideoPlayer import TkinterVideo

base_path = str(Path(__file__).parent).replace('\\', '/')
base_path = base_path[:-8]


COL_WIDTHS = {
    "word": 158,
    "start": 92,
    "end": 92,
    "conf": 57,
    "censor": 53,
}

class WordEnum(Enum):
    word = '#1'
    start = '#2'
    end = '#3'
    confidence = '#4'
    is_censored = '#5'


FFMPEG = "ffmpeg"


def check_install(*args) -> bool:
    try:
        subprocess.check_output(args, stderr=subprocess.STDOUT)
        return True
    except OSError as e:
        return False


def check_ffmpeg() -> bool:
    """
    Check if ffmpeg is installed.
    """
    return check_install(FFMPEG, "-version")

class App:
    def __init__(self):
        self.audio_file: AudioFile = None
        self.model: Model = None
        self.video_duration_in_milliseconds = None
        self.model_path = None

        self.set_up_window()
        self.start_app()

    def set_up_window(self):
        if not check_ffmpeg():
            messagebox.showerror("Ffmpeg error!", "Ffmpeg is not installed. The program will now exit.")

        self.window = Tk()

        self.window.geometry("1058x646")
        self.window.configure(bg = "#dfeeff")
        self.canvas = Canvas(
            self.window,
            bg="#dfeeff",
            height=646,
            width=1058,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=f"{base_path}/assets/background.png")
        self.background = self.canvas.create_image(
            529.0, 309.5,
            image=self.background_img)

        self.export_name_img = PhotoImage(file=f"{base_path}/assets/export_name.png")
        self.export_name_bg = self.canvas.create_image(
            741.0, 529.5,
            image=self.export_name_img)

        self.export_name = Text(
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        self.export_name.place(
            x=584, y=519,
            width=314,
            height=19)

        self.additional_times_frame = Frame(self.window, background="#ffffff",
                                            highlightbackground="#A3C4D7",
                                            highlightthickness=0
                                            )


        self.additional_times_frame.place(x=584, y=363, width=458, height=110)

        self.additional_times_scroll = Scrollbar(self.additional_times_frame)
        self.additional_times_scroll.pack(side=RIGHT, fill=Y)

        self.additional_times_display = TimeTable(parent=self.additional_times_frame,
                                                  scroll=self.additional_times_scroll)
        # DONE

        self.words_frame = Frame(self.window, background="#ffffff", highlightbackground="#A3C4D7",
                                 highlightthickness=0)
        self.words_frame.place(x=585, y=94, width=455 + 10, height=223)

        self.words_scroll = Scrollbar(self.words_frame, width=10)
        self.words_scroll.pack(side=RIGHT, fill=Y)

        self.words_display = WordTable(parent=self.words_frame, scroll=self.words_scroll, audio_file=self.audio_file)
        # DONE

        self.save_button_img = PhotoImage(file=f"{base_path}/assets/save_button.png")
        self.save_button = Button(
            image=self.save_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_project,
            relief="flat")

        self.save_button.place(
            x=989, y=554,
            width=55,
            height=26)

        self.export_button_img = PhotoImage(file=f"{base_path}/assets/export_button.png")
        self.export_button = Button(
            image=self.export_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.export,
            relief="flat")

        self.export_button.place(
            x=584, y=554,
            width=196,
            height=26)

        self.remove_button_img = PhotoImage(file=f"{base_path}/assets/remove_button.png")
        self.remove_button = Button(
            image=self.remove_button_img,
            borderwidth=0,
            highlightthickness=0,
            # command=self.remove_additional_time,
            command=self.additional_times_display.remove_additional_time,
            relief="flat")

        self.remove_button.place(
            x=1033, y=344,
            width=11,
            height=3)

        self.add_button_img = PhotoImage(file=f"{base_path}/assets/add_button.png")
        self.add_button = Button(
            image=self.add_button_img,
            borderwidth=0,
            highlightthickness=0,
            # command=self.add_additional_time,
            command=self.additional_times_display.add_additional_time,
            relief="flat")

        self.add_button.place(
            x = 1007, y = 339,
            width=11,
            height=11)

        self.convert_button_img = PhotoImage(file=f"{base_path}/assets/convert_button.png")
        self.convert_button = Button(
            image=self.convert_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.get_speech_to_text,
            relief="flat")

        self.convert_button.place(
            x = 16, y = 70,
            width=152,
            height=26)

        self.load_button_img = PhotoImage(file=f"{base_path}/assets/load_button.png")
        self.load_button = Button(
            image=self.load_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_project,
            relief="flat")

        self.load_button.place(
            x=987, y=15,
            width=55,
            height=26)

        self.new_project_button_img = PhotoImage(file=f"{base_path}/assets/new_project_button.png")
        self.new_project_button = Button(
            image=self.new_project_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_audio_file,
            relief="flat")

        self.new_project_button.place(
            x=16, y=15,
            width=85,
            height=26)

        self.forward_button_img = PhotoImage(file=f"{base_path}/assets/forward_button.png")
        self.forward_button = Button(
            image=self.forward_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.skip_forward,
            relief="flat")

        self.forward_button.place(
            x=115, y=520,
            width=34,
            height=34)

        self.back_button_img = PhotoImage(file=f"{base_path}/assets/back_button.png")
        self.back_button = Button(
            image=self.back_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.go_back,
            relief="flat")

        self.back_button.place(
            x=82, y=520,
            width=34,
            height=34)

        self.pause_button_img = PhotoImage(file=f"{base_path}/assets/pause_button.png")
        self.pause_button = Button(
            image=self.pause_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.pause,
            relief="flat")

        self.pause_button.place(
            x=48, y=520,
            width=34,
            height=34)

        self.play_button_img = PhotoImage(file=f"{base_path}/assets/play_button.png")
        self.play_button = Button(
            image=self.play_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.play,
            relief="flat")

        self.play_button.place(
            x=16, y=520,
            width=34,
            height=34)

        self.current_time = StringVar()
        self.current_time.set(convert_seconds_to_timestamp_format(0))
        self.current_time_label = Label(
            master=self.window,
            font=('Roboto', 9, 'bold'),
            textvariable=self.current_time,
            bg='black',
            fg='white',
            pady=0,
        )
        self.current_time_label.place(x=430, y=528)

        self.video_duration = StringVar()
        self.video_duration.set(convert_seconds_to_timestamp_format(0))
        self.video_duration_label = Label(
            master=self.window,
            font=('Roboto', 9, 'bold'),
            textvariable=self.video_duration,
            bg='black',
            fg='white',
            pady=0,
        )
        self.video_duration_label.place(x=490, y=528)

        self.progress_var = DoubleVar()
        self.video_progress_bar = Scale(
            master=self.window,
            orient=HORIZONTAL,
            bg="black",
            bd=1,
            showvalue=0,
            length=250,
            variable=self.progress_var,
            command=lambda x: self.update_time(),
        )
        self.video_progress_bar.place(x=160, y=526)

        # self.words_display = ttk.Treeview(self.words_frame, yscrollcommand=self.words_scroll.set)
        self.buttons_after_load = [
            self.save_button,
            self.export_button,
            self.remove_button,
            self.add_button,
            self.convert_button,
            self.forward_button,
            self.back_button,
            self.pause_button,
            self.play_button,
            self.video_progress_bar,
        ]

        self.video_frame = Screen(self.window)
        self.video_frame.place(x=16, y=132, width=536, height=388)

        self.selected_time_index = None

        self.set_load_state(DISABLED)

    def start_app(self):
        self.window.resizable(False, False)
        self.window.mainloop()

    def set_load_state(self, state):
        for button in self.buttons_after_load:
            button["state"] = state

    def set_text(self, text):
        self.export_name.delete(1.0, END)
        self.export_name.insert(1.0, text)

    def get_speech_to_text(self):
        self.video_frame.pause()
        if self.model and self.audio_file:
            # get wav file before that
            # subprocess.call(f'ffmpeg -y -i {get_path_without_mp4(audio_path)}.mp4 {get_path_without_mp4(audio_path)}.wav')
            print(self.audio_file.filepath)
            create_wav_from_mp4(self.audio_file.filepath)
            if not check_if_file_created(path_to_file=self.audio_file.filepath + ".wav"):
                messagebox.showerror("Speech to text error!",
                                     "There was an error when trying to run speech to text. Please try again.")

            list_of_words = speech_to_words(self.audio_file, self.model)
            self.audio_file.load_words(list_of_words=list_of_words)

            self.words_display.clear_all_items()
            self.words_display.set_words_display(list_of_words=self.audio_file.get_words())

    def load_audio_file(self):
        self.set_load_state(DISABLED)
        f = filedialog.askopenfile(title="Select mp4 file to load into project", initialdir="./sound_files/mp4_files")
        if f is None:
            return
        if not f.name.endswith('.mp4'):
            messagebox.showerror("Error when loading project",
                                 "A file not supported by the application was selected. Please try again.")
            return

        vosk_f = filedialog.askdirectory(
            title="Select Vosk model directory to convert speech to text, or cancel if model was loaded before.",
            initialdir='./models/')
        if vosk_f == '' and self.model is None:
            messagebox.showinfo("Failed to start new project",
                                "No model was selected and loaded. Select new model to convert.")
            return
        # do threading here and make it change a variable
        # self.vid_player.load(self.audio_file.filepath + ".mp4")
        self.prepare_video_and_model(f'{get_path_without_mp4(f.name)}', vosk_f)

    def prepare_video_and_model(self, video_file_path, model_path):
        self.audio_file = AudioFile(f'{video_file_path}')
        # print(f'VIDEO PATH: {get_path_without_mp4(video_file_path)}')
        if self.model is None:
            try:
                self.model = Model(model_path=model_path)
                self.model_path = model_path
            except:
                messagebox.showerror("Error when creating model",
                                     "A directory not containing a vosk model was selected. Please try again.")

        self.words_display.set_audio_file(self.audio_file)
        self.video_frame.reset_instance(self.audio_file.filepath + ".mp4")
        self.set_load_state(ACTIVE)
        self.reset_video()

    def reset_video(self):
        self.progress_var.set(0)
        self.update_time()
        self.video_duration.set(convert_seconds_to_timestamp_format(self.video_frame.get_video_length() / 1000))
        if self.video_frame.player.will_play():
            self.window.after(10, self.refresh_current_time)

    def update_time(self):
        selection: float = self.progress_var.get() / 100

        self.video_duration_in_milliseconds = max(self.video_frame.get_video_length(), 1)
        current_time_in_milliseconds = int(selection * self.video_duration_in_milliseconds)

        self.video_frame.set_current_time(current_time_in_milliseconds)
        self.current_time.set(convert_seconds_to_timestamp_format(current_time_in_milliseconds / 1000))

    def refresh_current_time(self):
        current_time_in_milliseconds = self.video_frame.get_current_time()
        progress = current_time_in_milliseconds / self.video_duration_in_milliseconds
        self.current_time.set(convert_seconds_to_timestamp_format(current_time_in_milliseconds / 1000))
        self.progress_var.set(progress * 100)
        if self.video_frame.player.will_play():
            self.window.after(10, self.refresh_current_time)

    def play(self):
        self.video_frame.play()

    def pause(self):
        self.video_frame.pause()

    def skip_forward(self):
        self.video_frame.skip_forward()

    def go_back(self):
        self.video_frame.reverse_back()

    def export(self):
        additional_times = self.additional_times_display.get_additional_times_list()
        for time in additional_times:
            print(f"{time.start.value} - {time.end.value}")
        export_input = self.export_name.get("1.0", END).strip()
        print("Export name: ", export_input)
        save_file_name = self.audio_file.export(additional_times, export_input)
        if save_file_name != '':
            print("SAVE FILE NAME:", save_file_name)
            self.video_frame.load_video(save_file_name + '.mp4')
            self.reset_video()

    def save_project(self):
        f = filedialog.asksaveasfile(mode='w', initialdir="./projects", defaultextension=".json")
        if f is None:
            return
        export_input = self.export_name.get("1.0", END).strip()

        additional_times = self.additional_times_display.get_additional_times_list()
        additional_times = list(map(lambda time: {
            'start': time.start.value,
            'end': time.end.value,
        }, additional_times))

        print(additional_times)
        list_of_words = list(map(lambda word: {
            'conf': word.confidence,
            'word': word.word,
            'is_censored': word.is_censored,
            'start': word.time_segment.start.value,
            'end': word.time_segment.end.value
        }, self.audio_file.list_of_words))
        print(list_of_words)
        print(self.audio_file.filepath)
        print(self.model_path)
        print(export_input)

        saveObj = {
            'additional_times': additional_times,
            'list_of_words': list_of_words,
            'video_file_path': self.audio_file.filepath,
            'model_path': self.model_path,
            'project_name': export_input
        }
        f.write(jsonpickle.encode(saveObj))

    def load_project(self):
        self.set_load_state(DISABLED)
        f = filedialog.askopenfile(title="Select project JSON to load into file", initialdir="./sound_files/mp4_files")
        if f is None:
            return
        if not os.path.isfile(f.name):
            messagebox.showerror("File was not found!")

        with open(f.name) as f:
            project_json = jsonpickle.decode(f.read())
            project_json = ProjectJSON(project_json)

        additional_times = []
        for time in project_json.additional_times:
            additional_times.append(TimeSegment(time))

        list_of_words = []
        for word in project_json.list_of_words:
            list_of_words.append(Word(word))

        video_file_path = project_json.video_file_path
        model_path = project_json.model_path
        project_name = project_json.project_name
        print(video_file_path)
        print(model_path)
        try:
            self.prepare_video_and_model(video_file_path, model_path)
        except:
            messagebox.showerror("Failed at setting up video and model!")
        try:
            self.audio_file.list_of_words = list_of_words
            self.words_display.set_audio_file(self.audio_file)
        except:
            messagebox.showerror("Failed at setting up list of words")
        try:
            self.additional_times_display.clear_all_items()
            self.additional_times_display.set_additional_times(additional_times)
        except:
            messagebox.showerror("Failed at setting up additional times!")
        self.set_text(project_name)


class ProjectJSON:
    def __init__(self, config):
        self.additional_times = config['additional_times']
        self.list_of_words = config['list_of_words']
        self.video_file_path = config['video_file_path']
        self.model_path = config['model_path']
        self.project_name = config['project_name']
