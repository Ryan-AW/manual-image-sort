import tkinter as tk
from .frames.directories_frame import DirectoriesFrame

class MainGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.directory_selector = DirectoriesFrame(self)
        self.directory_selector.pack()
