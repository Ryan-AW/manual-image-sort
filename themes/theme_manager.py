''' loads themes config file and provides an interface to its values '''
import configparser
import os

class ThemeManager:
    ''' manage themes from config file '''
    _instance = None
    _theme_settings = None

    CONFIG_PATH = 'themes/theme.conf'

    DEFAULT_CONFIG = {
        'THEME': {
            'inactive_directory_background': '#100006',
            'inactive_directory_text': '#CDCD00',
            'active_directory_background': '#100006',
            'active_directory_text': '#00CD00',
            'selected_directory_background': '#00CD00',
            'selected_directory_text': '#100006',
            'image_frame': '#111111',
            'image_border': '#333333'
        }
    }


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
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

        self._theme_settings = config['THEME']

    def _is_valid(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.CONFIG_PATH)

            return 'THEME' in config and \
                set(self.DEFAULT_CONFIG['THEME']).issubset(config['THEME'].keys())

        except configparser.Error:
            return False

    def regenerate_config(self):
        ''' rewrite config file if it is missing or invalid '''
        config = configparser.ConfigParser()
        config.read_dict(self.DEFAULT_CONFIG)
        with open(self.CONFIG_PATH, 'w', encoding='utf-8') as conf_file:
            config.write(conf_file)

    def get(self, key):
        ''' return the theme's value '''
        return self._theme_settings.get(key)

    def __iter__(self):
        return iter(self._theme_settings.keys())
