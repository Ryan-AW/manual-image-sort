''' create an array of image paths '''
from pathlib import Path
import os


class ImageArray:
    ''' an array of image paths '''
    _instance = None
    _update_function = lambda: None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ImageArray, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._paths = []
        self._cur_path = ''
        self._raise_image_not_found()

    def load_directory(self, directory):
        ''' scrape all the images from a directory (non-recursive) '''
        image_files = []
        for filename in os.listdir(directory):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff')):
                image_files.append(os.path.join(directory, filename))
        try:
            self._cur_path, *self._paths = image_files
        except ValueError:
            self._raise_image_not_found()

    def cur_path(self):
        ''' return the current image '''
        return self._cur_path

    def next(self):
        ''' move to next image '''
        try:
            self._cur_path = self._paths.pop()
        except IndexError:
            self._raise_image_not_found()
        self._update_function()

    def update(self, function):
        ''' provide a function that shall be run when next() is called '''
        self._update_function = function

    def _raise_image_not_found(self):
        self._paths = []
        self._cur_path = Path(__file__).parent.parent/'resources'/'img_not_found.png'
