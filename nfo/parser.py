"""Module to parse strings and file to nfo objects."""
from lxml import etree

from nfo.tvshow import TVShow


class NfoParser(object):
    """Lxml etree parser to any of our kodi "nfo" objects.

    https://lxml.de/parsing.html
    """

    def __init__(self):
        self.nfo_object = None
        self.last_tags_parsed = []

    def start(self, tag, attrib):
        if not self.last_tags_parsed:
            # Testing the value of the first tag of the source parsed,
            # to choose the right nfo object
            if tag == TVShow.root_node:
                self.nfo_object = TVShow()
            else:
                raise Exception("root node missing, no nfo object found")

        self.last_tags_parsed.append((tag, []))

    def data(self, data):
        self.last_tags_parsed[-1][1].append(data)

    def comment(self, text):
        pass

    def end(self, tag):
        tag, data = self.last_tags_parsed.pop()
        self.nfo_object.update_data({tag: " ".join(data)})

    def close(self):
        return self.nfo_object


def parse(source):
    """Parse a given source and returns the right Nfo object populated."""
    parser = etree.XMLParser(target=NfoParser())
    return etree.parse(source, parser=parser)
