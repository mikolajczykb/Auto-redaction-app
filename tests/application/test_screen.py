import unittest
from tkinter import Tk
from modules.Screen import Screen

MP4_FILEPATH = r'C:\Users\uncha\Desktop\Auto redaction app\sound_files\mp4_files\VID_20170428_234922.344 - Inside Store'


class TestScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.master = Tk()
        cls.screen = Screen(cls.master)
        cls.screen.load_video(MP4_FILEPATH + ".mp4")

    def test_is_video_loaded(self):
        current_time = self.screen.get_current_time()
        self.assertTrue(current_time > 0)

    def test_set_current_time(self):
        self.screen.set_current_time(5000)
        current_time = self.screen.get_current_time()
        self.assertTrue(current_time == 5000)

    def test_skip_forward(self):
        current_time = self.screen.get_current_time()
        self.screen.skip_forward()
        self.assertEqual(current_time + 5000, self.screen.get_current_time())

    def test_reverse_back(self):
        self.screen.set_current_time(8000)
        current_time = self.screen.get_current_time()
        self.screen.reverse_back()
        self.assertEqual(3000, self.screen.get_current_time())

    def test_reverse_back_if_five_seconds_didnt_pass(self):
        self.screen.set_current_time(4000)
        current_time = self.screen.get_current_time()
        self.screen.reverse_back()
        self.assertEqual(0, self.screen.get_current_time())
