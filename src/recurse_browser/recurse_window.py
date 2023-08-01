import tkinter

from recurse_browser.recurse_requests import request

# from recurse_requests import request

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18  # Horizontal and vertical pixel sizes
SCROLL_STEP = 100


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
        self.canvas.delete(
            "all"
        )  # erases canvas before text is redrawn during scrolling
        for x, y, c in self.display_list:
            # performance enhancement, prevents redrawing pixels that are off screen
            if y > self.scroll + HEIGHT:
                continue  # skips character below viewing window
            if y + VSTEP < self.scroll:
                continue  # skips character above viewing window

            self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, url):
        headers, body = request(url)
        text = lex(body)
        self.display_list = layout(text)
        self.draw()

    def scrolldown(
        self, e
    ):  # e is an event object that's passed to Tk, but isn't used here
        self.scroll += SCROLL_STEP
        self.draw()


def layout(text):
    """
    Computes and stores the position of each character in text
    as a tuple in display_list
    """
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP  # Breaks onto next line
            cursor_x = HSTEP  # Resets horizontal cursor position
    return display_list


def lex(body):
    """
    Strips tags (anything between angle brackets) from body,
    accumulates and and returns the remaining text.
    """
    text = ""
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            text += c
    return text
