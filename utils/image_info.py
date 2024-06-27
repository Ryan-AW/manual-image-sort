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
        self._path = None

        self._file_path_info = InfoTable()
        self._file_path_info.append('', '')
        self._file_path_info.append('', '')
        self._file_path_info.append('', '')

        self._file_info = InfoTable()
        self._file_info.append('', '')
        self._file_info.append('', '')
        self._file_info.append('', '')
        self._file_info.append('', '')
        self._file_info.append('', '')
        self._file_info.append('', '')


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

        self._file_info.set(
                0,
                tk.StringVar(value='(SI) File Size:'),
                tk.StringVar(value='')
            )
        self._file_info.set(
                1,
                tk.StringVar(value='(IEC) File Size:'),
                tk.StringVar(value='')
            )
        self._file_info.set(
                2,
                tk.StringVar(value='Last Accessed:'),
                tk.StringVar(value='')
            )
        self._file_info.set(
                3,
                tk.StringVar(value='Last Modified:'),
                tk.StringVar(value='')
            )
        self._file_info.set(
                4,
                tk.StringVar(value='Time Created:'),
                tk.StringVar(value='')
            )
        self._file_info.set(
                5,
                tk.StringVar(value='md5 Hash:'),
                tk.StringVar(value='')
            )


    def open(self, image_path):
        ''' choose image to laod its info '''
        self._path = Path(image_path).resolve()

        self._file_path_info.set_value(0, tk.StringVar(value=self._path.parent))
        self._file_path_info.set_value(1, tk.StringVar(value=self._path.stem))
        self._file_path_info.set_value(2, tk.StringVar(value=self._path.suffix[1:]))

        *_, raw_size, last_accessed, last_modified, time_created = self._path.stat()
        si_size, iec_size = self._convert_bytes(raw_size)

        self._file_info.set_value(0, tk.StringVar(value=si_size))
        self._file_info.set_value(1, tk.StringVar(value=iec_size))
        self._file_info.set_value(2, tk.StringVar(value=datetime.fromtimestamp(last_accessed)))
        self._file_info.set_value(3, tk.StringVar(value=datetime.fromtimestamp(last_modified)))
        self._file_info.set_value(4, tk.StringVar(value=datetime.fromtimestamp(time_created)))
        self._file_info.set_value(5, tk.StringVar(value=self._md5_checksum(image_path)))


    @staticmethod
    def _md5_checksum(path: str):
        with open(path, 'rb') as img_file:
            return md5(img_file.read()).hexdigest()


    @staticmethod
    def _convert_bytes(num_bytes: int):
        si_result = ''
        units = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
        values = [0] * len(units)
        unit_pointer = len(units)-1
        max_unit_pointer = 0
        remainder = num_bytes
        value = None
        while unit_pointer+1:
            value, remainder = divmod(remainder, 1000**unit_pointer)
            values[(len(values)-1)-unit_pointer] = str(value)
            if not max_unit_pointer and values[(len(units)-1)-unit_pointer]:
                max_unit_pointer = (len(units)-1)-unit_pointer
            unit_pointer -= 1
        si_result = units[max_unit_pointer]+' '+'.'.join(values).lstrip('0.')
            

        # this is a very bad implementation. And should be improved
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

        return si_result, iec_total

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
    def si_size(self):
        ''' returns the file size of the image using si units '''
        return self._file_info.get_value(0)

    @property
    def iec_size(self):
        ''' returns the file size of the image using iec units '''
        return self._file_info.get_value(1)


    @property
    def last_accessed(self):
        ''' returns the datetime of when the image was last accessed '''
        return self._file_info.get_value(2)

    @property
    def last_modified(self):
        ''' returns the datetime of when the image was last modified '''
        return self._file_info.get_value(3)

    @property
    def time_created(self):
        ''' returns the datetime of when the image was created '''
        return self._file_info.get_value(4)


    @property
    def checksum(self):
        ''' returns the checksum of the image '''
        return self._file_info.get_value(5)


    @property
    def file_path_table(self):
        ''' returns a table of info about the file system '''
        return self._file_path_info

    @property
    def file_table(self):
        ''' returns a table of info about the image itself '''
        return self._file_info
