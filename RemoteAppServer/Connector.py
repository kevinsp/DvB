__author__ = 'MrLapTop'
import Parser

class Connector():

    def __init__(self):
        self.parser = Parser()

    def feedData(self, data):
        return self.parser.parseJson(data)