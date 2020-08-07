from html.parser import HTMLParser
from flask_restful import fields


class HTMLStripper(HTMLParser):
    fed = list()

    def __init__(self):
        self.reset()
        self.fed = []
        self.convert_charrefs = True

    def handle_data(self, data):
        self.fed.append(data)

    def get_data(self):
        return "".join(self.fed)


def strip_tag(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()


class HTMLField(fields.Raw):
    def format(self, value):
        return strip_tag(str(value))
