''' a program for manually sorting images into directories '''
from config.config_manager import ConfigManager
from gui.main_gui import init_gui


def main():
    ''' initialize program '''
    ConfigManager()
    init_gui()


if __name__ == "__main__":
    main()
