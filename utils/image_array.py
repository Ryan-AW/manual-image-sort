''' create an array of image paths '''
from pathlib import Path
import os


class ImageArray:
    ''' an array of image paths '''
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ImageArray, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._paths = []
        self._cur_path = ''

    def load_directory(self, directory):
        ''' scrape all the images from a directory (non-recursive) '''
        image_files = []
        for filename in os.listdir(directory):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff')):
                image_files.append(os.path.join(directory, filename))
        try:
            self._cur_path, *self._paths = image_files
        except ValueError:
            self._paths = []
            self._cur_path = Path(__file__).parent/'resources'/'img_not_found.png'

    def cur_path(self):
        ''' return the current image '''
        return self._cur_path

    def next(self):
        ''' move to next image '''
        self._cur_path = self._paths.pop()
