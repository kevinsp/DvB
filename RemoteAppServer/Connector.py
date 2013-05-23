__author__ = 'MrLapTop'
from Parser import Parser
###
# Connector is a proxy class for being able to use interchangable handlers
# for the incoming data, such as different parsers.
###

class Connector(object):

    def __init__(self,parser):
        self.parser = parser

    def feedData(self, data):
        return self.parser.prepareForParsing(data)

    def connectionInteruppted(self):
        self.parser.prepareForParsing(None,True)

    def cStop(self):
        self.parser.pStop()