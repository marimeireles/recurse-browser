import tkinter.font
from recurse_browser.browser_config import WIDTH, HSTEP, VSTEP
from recurse_browser.html_parser import Text

FONTS = {}


def get_font(size, weight, slant):
    """Implement cache for fonts"""
    key = (size, weight, slant)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight, slant=slant)
        FONTS[key] = font
    return FONTS[key]


class Layout:
    """
    Computes and stores the position of each character in text
    as a tuple in display_list
    """

    def __init__(self, tree):
        self.display_list = []

        # cursor_x keeps track of the horizontal text additions
        self.cursor_x = HSTEP
        # similarly cursor_y keeps track of the new added lines
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 16

        self.line = []
        self.recurse(tree)
        self.flush()

    def recurse(self, tree):
        if isinstance(tree, Text):
            for word in tree.text.split():
                self.word(word)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close_tag(tree.tag)

    def open_tag(self, tag):
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        elif tag == "br":
            self.flush()

    def close_tag(self, tag):
        if tag == "i":
            self.style = "roman"
        elif tag == "b":
            self.weight = "normal"
        elif tag == "small":
            self.size += 2
        elif tag == "big":
            self.size -= 4
        elif tag == "p":
            self.flush()
            self.cursor_y += VSTEP

    def word(self, word):
        font = get_font(self.size, self.weight, self.style)
        w = font.measure(word)
        if self.cursor_x + w > WIDTH - HSTEP:
            self.flush()
        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + font.measure(" ")

    def flush(self):
        """Adds new line"""
        if not self.line:
            return
        metrics = [font.metrics() for x, word, font in self.line]
        # finds word with largest vertical ascent
        max_ascent = max([metric["ascent"] for metric in metrics])
        # calculates a line that will serve as a metric to "hang" all words in
        baseline = self.cursor_y + 1.25 * max_ascent

        # places each word in the line in baseline height
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))

        # resets vars for a new text input in a new line
        self.cursor_x = HSTEP
        self.line = []

        # finds word with largest vertical descent
        max_descent = max([metric["descent"] for metric in metrics])

        self.cursor_y = baseline + 1.25 * max_descent
