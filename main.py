import tkinter as tk
from gui.main_gui import MainGui

def main():
    root = tk.Tk()
    root.title("Manual Image Sort")
    app = MainGui(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
