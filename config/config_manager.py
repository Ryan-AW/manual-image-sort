''' load config file and provides an interface to its values '''
import configparser
import os

class ConfigManager:
    ''' manage config file '''
    _instance = None
    _config = None

    CONFIG_PATH = 'config/config.conf'

    DEFAULT_CONFIG = {
        'directory_entry': {
            'inactive_directory_background': '#100006',
            'inactive_directory_text': '#CDCD00',
            'active_directory_background': '#100006',
            'active_directory_text': '#00CD00',
            'selected_directory_background': '#00CD00',
            'selected_directory_text': '#100006',
            'error_directory_background': '#CD0000',
            'error_directory_text': '#EEEEEE'
        },
        'directory_widget': {
            'background': '#00CD00',
            'label_background': '#00CD00',
            'label_text': '#100006'
        },
        'directories_frame': {
            'background': '#00CD00'
        },
        'image_widget': {
            'image_frame': '#111111',
            'image_border': '#333333'
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
            else:
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
