''' create an image datatype '''
from pathlib import Path
from datetime import datetime
from hashlib import md5
import tkinter as tk
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

    def tk_init(self):
        self._file_path_info.set(
                0,
                tk.StringVar(value='Parent:'),
                tk.StringVar(value='')
            )
        self._file_path_info.set(
                1,
                tk.StringVar(value='Filename:'),
                tk.StringVar(value='')
            )
        self._file_path_info.set(
                2,
                tk.StringVar(value='Extension:'),
                tk.StringVar(value='')
            )


    def open(self, image_path):
        ''' choose image to laod its info '''
        self._checksum = self._md5_checksum(image_path)
        self._path = Path(image_path).resolve()

        self._file_path_info.set_value(0, tk.StringVar(value=self._path.parent))
        self._file_path_info.set_value(1, tk.StringVar(value=self._path.stem))
        self._file_path_info.set_value(2, tk.StringVar(value=self._path.suffix[1:]))

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


    @staticmethod
    def _convert_bytes(num_bytes: int):
        # this is a very bad implementation. And should be improved
        si_total = [None for _ in range(6)]
        bytes_remaining = num_bytes
        si_total[0], bytes_remaining = divmod(bytes_remaining, 1000000000000000)
        si_total[1], bytes_remaining = divmod(bytes_remaining, 1000000000000)
        si_total[2], bytes_remaining = divmod(bytes_remaining, 1000000000)
        si_total[3], bytes_remaining = divmod(bytes_remaining, 1000000)
        si_total[4], bytes_remaining = divmod(bytes_remaining, 1000)
        si_total[5] =  bytes_remaining

        z_count = 0
        for item in si_total:
            if item != 0:
                break
            z_count += 1
        si_total = si_total[z_count:]
        si_total = '.'.join(map(str, si_total))
        si_total = ['B ', 'B ','KB ', 'MB ', 'GB ', 'TB ', 'PB '][6-z_count] + si_total

        iec_total = [None for _ in range(6)]
        bytes_remaining = num_bytes
        iec_total[0], bytes_remaining = divmod(bytes_remaining, 1125899906842624)
        iec_total[1], bytes_remaining = divmod(bytes_remaining, 1099511627776)
        iec_total[2], bytes_remaining = divmod(bytes_remaining, 1073741824)
        iec_total[3], bytes_remaining = divmod(bytes_remaining, 1048576)
        iec_total[4], bytes_remaining = divmod(bytes_remaining, 1024)
        iec_total[5] =  bytes_remaining

        z_count = 0
        for item in iec_total:
            if item != 0:
                break
            z_count += 1
        iec_total = iec_total[z_count:]
        iec_total = '.'.join(map(str, iec_total))
        iec_total = ['B ', 'B ','KiB ', 'MiB ', 'GiB ', 'TiB ', 'PiB '][6-z_count] + iec_total

        return si_total, iec_total

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


    @property
    def file_path_table(self):
        return self._file_path_info
