import tkinter

from recurse_browser.browser_config import WIDTH, HEIGHT, HSTEP, VSTEP, SCROLL_STEP
from recurse_browser.recurse_requests import request
from recurse_browser.text_formatting import lex, Layout

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.display_list = []
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)  # Scrolls when down key is presses

    def draw(self):
        """
        Loops through each tuple in display_list and draws
        character at its x,y coordinates
        """
        # erases canvas before text is redrawn during scrolling
        self.canvas.delete(
            "all"
        )

        for x, y, word, font in self.display_list:
            # performance enhancement, prevents redrawing pixels that are off screen
            if y > self.scroll + HEIGHT:
                continue  # skips character below viewing window
            if y + VSTEP < self.scroll:
                continue  # skips character above viewing window

            self.canvas.create_text(x, y - self.scroll, text=word, font=font, anchor="nw")

    def load(self, url):
        headers, body = request(url)
        tokens = lex(body)
        self.display_list = Layout(tokens).display_list
        self.draw()

    def scrolldown(
        self, e
    ):  # e is an event object that's passed to Tk, but isn't used here
        self.scroll += SCROLL_STEP
        self.draw()
