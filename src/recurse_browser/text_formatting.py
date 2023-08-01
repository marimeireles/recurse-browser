import tkinter.font

from recurse_browser.browser_config import WIDTH, HEIGHT, HSTEP, VSTEP, SCROLL_STEP
from recurse_browser.recurse_requests import request


class Text:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "Text('{}')".format(self.text)


class Tag:
    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return "Tag('{}')".format(self.tag)


def lex(body):
    """
    Strips tags (anything between angle brackets) from body,
    accumulates and and returns the remaining text.
    Differentiates between text chars and tags.
    """
    out = []
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if text:
                out.append(Text(text))
            text = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(text))
            text = ""
        else:
            text += c
    if not in_tag and text:
        out.append(Text(text))
    return out


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

    def __init__(self, tokens):
        self.tokens = tokens
        self.display_list = []

        # cursor_x keeps track of the horizontal text aditions
        self.cursor_x = HSTEP  # Resets horizontal cursor position
        # similarly cursor_y keeps track of the new added lines
        self.cursor_y = VSTEP  # Breaks onto next line
        self.weight = "normal"
        self.style = "roman"
        self.size = 16

        self.line = []
        for tok in tokens:
            self.token(tok)
        self.flush()

    def token(self, tok):
        """
        Applies cosmetic styles to the text according to different HTML tags
        """
        if isinstance(tok, Text):
            self.text(tok)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "br":
            self.flush()
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += VSTEP

    def text(self, tok):
        font = get_font(self.size, self.weight, self.style)
        # splits the list of words gathered in the token method into words
        for word in tok.text.split():
            w = font.measure(word)
            # if word is bigger than the space available in the rest of the line
            # start a new line
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
