''' implements a tkinter frame with multiple directory selectors '''
import tkinter as tk
from tkinter import filedialog
from config.config_manager import ConfigManager


CONFIG = ConfigManager()


class DirectoryBox(tk.Entry):
    ''' wrap tkinter entry to make a text box for directory paths '''
    _config = CONFIG['directory_entry']

    def __init__(self, *args, **kwargs):
        self._is_selected = False
        kwargs['state'] = 'disabled'
        kwargs['disabledbackground'] = self._config['inactive_directory_background']
        kwargs['disabledforeground'] = self._config['inactive_directory_text']
        kwargs['readonlybackground'] = self._config['active_directory_background']
        kwargs['foreground'] = self._config['active_directory_text']
        super().__init__(*args, **kwargs)

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool):
        if super().__getitem__('state') == 'readonly':
            self._is_selected = bool(value)
            if self._is_selected:
                super().config(readonlybackground=self._config['selected_directory_background'])
                super().config(foreground=self._config['selected_directory_text'])
            else:
                super().config(readonlybackground=self._config['active_directory_background'])
                super().config(foreground=self._config['active_directory_text'])
        else:
            self.flash_error()

    def toggle(self):
        self.is_selected = not self.is_selected

    def flash_error(self, _unflash=False):
        if _unflash:
            self.config(disabledbackground=self._config['inactive_directory_background'])
            self.config(disabledforeground=self._config['inactive_directory_text'])
        else:
            self.config(disabledbackground=self._config['error_directory_background'])
            self.config(disabledforeground=self._config['error_directory_text'])
            self.after(100, lambda: self.flash_error(_unflash=True))




class DirectorySelectorFrame(tk.Frame):
    ''' tkinter frame for selecting a directory '''
    _config = CONFIG['directory_widget']

    def __init__(self, master, char):
        super().__init__(master)
        self.master = master
        self._char = char

        self._has_directory = False

        self._create_widgets()

    def _create_widgets(self):
        self.config(background=self._config['background'])
        self._keybind_label = tk.Label(
                self,
                text=self._char+':',
                background=self._config['label_background'],
                foreground=self._config['label_text']
            )
        self._keybind_label.pack(side='left')

        self._entry_text = tk.StringVar()
        self._entry_text.set('No Directory Selected')

        self._directory_entry = DirectoryBox(self, textvariable=self._entry_text)
        self._directory_entry.pack(side='left', fill=tk.X, expand=True)

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
    _config = CONFIG['directories_frame']

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._create_widgets()

    def _create_widgets(self):
        self.config(background=self._config['background'])
        self._selectors = [DirectorySelectorFrame(self, str(i)) for i in range(10)]
        for selector in self._selectors:
            selector.pack(fill=tk.X, expand=True)

    @property
    def directories(self):
        return [selector.directory for selector in self._selectors]
