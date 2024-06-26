''' create an image datatype '''
from pathlib import Path
from datetime import datetime
from hashlib import md5


class ImageInfo:
    ''' image type that also has file info '''
    def __init__(self, image_path):
        self._checksum = self._md5_checksum(image_path)

        self._path = Path(image_path)

        self._path_info = {
                'path': self._path,
                'parent': self._path.parent,
                'filename': self._path.stem,
                'extension': self._path.suffix[1:]
        }

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
        return self._path_info['path']

    @property
    def parent(self):
        ''' returns the directory of the image '''
        return self._path_info['parent']

    @property
    def filename(self):
        ''' returns the filename of the image '''
        return self._path_info['filename']

    @property
    def extension(self):
        ''' returns the file extension of the image '''
        return self._path_info['extension']


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
