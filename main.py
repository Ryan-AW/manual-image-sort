''' a program for manually sorting images into directories '''
from config.config_manager import ConfigManager
from gui.main_gui import init_gui
from utils.image_info import ImageInfo


def main():
    ''' initialize program '''
    ConfigManager()
    ImageInfo().open('resources/img_not_found.png')
    init_gui()


if __name__ == "__main__":
    main()
