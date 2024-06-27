''' a program for manually sorting images into directories '''
from config.config_manager import ConfigManager
from gui.main_gui import init_gui, mainloop
from utils.image_info import ImageInfo


def main():
    ''' initialize program '''
    ConfigManager()
    ImageInfo()

    init_gui()

    mainloop()


if __name__ == "__main__":
    main()
