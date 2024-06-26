''' create an image datatype '''
from pathlib import Path
from datetime import datetime
from hashlib import md5
from utils.info_table import InfoTable


class ImageInfo:
    ''' image type that also has file info '''
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ImageInfo, cls).__new__(cls)
        return cls._instance


    def __init__(self):
        self._file_path_info = InfoTable()
        self._file_path_info.append('parent', '')
        self._file_path_info.append('filename', '')
        self._file_path_info.append('extension', '')

        self._checksum = None
        self._path = None

        self._file_datetimes = {
                'accessed': None,
                'modified': None,
                'created': None
        }


    def open(self, image_path):
        ''' choose image to laod its info '''
        self._checksum = self._md5_checksum(image_path)
        self._path = Path(image_path).resolve()

        self._file_path_info.set_value(0, self._path.parent)
        self._file_path_info.set_value(1, self._path.stem)
        self._file_path_info.set_value(2, self._path.suffix[1:])

        *_, raw_size, last_accessed, last_modified, time_created = self._path.stat()

        self._file_datetimes = {
                'accessed': datetime.fromtimestamp(last_accessed),
                'modified': datetime.fromtimestamp(last_modified),
                'created': datetime.fromtimestamp(time_created)
                }


    @staticmethod
    def _md5_checksum(path: str):
        with open(path, 'rb') as img_file:
            return md5(img_file.read()).hexdigest()


    @property
    def path(self):
        ''' returns the image's path '''
        return self._path

    @property
    def parent(self):
        ''' returns the directory of the image '''
        return self._file_path_info.get_value(0)

    @property
    def filename(self):
        ''' returns the filename of the image '''
        return self._file_path_info.get_value(1)

    @property
    def extension(self):
        ''' returns the file extension of the image '''
        return self._file_path_info.get_value(2)


    @property
    def last_accessed(self):
        ''' returns the datetime of when the image was last accessed '''
        return self._file_datetimes['accessed']

    @property
    def last_modified(self):
        ''' returns the datetime of when the image was last modified '''
        return self._file_datetimes['modified']

    @property
    def time_created(self):
        ''' returns the datetime of when the image was created '''
        return self._file_datetimes['created']


    @property
    def checksum(self):
        ''' returns the checksum of the image '''
        return self._checksum
