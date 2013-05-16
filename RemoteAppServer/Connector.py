
import Parser
###
# Connector is a proxy class for being able to use interchangable handlers
# for the incoming data, such as different parsers.
###

class Connector():

    def __init__(self):
        self.parser = Parser()

    def feedData(self, data):
        return self.parser.parseJson(data)