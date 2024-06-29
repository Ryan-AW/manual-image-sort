''' implements a tkinter frame for displaying an image '''
import tkinter as tk
from PIL import Image, ImageTk
from config import ConfigManager
from utils import ImageArray, ImageInfo


CONFIG = ConfigManager()
INFO = ImageInfo()
PATHS = ImageArray()


class ImageFrame(tk.Frame):
    ''' tkinter frame for displaying an image'''
    _config = CONFIG['image_widget']

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._width = 800
        self._height = 600


        self._image = None
        self._raw_image = None

        self._create_widgets()

        self.load_image(PATHS.cur_path())

        self.bind("<Configure>", self._on_resize)

    def _create_widgets(self):
        self.config(bg=self._config['image_frame'])

        self._image_label = tk.Label(self, image=self._image)
        self._image_label.config(bg=self._config['image_border'])
        self._image_label.pack()

    def load_image(self, file_path):
        ''' choose the image to display using its file path '''
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

        self._image = self._raw_image.resize((new_width, new_height), Image.ANTIALIAS)

        background = Image.new('RGBA', (self._width, self._height), self._config['image_border'])

        padding_x = (self._width - new_width) // 2
        padding_y = (self._height - new_height) // 2
        background.paste(self._image, (padding_x, padding_y), self._image)

        self._image = ImageTk.PhotoImage(background)
        self._image_label.config(image=self._image)

    def _on_resize(self, event):
        self._width = event.width-2
        self._height = event.height-2
        self._scale_image()
