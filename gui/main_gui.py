''' compose a gui out of various independent frames '''
import tkinter as tk
from .frames.directories_frame import DirectoriesFrame
from .frames.info_frame import InfoFrame
from .frames.image_frame import ImageFrame

class MainGui(tk.Frame):
    ''' combine various frames into the gui '''
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky='nsew')

        self._left_frame = tk.Frame(self)
        self._left_frame.grid(row=0, column=0, sticky='nsew')

        self._info_frame = InfoFrame(self._left_frame)
        self._info_frame.grid(row=0, column=0, sticky='nsew')

        self._directory_selector = DirectoriesFrame(self._left_frame)
        self._directory_selector.grid(row=1, column=0, sticky='nsew')

        self._image_frame = ImageFrame(self)
        self._image_frame.grid(row=0, column=1, sticky='nsew')



        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self._left_frame.rowconfigure(0, weight=1)
        self._left_frame.rowconfigure(1, weight=1)
