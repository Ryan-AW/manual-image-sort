''' a program for manually sorting images into directories '''
import tkinter as tk
from gui.main_gui import MainGui
from config.config_manager import ConfigManager


def main():
    ''' initialize program '''
    ConfigManager()
    root = tk.Tk()
    root.title("Manual Image Sort")
    app = MainGui(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
