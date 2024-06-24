''' implements a tkinter frame with multiple directory selectors '''
import tkinter as tk


class ReadOnlyInfoFrame(tk.Frame):
    ''' tkinter frame for displaying info in the format '<key> <value>' '''
    def __init__(self, master, key, value, max_key_len, max_value_len):
        super().__init__(master)
        self.master = master

        self._key = tk.StringVar()
        self._key.set(key)

        self._value = tk.StringVar()
        self._value.set(value)

        self._max_key_len = max_key_len
        self._max_value_len = max_value_len

        self._create_widgets()

    def _create_widgets(self):
        super().config(pady=5)
        self._key_label = tk.Label(self, textvariable=self._key, anchor='e', width=12)
        self._key_label.pack(side='left')

        self._value_label = tk.Label(self, textvariable=self._value, anchor='e', width=32)
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


class MutableInfoFrame(tk.Frame):
    ''' tkinter frame for displaying info that the user can edit '''
    def __init__(self, master, key, value, max_width):
        super().__init__(master)
        self.master = master

        self._key = tk.StringVar()
        self._key.set(key)

        self._value = tk.StringVar()
        self._value.set(value)

        self._max_width = max_width

        self._create_widgets()

    def _create_widgets(self):
        self._key_label = tk.Label(self, textvariable=self._key, anchor='e', width=self._max_width)
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

class InfoFrame(tk.Frame):
    ''' tkinter frame for displaying file info '''
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._create_widgets()

    def _create_widgets(self):
        # this data will be generated by future code in main_gui.py
        mutable_info = {
            'Parent:': '~/fll/',
            'Filename:': 'default-image',
            'Extension:': 'png'
        }
        max_length = max(len(key) for key in mutable_info)

        # this data will be generated by future code in main_gui.py
        immutable_info = {
            '(SI) File Size:': 'KB 17.108',
            '(IEC) File Size:': 'KiB 16.724',
            'Last Accessed:': '2024-06-21 00:00:00',
            'Last Modified:': '2023-01-26 20:50:36',
            'Time Created:': '2023-01-26 20:50:36',
            'md5 Hash:': 'b3f55a97a806d730a4470a4e2564c681'
        }
        max_key_len = max(len(key) for key in immutable_info)
        max_value_len = max(len(key) for key in immutable_info.values())

        self._mutable_frames = [MutableInfoFrame(self, key, value, max_length) for key, value in mutable_info.items()]
        self._read_only_frames = [ReadOnlyInfoFrame(self, key, value, max_key_len, max_value_len) for key, value in immutable_info.items()]

        for frame in self._mutable_frames:
            frame.pack(fill=tk.X)
        for frame in self._read_only_frames:
            frame.pack()
