''' a program for manually sorting images into directories '''
from config import ConfigManager
from gui import init_gui, mainloop
from utils import ImageInfo, ImageArray


def main():
    ''' initialize program '''
    ConfigManager()
    ImageArray()
    ImageInfo()

    init_gui()

    mainloop()


if __name__ == "__main__":
    main()
