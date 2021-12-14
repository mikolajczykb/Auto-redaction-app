from tkinter import *
import vlc
import time


#
#   Screen widget: Embedded video player from local or youtube
#
class Screen(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        self.settings = {
            "width": 536,
            "height": 388
        }

        # Canvas where to draw video output
        self.canvas = Canvas(
            self,
            width=self.settings['width'],
            height=self.settings['height'],
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack()

        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def get_handle(self):
        # Getting frame ID
        return self.winfo_id()

    def load_video(self, _source):
        # Function to start player from given source
        media = self.instance.media_new(_source)
        media.get_mrl()
        self.player.set_media(media)

        self.player.set_hwnd(self.get_handle())
        self.player.play()
        time.sleep(0.5)
        self.player.pause()

    def play(self):
        if self.player.is_playing() and self.player.will_play():
            self.player.pause()
        else:
            self.player.play()

    def skip_forward(self):
        current_time = self.player.get_time()
        if self.player.will_play():
            length_of_video = self.player.get_length()
            if current_time + 5000 < length_of_video:
                self.player.set_time(current_time + 5000)
            else:
                self.player.set_time(length_of_video)

    def reverse_back(self):
        current_time = self.player.get_time()
        if self.player.will_play():
            length_of_video = self.player.get_length()
            if current_time - 5000 < length_of_video:
                self.player.set_time(current_time - 5000)
            else:
                self.player.set_time(length_of_video)

    def get_current_time(self):
        return self.player.get_time()

    def get_video_length(self):
        return self.player.get_length()

    def set_current_time(self, time_in_milliseconds: int):
        self.player.set_time(time_in_milliseconds)