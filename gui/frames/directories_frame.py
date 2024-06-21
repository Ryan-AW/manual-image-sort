''' implements a tkinter frame with multiple directory selectors '''
import tkinter as tk
from tkinter import filedialog


class DirectorySelectorFrame(tk.Frame):
    ''' tkinter frame for selecting a directory '''
    def __init__(self, master, char):
        super().__init__(master)
        self.master = master
        self._char = char

        self._has_directory = False

        self._create_widgets()

    def _create_widgets(self):
        self._keybind_label = tk.Label(self, text=self._char+':')
        self._keybind_label.pack(side='left')

        self._entry_text = tk.StringVar()
        self._entry_text.set('No Directory Selected')

        self._directory_entry = tk.Entry(self, textvariable=self._entry_text, state='disabled', width=40)
        self._directory_entry.pack(side='left')

        self._select_button = tk.Button(self, text='Select Directory', command=self._on_select)
        self._select_button.pack()

    def _on_select(self):
        if dir_path := filedialog.askdirectory():
            self._entry_text.set(dir_path)
            self._directory_entry.config(state='readonly')

    def __bool__(self):
        return self._has_directory

    @property
    def directory(self):
        ''' returns the selected directory or returns False if the user hasn't selected one '''
        if self._has_directory:
            return self._entry_text.get()
        return False


class DirectoriesFrame(tk.Frame):
    ''' tkinter frame with multiple directory selectors '''
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._create_widgets()

    def _create_widgets(self):
        self._selectors = [DirectorySelectorFrame(self, str(i)) for i in range(10)]
        for selector in self._selectors:
            selector.pack(expand=True)

    @property
    def directories(self):
        return [selector.directory for selector in self._selectors]
