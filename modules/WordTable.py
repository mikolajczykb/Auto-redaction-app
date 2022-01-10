from enum import Enum
from modules.AudioFile import AudioFile
from modules.Table import Table
from modules.Word import Word
from tkinter import Menu, Frame, Scrollbar
from typing import List

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


class WordTable(Table):
    def __init__(self, parent: Frame, scroll: Scrollbar, audio_file: AudioFile):
        super().__init__(master=parent, col_widths=COL_WIDTHS, scroll=scroll)
        self.audio_file: AudioFile = audio_file

        self.reverses = {
            'word_reverse': False,
            'start_reverse': False,
            'end_reverse': False,
            'confidence_reverse': False,
            'is_censored_reverse': False
        }

        # self.bind("<Double-1>", self.censor_selected_word)
        self.bind("<Button-3>", self.popup_selection_menu)
        self.bind("<Button-1>", self.sort_word_treeview)

    def set_audio_file(self, audio_file: AudioFile) -> None:
        self.audio_file = audio_file
        # clear table
        self.clear_all_items()
        # set table
        self.set_words_display(audio_file.list_of_words)

    def set_words_display(self, list_of_words: List[Word]) -> None:
        # maybe export it to window?
        # self.audio_file.list_of_words = list_of_words

        index = 1
        for word in list_of_words:
            print("IS CENSORED BEFORE DISPLAY:", word.is_censored)
            self.insert(parent='', index='end', iid=index, text='',
                        values=(
                                 word.word, str(word.time_segment.start), str(word.time_segment.end),
                                 word.confidence, word.is_censored))
            index += 1

    # get rid of audio file
    def select_all_instances_of_word(self, event) -> None:
        selected_row: str = self.identify_row(event.y)
        if selected_row != '':
            # word_selected = self.audio_file.list_of_words[int(selected_row) - 1]
            word_selected = self.item(selected_row)["values"][0]
            filtered_rows = filter(lambda word: word_selected == self.item(word)["values"][0],
                                   self.get_children())
            # for row_number in filtered_rows:
            self.selection_set(*filtered_rows)

    def censor_selected_word(self, event) -> None:
        selected: List = list(self.selection())
        # print("FOCUS:", self.words_display.focus())
        # print("SELCTED:", selected)
        # self.words_display.selection_set(self.words_display.focus())
        # selected = selected + [self.focus()]
        row_selected: str = self.identify_row(event.y)
        # print(row_selected)
        if row_selected == '':
            return

        # word_index = int(self.words_display.identify_row(event.y)) - 1
        for selection in selected:
            if selection == '':
                continue
            word_index: int = int(selection) - 1
            word_selected: Word = self.audio_file.list_of_words[word_index]
            word_selected.is_censored = not word_selected.is_censored
            self.item(selection, text="", values=(
                word_selected.word, str(word_selected.time_segment.start), str(word_selected.time_segment.end),
                word_selected.confidence, word_selected.is_censored
            ))

    def sort_word_treeview(self, event):
        # selected = self.words_display.focus()
        row_selected = self.identify_row(event.y)
        column_selected = self.identify_column(event.x)
        print("ROW SELECTED:", row_selected)
        # self.clear_words_display()
        if row_selected == '' and self.audio_file:
            self.clear_all_items()
            column_name = WordEnum(column_selected).name
            print("COLUMN NAME:", column_name)
            self.audio_file.sort_words_by(column_name, reverse=self.reverses[f'{column_name}_reverse'])
            self.reverses[f'{column_name}_reverse'] = not self.reverses[f'{column_name}_reverse']
            self.set_words_display(self.audio_file.list_of_words)
            # if column_selected == '#1':

    def popup_selection_menu(self, event) -> None:
        m: Menu = Menu(self.master, tearoff=0)
        m.add_command(label="Select all instances of word",
                      command=lambda: self.select_all_instances_of_word(event))
        m.add_command(label="Select all words", command=lambda: self.select_all_items(event))
        m.add_separator()
        m.add_command(label="Censor / uncensor selected words", command=lambda: self.censor_selected_word(event))
        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()
