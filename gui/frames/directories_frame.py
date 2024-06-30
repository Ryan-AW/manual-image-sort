''' implements a tkinter frame with multiple directory selectors '''
import tkinter as tk
from tkinter import filedialog
from config import ConfigManager


CONFIG = ConfigManager()


class DirectoryBox(tk.Entry):
    ''' wrap tkinter entry to make a text box for directory paths '''
    _config = CONFIG['directory_entry']

    def __init__(self, master, **kwargs):
        self._is_selected = False
        kwargs['state'] = 'disabled'
        kwargs['disabledbackground'] = self._config['inactive_directory_background']
        kwargs['disabledforeground'] = self._config['inactive_directory_text']
        kwargs['readonlybackground'] = self._config['active_directory_background']
        kwargs['foreground'] = self._config['active_directory_text']
        kwargs['highlightthickness'] = 0
        super().__init__(master, **kwargs)


    @property
    def is_selected(self):
        ''' return whether the user has selected this directory '''
        return bool(self)

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
        ''' toggle the selection state of this directory '''
        self.is_selected = not self.is_selected

    def flash_error(self, _unflash=False):
        ''' flash the directory red to indicate an invalid action '''
        if _unflash:
            self.config(disabledbackground=self._config['inactive_directory_background'])
            self.config(disabledforeground=self._config['inactive_directory_text'])
        else:
            self.config(disabledbackground=self._config['error_directory_background'])
            self.config(disabledforeground=self._config['error_directory_text'])
            self.after(100, lambda: self.flash_error(_unflash=True))

    def keybind(self, key: str):
        ''' bind a key on the keyboard to the toggle function '''
        self.bind_all(f'<KeyPress-{key}>', lambda _:self.toggle())

    def __bool__(self):
        return self._is_selected


class SelectButton(tk.Button):
    ''' wraps tkinter button to match the aesthetic '''
    _config = CONFIG['select_button']

    def __init__(self, master, **kwargs):
        kwargs['font'] = ('Segoe UI', 11)
        kwargs['text'] = self._config['legend']
        kwargs['background'] = self._config['background']
        kwargs['foreground'] = self._config['text_color']
        kwargs['activebackground'] = self._config['hover_background']
        kwargs['activeforeground'] = self._config['hover_text_color']
        kwargs['pady'] = 0
        kwargs['relief'] = 'flat'
        kwargs['borderwidth'] = 0
        kwargs['highlightthickness'] = 0

        super().__init__(master, **kwargs)





class DirectorySelectorFrame(tk.Frame):
    ''' tkinter frame for selecting a directory '''
    _config = CONFIG['directory_widget']

    def __init__(self, master, char):
        super().__init__(master)
        self.master = master
        self._char = char

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
        self._directory_entry.keybind(self._char)
        self._directory_entry.keybind('KP_'+self._char)
        self._directory_entry.pack(side='left', fill=tk.X, expand=True)

        self._select_button = SelectButton(self, command=self._on_select)
        self._select_button.pack(fill=tk.Y, expand=True)

    def _on_select(self):
        if dir_path := filedialog.askdirectory():
            self._entry_text.set(dir_path)
            self._directory_entry.config(state='readonly')

    def __bool__(self):
        return bool(self._directory_entry)

    @property
    def directory(self):
        ''' returns the directory '''
        return self._entry_text.get()

    def deselect(self):
        ''' deselect the directory '''
        if self._directory_entry.is_selected:
            self._directory_entry.is_selected = False

    def state(self, state: bool):
        self._directory_entry.is_selected = state


class DirectoriesFrame(tk.Frame):
    ''' tkinter frame with multiple directory selectors '''
    _config = CONFIG['directories_frame']
    _last_state = [None for _ in range(10)]

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._create_widgets()

    def _create_widgets(self):
        self.config(background=self._config['background'])
        self._selectors = [DirectorySelectorFrame(self, str(i)) for i in range(len(self._last_state))]
        for selector in self._selectors:
            selector.pack(fill=tk.X, expand=True)

    @property
    def directories(self):
        ''' return list of user inputted directories '''
        return [selector.directory for selector in self._selectors]

    def clear(self):
        ''' clear all directories' selectors '''
        temp_state = [None]*len(self._last_state)
        for i, selector in enumerate(self._selectors):
            temp_state[i] = bool(selector)
            selector.deselect()

        if True in temp_state:
            self._last_state = temp_state

    def recall(self):
        for selector, state in zip(self._selectors, self._last_state):
            selector.state(state)
