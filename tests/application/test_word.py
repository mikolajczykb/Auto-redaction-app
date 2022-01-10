import unittest
from modules.Word import convert_timestamp_to_second_format, convert_seconds_to_timestamp_format, \
    check_if_correct_timestamp_format


class TestWord(unittest.TestCase):
    def test_empty_timestamp(self):
        timestamp = ''
        self.assertEqual(False, check_if_correct_timestamp_format(timestamp))

    def test_format_too_many_seconds(self):
        timestamp = '4:569:569'
        self.assertEqual(False, check_if_correct_timestamp_format(timestamp))

    def test_format_too_many_milliseconds(self):
        timestamp = '4:56:5940'
        self.assertEqual(False, check_if_correct_timestamp_format(timestamp))

    def test_format_too_few_milliseconds(self):
        timestamp = '4:56:1'
        self.assertEqual(False, check_if_correct_timestamp_format(timestamp))

    def test_format_no_minutes(self):
        timestamp = '56:459'
        self.assertEqual(False, check_if_correct_timestamp_format(timestamp))

    def test_full_timestamp_conversion(self):
        timestamp = '00:01:590'
        self.assertEqual(1.590, convert_timestamp_to_second_format(timestamp))

    def test_short_timestamp_conversion(self):
        timestamp = '5:05'
        self.assertEqual(305, convert_timestamp_to_second_format(timestamp))

    def test_full_timestamp_with_minutes_conversion(self):
        timestamp = '01:04:352'
        self.assertEqual(64.352, convert_timestamp_to_second_format(timestamp))

    def test_empty_timestamp_conversion(self):
        timestamp = '00:00:000'
        self.assertEqual(0, convert_timestamp_to_second_format(timestamp))

    def test_wrong_timestamp_conversion(self):
        timestamp = '34:352:1234'
        self.assertEqual(-1, convert_timestamp_to_second_format(timestamp))

    def test_seconds_to_timestamp_conversion(self):
        seconds = 127.54
        self.assertEqual('2:07:540', convert_seconds_to_timestamp_format(seconds))

    def test_seconds_zero_value_conversion(self):
        seconds = 0
        self.assertEqual('0:00:000', convert_seconds_to_timestamp_format(seconds))


if __name__ == "__main__":
    unittest.main(TestWord())