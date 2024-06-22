''' loads themes config file and provides an interface to its values '''
import configparser
import os

class ConfigManager:
    ''' manage themes from config file '''
    _instance = None
    _config = None

    CONFIG_PATH = 'config/config.conf'

    DEFAULT_CONFIG = {
        'directory_widget': {
            'inactive_directory_background': '#100006',
            'inactive_directory_text': '#CDCD00',
            'active_directory_background': '#100006',
            'active_directory_text': '#00CD00',
            'selected_directory_background': '#00CD00',
            'selected_directory_text': '#100006',
            'error_directory_background': '#CD0000',
            'error_directory_text': '#EEEEEE'
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

        if not os.path.exists(self.CONFIG_PATH) or not self._is_valid():
            self.regenerate_config()
            config.read_dict(self.DEFAULT_CONFIG)
        else:
            config.read(self.CONFIG_PATH)

        self._config = config

    def _is_valid(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.CONFIG_PATH)

            return set(self.DEFAULT_CONFIG).issubset(config.keys())

        except configparser.Error:
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
