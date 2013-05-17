__author__ = 'MrLapTop'
from Parser import Parser

class Connector(object):

    def __init__(self,parser):
        self.parser = parser

    def feedData(self, data):
        return self.parser.parseJson(data)