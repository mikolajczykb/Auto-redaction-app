import unittest
from modules.AudioFile import AudioFile, get_final_time
from modules.Word import TimeSegment
from modules.speech_to_text import speech_to_words
from vosk import Model

MP4_FILEPATH = r'C:\Users\uncha\Desktop\Auto redaction app\sound_files\mp4_files\VID_20170428_234922.344 - Inside Store'
MODEL_DIRPATH = r'C:\Users\uncha\Desktop\Auto redaction app\models\vosk-model-en-us-0.22'


class TestAudioFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audio_file = AudioFile(MP4_FILEPATH)
        cls.model = Model(MODEL_DIRPATH)
        cls.list_of_words = speech_to_words(cls.audio_file, cls.model)

    def test_if_speech_to_text_returns_words(self):
        self.assertTrue(len(self.list_of_words) > 1)

    def test_if_words_have_proper_format(self):
        word = self.list_of_words[0]
        self.assertTrue(len(word.word) > 1)
        self.assertTrue(word.time_segment and word.time_segment.start.value > 0)
        self.assertTrue(word.time_segment and word.time_segment.end.value > 0)
        self.assertTrue(word.confidence and word.confidence > 0)
        self.assertTrue(word.is_censored is not None)

    def test_save_file_name_without_argument(self):
        self.assertEqual(MP4_FILEPATH + "_output.mp4", self.audio_file.get_output_file_name())

    def test_save_file_name_with_argument(self):
        output_file_name = r'C:\Users\uncha\Desktop\Auto redaction app\sound_files\mp4_files\whatsup.mp4'
        self.assertTrue(output_file_name, self.audio_file.get_output_file_name('whatsup'))

    def test_create_ffmpeg_string(self):
        self.audio_file.load_words(self.list_of_words)
        self.audio_file.list_of_words[0].is_censored = True
        self.audio_file.list_of_words[1].is_censored = True
        self.audio_file.list_of_words[2].is_censored = True
        self.audio_file.list_of_words[3].is_censored = True
        self.assertEqual("volume=enable='between(t,0.27,20.16)':volume=0, volume=enable='between(t,20.19,34.44)':" +
                         "volume=0, volume=enable='between(t,34.74,34.86)':volume=0",
                         self.audio_file.create_ffmpeg_string([]))

    def test_get_final_time_intersected(self):
        additional_times = [TimeSegment({
            'start': 0.5,
            'end': 0.7
        }), TimeSegment({
            'start': 0.6,
            'end': 1.3
        }), TimeSegment({
            'start': 1.5,
            'end': 2.4
        })]
        final_time = get_final_time(additional_times)
        self.assertEqual(final_time[0].end, 1.3)
        self.assertEqual(final_time[1].start, 1.5)
        self.assertEqual(final_time[1].end, 2.4)

    def test_get_final_time_separate(self):
        additional_times = [TimeSegment({
            'start': 0.5,
            'end': 0.7
        }), TimeSegment({
            'start': 1.5,
            'end': 2.4
        })]
        final_time = get_final_time(additional_times)
        self.assertEqual(final_time[0].end, 0.7)
        self.assertEqual(final_time[1].start, 1.5)
        self.assertEqual(final_time[1].end, 2.4)


if __name__ == "__main__":
    unittest.main(TestAudioFile())