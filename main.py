import tkinter
from recurse_browser import recurse_window


if __name__ == "__main__":
    import sys

    recurse_window.Browser().load(sys.argv[1])
    tkinter.mainloop()
