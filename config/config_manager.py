''' load config file and provides an interface to its values '''
import configparser
from pathlib import Path

class ConfigManager:
    ''' manage config file '''
    _instance = None
    _config = None

    CONFIG_PATH = Path(__file__).parent/'themes'/'theme.conf'

    DEFAULT_CONFIG = {
        'root': {
            'background': '#111111',
            'sub_frame_background': '#111111'
        },
        'directory_entry': {
            'inactive_directory_background': '#100006',
            'inactive_directory_text': '#CDCD00',
            'active_directory_background': '#100006',
            'active_directory_text': '#00EE00',
            'selected_directory_background': '#00EE00',
            'selected_directory_text': '#100006',
            'error_directory_background': '#CD0000',
            'error_directory_text': '#EEEEEE'
        },
        'select_button': {
            'legend': 'Select Directory',
            'background': '#CDCD00',
            'text_color': '#100006',
            'hover_background': '#AFAF06',
            'hover_text_color': '#FFFFFF'
        },
        'directory_widget': {
            'background': '#111111',
            'label_background': '#111111',
            'label_text': '#EEEEEE'
        },
        'directories_frame': {
            'background': '#111111'
        },
        'image_widget': {
            'image_frame': '#111111',
            'image_border': '#333333'
        },
        'mutable_info_frame': {
            'background': '#111111',
            'label_background': '#111111',
            'label_text': '#EEEEEE'
        },
        'source_selector': {
            'background': '#100006',
            'text': '#CDCD00',
            'label_background': '#111111',
            'label_text': '#CDCD00'
        },
        'read_only_frame': {
            'background': '#111111',
            'label_background': '#111111',
            'label_text': '#EEEEEE'
        },
        'info_frame': {
            'background': '#111111'
        }
    }


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        ''' load config file '''
        config = configparser.ConfigParser()
        try:
            config.read(self.CONFIG_PATH)
            config_filtered = {k: v for k, v in config.items() if k!='DEFAULT'}
            if not self._has_same_keys(config_filtered, self.DEFAULT_CONFIG):
                raise ValueError('The Config File Does Not Match The Template')
        except (configparser.Error, ValueError):
            self.regenerate_config()
            config.read_dict(self.DEFAULT_CONFIG)

        self._config = config

    def _has_same_keys(self, dict1:configparser.ConfigParser, dict2: dict):
        if isinstance(dict1, configparser.SectionProxy|configparser.ConfigParser):
            dict1 = dict(dict1)

        if isinstance(dict1, dict):
            if not isinstance(dict2, dict):
                return False

            if set(dict1) <= set(dict2) and set(dict2) <= set(dict1):
                for key, value in dict1.items():
                    if not self._has_same_keys(value, dict2[key]):
                        return False
                return True

        elif not isinstance(dict2, dict):
            return True
        return False


    def regenerate_config(self):
        ''' rewrite config file if it is missing or invalid '''
        config = configparser.ConfigParser()
        config.read_dict(self.DEFAULT_CONFIG)
        with open(self.CONFIG_PATH, 'w', encoding='utf-8') as conf_file:
            config.write(conf_file)

    def __getitem__(self, key):
        return self._config[key]

    def __iter__(self):
        return iter(self._config.keys())
