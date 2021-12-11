from tkinter import *
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from modules.AudioFile import get_mp4_path, create_wav_from_mp4, AudioFile
from modules.speech_to_text import speech_to_words
from vosk import Model
import subprocess

base_path = str(Path(__file__).parent).replace('\\', '/')
base_path = base_path[:-8]


COL_WIDTHS = {
    "word": 158,
    "start": 92,
    "end": 92,
    "conf": 57,
    "censor": 59,
}

FFMPEG = "ffmpeg"


def check_install(*args):
    try:
        subprocess.check_output(args,
                    stderr=subprocess.STDOUT)
        return True
    except OSError as e:
        return False


def check_ffmpeg():
    """
    Check if ffmpeg is installed.
    """
    return check_install(FFMPEG, "-version")



def btn_clicked():
    print("Button Clicked")


class App:
    def __init__(self):
        self.audio_file: AudioFile = None
        self.model: Model = None
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
            bg = "#dfeeff",
            height = 646,
            width = 1058,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = PhotoImage(file = f"{base_path}/assets/background.png")
        self.background = self.canvas.create_image(
            529.0, 309.5,
            image=self.background_img)

        self.export_name_img = PhotoImage(file = f"{base_path}/assets/export_name.png")
        self.export_name_bg = self.canvas.create_image(
            741.0, 529.5,
            image = self.export_name_img)

        self.export_name = Text(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        self.export_name.place(
            x = 584, y = 519,
            width = 314,
            height = 19)

        self.save_button_img = PhotoImage(file = f"{base_path}/assets/save_button.png")
        self.save_button = Button(
            image = self.save_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat")

        self.save_button.place(
            x = 989, y = 554,
            width = 55,
            height = 26)

        self.export_button_img = PhotoImage(file = f"{base_path}/assets/export_button.png")
        self.export_button = Button(
            image = self.export_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat")

        self.export_button.place(
            x = 584, y = 554,
            width = 196,
            height = 26)

        self.remove_button_img = PhotoImage(file = f"{base_path}/assets/remove_button.png")
        self.remove_button = Button(
            image = self.remove_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat")

        self.remove_button.place(
            x = 1033, y = 344,
            width = 11,
            height = 3)

        self.add_button_img = PhotoImage(file = f"{base_path}/assets/add_button.png")
        self.add_button = Button(
            image = self.add_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat")

        self.add_button.place(
            x = 1007, y = 339,
            width = 11,
            height = 11)

        self.convert_button_img = PhotoImage(file = f"{base_path}/assets/convert_button.png")
        self.convert_button = Button(
            image = self.convert_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.get_speech_to_text,
            relief = "flat")

        self.convert_button.place(
            x = 16, y = 70,
            width = 152,
            height = 26)

        self.load_button_img = PhotoImage(file = f"{base_path}/assets/load_button.png")
        self.load_button = Button(
            image = self.load_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat")

        self.load_button.place(
            x = 987, y = 15,
            width = 55,
            height = 26)

        self.new_project_button_img = PhotoImage(file = f"{base_path}/assets/new_project_button.png")
        self.new_project_button = Button(
            image = self.new_project_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.load_audio_file,
            relief = "flat")

        self.new_project_button.place(
            x = 16, y = 15,
            width = 85,
            height = 26)

        self.forward_button_img = PhotoImage(file = f"{base_path}/assets/forward_button.png")
        self.forward_button = Button(
            image = self.forward_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat")

        self.forward_button.place(
            x = 115, y = 520,
            width = 34,
            height = 34)

        self.back_button_img = PhotoImage(file = f"{base_path}/assets/back_button.png")
        self.back_button = Button(
            image = self.back_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat")

        self.back_button.place(
            x = 82, y = 520,
            width = 34,
            height = 34)

        self.pause_button_img = PhotoImage(file = f"{base_path}/assets/pause_button.png")
        self.pause_button = Button(
            image = self.pause_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat")

        self.pause_button.place(
            x = 48, y = 520,
            width = 34,
            height = 34)

        self.play_button_img = PhotoImage(file = f"{base_path}/assets/play_button.png")
        self.play_button = Button(
            image = self.play_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat")

        self.play_button.place(
            x = 16, y = 520,
            width = 34,
            height = 34)

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
        ]

        # x = 584 y = 111 / 112
        # w = 458
        # h = 207 / 206
        self.words_frame = Frame(self.window, background="#ffffff", highlightbackground="#A3C4D7", highlightthickness=0.5)
        self.words_frame.place(x=585, y=114, width=455 + 10, height=203)

        self.words_scroll = Scrollbar(self.words_frame, width=10)
        self.words_scroll.pack(side=RIGHT, fill=Y)

        self.words_display = ttk.Treeview(self.words_frame, yscrollcommand=self.words_scroll.set)
        self.words_display.pack()

        self.words_scroll.config(command=self.words_display.yview)

        self.words_display['columns'] = list(COL_WIDTHS.keys())
        self.words_display.column("#0", width=0, stretch=NO)
        for col_name in COL_WIDTHS:
            self.words_display.column(col_name, width=COL_WIDTHS[col_name], anchor=CENTER)
            # print(col_name)

        self.set_load_state(DISABLED)

    def start_app(self):
        self.window.resizable(False, False)
        self.window.mainloop()

    def load_audio_file(self):
        f = filedialog.askopenfile(title="Select mp4 file to load into project", initialdir="./sound_files/mp4_files")
        if f is None:
            return
        if not f.name.endswith('.mp4'):
            messagebox.showerror("Error when loading project",
                                 "A file not supported by the application was selected. Please try again.")
        print(f.name)
        self.audio_file = AudioFile(f'{get_mp4_path(f.name)}')

        vosk_f = filedialog.askdirectory(
            title="Select Vosk model directory to convert speech to text, or cancel if model was loaded before.",
            initialdir='./models/')
        if vosk_f is None and self.model is None:
            messagebox.showinfo("Failed to start new project",
                                "No model was selected and loaded. Select new model to convert.")
        # do threading here and make it change a variable
        self.model = Model(model_path=vosk_f)
        self.set_load_state(ACTIVE)
        # file = open(f.name)
        # self.data = json.load(file)
        # self.update_plot()

    def set_load_state(self, state):
        for button in self.buttons_after_load:
            button["state"] = state

    def get_speech_to_text(self):
        if self.model and self.audio_file:
            # get wav file before that
            # subprocess.call(f'ffmpeg -y -i {get_mp4_path(audio_path)}.mp4 {get_mp4_path(audio_path)}.wav')

            list_of_words = speech_to_words(self.audio_file, self.model)
            self.audio_file.load_words(list_of_words=list_of_words)

            if self.words_display:
                for word in self.audio_file.get_words():
                    self.words_display.insert(parent='', index='end', iid=0, text='',
                                              values=(
                                                  word.word, str(word.time_segment.start), str(word.time_segment.end),
                                                  word.conf, word.is_censored))

            # allow for the words to be selectable (censor can be a button)

    def add_additional_time(self):
        pass

    def remove_additional_time(self):
        pass

    def export(self):
        pass

    def save_project(self):
        pass

    def load_project(self):
        pass

    # caly player jeszcze xD xD


