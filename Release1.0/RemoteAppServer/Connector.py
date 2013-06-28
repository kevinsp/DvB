__author__ = 'MrLapTop'

class Connector(object):

    def __init__(self,parser):
        """
        Connector is a proxy class for being able to use interchangable handlers
        for the incoming data, such as different parsers.
        """

        self.parser = parser

    def feedData(self, data):
        """give the parser something to eat"""

        return self.parser.prepareForParsing(data)

    def connectionInteruppted(self):
        """tell the parser the connection was Interruppted"""

        self.parser.prepareForParsing(None,True)

    def cShutdown(self):
        """Shutting down the parser"""

        self.parser.pShutdown()
        return True