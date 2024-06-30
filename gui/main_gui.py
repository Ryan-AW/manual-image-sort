''' compose a gui out of various independent frames '''
import tkinter as tk
from .frames import DirectoriesFrame, InfoFrame, ImageFrame
from config import ConfigManager
from utils import ImageArray, ImageInfo


CONFIG = ConfigManager()
PATHS = ImageArray()
INFO = ImageInfo()
root = None


class MainGui(tk.Frame):
    ''' combine various frames into the gui '''
    _config = CONFIG['root']

    def __init__(self, master):
        super().__init__(master)
        super().config(background=self._config['background'])
        self.master = master
        self.grid(row=0, column=0, sticky='nsew')

        self._left_frame = tk.Frame(self, background=self._config['sub_frame_background'])
        self._left_frame.grid(row=0, column=0, sticky='nsew')

        self._info_frame = InfoFrame(self._left_frame)
        self._info_frame.grid(row=0, column=0, sticky='nsew')

        self._directory_selector = DirectoriesFrame(self._left_frame)
        self._directory_selector.grid(row=1, column=0, sticky='nsew')

        self._image_frame = ImageFrame(self)
        PATHS.update(self._image_frame.load_image)
        self._image_frame.grid(row=0, column=1, sticky='nsew')



        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self._left_frame.rowconfigure(0, weight=1)
        self._left_frame.rowconfigure(1, weight=1)


def init_gui():
    global root
    root = tk.Tk()
    root.title("Manual Image Sort")
    app = MainGui(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.bind('<Return>', next_image)
    root.bind('<KP_Enter>', next_image)

def next_image(_):
    PATHS.next()
    INFO.get()

def mainloop():
    global root
    root.mainloop()
