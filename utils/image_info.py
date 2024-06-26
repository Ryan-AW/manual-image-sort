''' create an image datatype '''
from pathlib import Path
from datetime import datetime


class ImageInfo:
    ''' image type that also has file info '''
    def __init__(self, image_path):
        self._path = Path(image_path).resolve()

        self._path_info = {
                'path': self._path,
                'parent': self._path.parent,
                'filename': self._path.stem,
                'extension': self._path.suffix[1:]
        }

        *_, raw_size, last_accessed, last_modified, time_created = self._path.stat()

        self._last_accessed_utc = datetime.fromtimestamp(last_accessed)
        self._last_modified_utc = datetime.fromtimestamp(last_modified)
        self._created_utc = datetime.fromtimestamp(time_created)


ImageInfo(Path(__file__).parent.parent/'resources/img_not_found.png')
