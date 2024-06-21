import tkinter as tk
from .frames.directories_frame import DirectoriesFrame
from .frames.info_frame import InfoFrame
from .frames.image_frame import ImageFrame

class MainGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self._left_frame = tk.Frame(self)
        self._left_frame.pack(fill=tk.BOTH, expand=True, side='left')

        self.info_frame = InfoFrame(self._left_frame)
        self.info_frame.pack()

        self.directory_selector = DirectoriesFrame(self._left_frame)
        self.directory_selector.pack(fill=tk.Y, expand=True)

        self.image_frame = ImageFrame(self)
        self.image_frame.pack(side='right')
