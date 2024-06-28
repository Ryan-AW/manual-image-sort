''' implements a tkinter frame with multiple directory selectors '''
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from config import ConfigManager
from utils import InfoTable, ImageInfo


CONFIG = ConfigManager()
INFO = ImageInfo()


class MutableInfoFrame(tk.Frame):
    ''' tkinter frame for displaying info that the user can edit '''
    _config = CONFIG['mutable_info_frame']

    def __init__(self, master, info_table: InfoTable, index: int):
        super().__init__(master)
        self.master = master
        self._index = index

        self._info_table = info_table
        self._key = info_table.get_key(index)
        self._value = info_table.get_value(index)

        self._create_widgets()

    def _create_widgets(self):
        super().config(background=self._config['background'])
        self._key_label = tk.Label(
                self,
                textvariable=self._key,
                anchor='e',
                width=self._info_table.max_key_len,
                background=self._config['label_background'],
                foreground=self._config['label_text']
            )
        self._key_label.pack(side='left')

        self._value_entry = tk.Entry(self, textvariable=self._value, state='readonly')
        self._value_entry.pack(side='left', fill=tk.X, expand=True)

        self._edit_button = tk.Button(self, command=self._on_edit)
        self._edit_button.pack()

    def _on_edit(self):
        cur_state = self._value_entry.cget('state')
        if cur_state == 'normal':
            self._value_entry.configure(state='readonly')
        else:
            self._value_entry.configure(state='normal')

    @property
    def key(self):
        ''' get the legend/key of the info '''
        return self._key.get()

    @property
    def value(self):
        ''' get the value of the info '''
        return self._value.get()

    @key.setter
    def key(self, key: str):
        ''' change the legend/key of the info '''
        self._key.set(key)

    @value.setter
    def value(self, value: str):
        ''' change the value of the info '''
        self._value.set(value)


class SourceDirectorySelector(MutableInfoFrame):
    _source_config = CONFIG['source_selector']
    def __init__(self, master, info_table: InfoTable, index: int):
        super().__init__(master, info_table, index)
        self._key_label.config(
                background=self._source_config['label_background'],
                foreground=self._source_config['label_text']
            )

        self._value_entry.config(
                readonlybackground=self._source_config['background'],
                foreground=self._source_config['text'],
                highlightthickness = 0
            )

    def _on_edit(self):
        if dir_path := filedialog.askdirectory():
            self._info_table.get_value(self._index).set(dir_path)


class ReadOnlyInfoFrame(tk.Frame):
    ''' tkinter frame for displaying info in the format '<key> <value>' '''
    _config = CONFIG['read_only_frame']

    def __init__(self, master, info_table: InfoTable, index: int):
        super().__init__(master)
        self.master = master

        self._info_table = info_table
        self._key = info_table.get_key(index)
        self._value = info_table.get_value(index)

        self._create_widgets()

    def _create_widgets(self):
        super().config(pady=5)
        super().config(background=self._config['background'])
        self._key_label = tk.Label(
                self,
                textvariable=self._key,
                anchor='e',
                width=self._info_table.max_key_len,
                font=('Consolas', 10),
                background=self._config['label_background'],
                foreground=self._config['label_text']
            )
        self._key_label.pack(side='left')

        self._value_label = tk.Label(
                self,
                textvariable=self._value,
                anchor='e',
                width=self._info_table.max_value_len,
                font=('Consolas', 10),
                background=self._config['label_background'],
                foreground=self._config['label_text']
            )
        self._value_label.pack(side='right')

    @property
    def key(self):
        ''' get the legend/key of the info '''
        return self._key.get()

    @property
    def value(self):
        ''' get the value of the info '''
        return self._value.get()

    @key.setter
    def key(self, key: str):
        ''' change the legend/key of the info '''
        self._key.set(key)

    @value.setter
    def value(self, value: str):
        ''' change the value of the info '''
        self._value.set(value)


class InfoFrame(tk.Frame):
    ''' tkinter frame for displaying file info '''
    _config = CONFIG['info_frame']

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._create_widgets()

    def _create_widgets(self):
        super().config(background=self._config['background'])

        INFO.tk_init()

        # remove this line when image loading logic is implemented
        INFO.open(Path(__file__).parent.parent.parent/'resources'/'img_not_found.png')

        mutable_info = INFO.file_path_table
        immutable_info = INFO.file_table

        self._source_directory = SourceDirectorySelector(self, mutable_info, 0)
        self._source_directory.pack(fill=tk.X)

        self._mutable_frames = []
        for i in range(1, len(mutable_info)):
            self._mutable_frames.append(MutableInfoFrame(self, mutable_info, i))
            self._mutable_frames[-1].pack(fill=tk.X)

        self._immutable_frames = []
        for i in range(len(immutable_info)):
            self._immutable_frames.append(ReadOnlyInfoFrame(self, immutable_info, i))
            self._immutable_frames[-1].pack(fill=tk.X)
