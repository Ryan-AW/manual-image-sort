''' implements a tkinter frame for displaying an image '''
import tkinter as tk
from PIL import ImageTk


class ImageFrame(tk.Frame):
    ''' tkinter frame for displaying an image'''
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self._error_images = {
            'ImageNotFound': ImageTk.PhotoImage(file='resources/img_not_found.png')
        }
        self._image = self._error_images['ImageNotFound']

        self._create_widgets()

    def _create_widgets(self):
        self._image_label = tk.Label(self, image=self._image)
        self._image_label.pack()

    def change_image(self, image: ImageTk.PhotoImage):
        self._image = image
        self._image_label.config(image=self._image)
