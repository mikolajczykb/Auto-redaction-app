from tkinter import ttk, NO, CENTER, Frame, Scrollbar


class Table(ttk.Treeview):
    def __init__(self, master: Frame, col_widths, scroll: Scrollbar):
        super().__init__(master=master, yscrollcommand=scroll.set)
        self.pack()

        # self.words_scroll.config(command=self.words_display.yview)
        scroll.config(command=self.yview)

        self['columns'] = list(col_widths.keys())
        self.column("#0", width=0, stretch=NO)
        for col_name in col_widths:
            self.column(col_name, width=col_widths[col_name], anchor=CENTER)
        self.heading("#0", text="", anchor=CENTER)
        for col_name in col_widths:
            self.heading(col_name, text=col_name.capitalize(), anchor=CENTER)

    # def select_all_words(self, event):
    #     selected_row = self.words_display.identify_row(event.y)
    #     if selected_row != '':
    #         self.words_display.selection_set(self.words_display.get_children())
    def select_all_items(self, event):
        selected_row = self.identify_row(event.y)
        if selected_row != '':
            self.selection_set(self.get_children())

    def clear_all_items(self):
        for item in self.get_children():
            self.delete(item)

