import tkinter as tk
from .frames.directories_frame import DirectoriesFrame
from .frames.info_frame import InfoFrame

class MainGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.info_frame = InfoFrame(self)
        self.info_frame.pack()

        self.directory_selector = DirectoriesFrame(self)
        self.directory_selector.pack()
