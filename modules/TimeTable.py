from enum import Enum
from modules.AudioFile import AudioFile
from modules.Table import Table
from modules.Word import Word, TimeSegment, convert_seconds_to_timestamp_format,\
    convert_timestamp_to_second_format, check_if_correct_timestamp_format
from tkinter import Menu, Frame, Scrollbar, simpledialog

from typing import List

COL_WIDTHS = {
    "start": 218,
    "end": 218
}


class TimeEnum(Enum):
    start = '#1'
    end = '#2'


# TODO: cannot set additional time bigger than video length
class TimeTable(Table):
    def __init__(self, parent: Frame, scroll: Scrollbar):
        super().__init__(master=parent, col_widths=COL_WIDTHS, scroll=scroll)

        self.reverses = {
            'start_reverse': False,
            'end_reverse': False,
        }

        self.bind("<Button-1>", self.sort_additional_times)
        self.bind("<Double-1>", self.change_selected_time)

    def sort_additional_times(self, event):
        row_selected: str = self.identify_row(event.y)
        column_selected: str = self.identify_column(event.x)

        if row_selected == '':
            additional_times: List[TimeSegment] = self.get_additional_times_list()
            column_name = TimeEnum(column_selected).name
            additional_times.sort(key=lambda time: getattr(time, column_name).value,
                                  reverse=self.reverses[f'{column_name}_reverse'])
            self.reverses[f'{column_name}_reverse'] = not self.reverses[f'{column_name}_reverse']
            self.clear_all_items()
            self.set_additional_times(additional_times)

    def set_additional_times(self, additional_times: List[TimeSegment]):
        # this can be removed i guess
        # if self.additional_times_display:
        index = 1
        for time in additional_times:
            print(time.start.value, time.end.value)
            print(convert_seconds_to_timestamp_format(time.start.value),
                  convert_seconds_to_timestamp_format(time.end.value))
            self.add_additional_time(convert_seconds_to_timestamp_format(time.start.value),
                                     convert_seconds_to_timestamp_format(time.end.value))

    def add_additional_time(self, start_value='00:00:00', end_value='00:00:00'):
        self.insert(parent='', index='end',
                    values=(start_value, end_value))

    def remove_additional_time(self):
        selected_item: str = self.focus()
        if selected_item:
            self.delete(selected_item)

    def change_selected_time(self, event):
        column: str = self.identify_column(event.x)
        edited_section_name: str = 'start' if column == '#1' else 'end'
        time_stamp = simpledialog.askstring(f"Change {edited_section_name} of timestamp",
                                            f"Input {edited_section_name} date in MM:SS:MMM or MM:SS format",
                                            initialvalue='00:00:000',
                                            parent=self)

        if time_stamp is None:
            return

        if not check_if_correct_timestamp_format(time_stamp):
            simpledialog.messagebox.showerror("Format error!", "Wrong timestamp has been provided, please try again.")
            return

        selected_name: str = self.focus()
        selected = self.set(selected_name)

        if column == '#1':
            selected_start_seconds: float = convert_timestamp_to_second_format(time_stamp)
            selected_end_seconds: float = convert_timestamp_to_second_format(selected["end"])

            self.item(selected_name, text="", values=(
                time_stamp,
                selected["end"] if selected_end_seconds > selected_start_seconds else time_stamp
            ))
        else:
            self.item(selected_name, text="", values=(
                selected["start"], time_stamp
            ))

    def get_additional_times_list(self) -> List[TimeSegment]:
        additional_times: List[TimeSegment] = []
        print("GET ADDITIONAL TIME FROM DISPLAY")
        for line in self.get_children():
            start, end = self.item(line)['values']
            print(start, end)
            additional_times.append(TimeSegment({
                'start': convert_timestamp_to_second_format(start),
                'end': convert_timestamp_to_second_format(end)
            }))
        # for time in additional_times:
        #     print(f"{time.start.value} - {time.end.value}")
        return additional_times
        # times_rows = self.additional_times_display.get_children()
        # additional_times = []
        # for times in times_rows:
        #     times_values = times['values']
        #     print(times['values'][0])
        #     additional_times.append(TimeSegment({'start': times_values['start'], 'end': times_values['end']}))
        # return additional_times





