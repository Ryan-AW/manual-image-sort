''' implements a tkinter frame for displaying an image '''
import tkinter as tk
from PIL import Image, ImageTk


class ImageFrame(tk.Frame):
    ''' tkinter frame for displaying an image'''
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._width = 800
        self._height = 600
        
        self._error_images = {
            'ImageNotFound': ImageTk.PhotoImage(file='resources/img_not_found.png')
        }

        self._image = self._error_images['ImageNotFound']
        self._raw_image = None
        self._create_widgets()
        self.load_image('resources/img_not_found.png')
        self.bind("<Configure>", self._on_resize)

    def _create_widgets(self):
        self._image_label = tk.Label(self, image=self._image)
        self._image_label.pack()

    def load_image(self, file_path):
        self._raw_image = Image.open(file_path)
        self._scale_image()

    def _scale_image(self):
        aspect_ratio = self._raw_image.width / self._raw_image.height

        if aspect_ratio > self._width / self._height:
            new_width = self._width
            new_height = int(self._width / aspect_ratio)
        else:
            new_width = int(self._height * aspect_ratio)
            new_height = self._height

        self._raw_image = self._raw_image.resize((new_width, new_height), Image.ANTIALIAS)

        background = Image.new('RGBA', (self._width, self._height), (0, 0, 0, 255))

        x = (self._width - new_width) // 2
        y = (self._height - new_height) // 2
        background.paste(self._raw_image, (x, y), self._raw_image)

        self._image = ImageTk.PhotoImage(background)
        self._image_label.config(image=self._image)

    def _on_resize(self, event):
        print('resizing')
        self._width = event.width
        self._height = event.height
        self._scale_image()

