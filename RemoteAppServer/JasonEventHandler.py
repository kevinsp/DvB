__author__ = 'MrLapTop'

import viz
import AndroidMSGConvorter



"""This class handels the Events from the Parser for the JasonObj"""
class JasonEventHandler(viz.EventClass):

    def __init__(self):
        #IMPORTANT: We need to initialize base class
        viz.EventClass.__init__(self)

        self.dictOfEvents = {}

    def registerCallback(self, callerClass, **dicti):
        #Registers callback with our callerClass
        #ls is a list
        #ls[0] is the callebel funk/obj that should be executet when an specifik Event(spezified by eventName) is receved
        #ls[1] is the viz.Pryoriti, if not spezifide , default is used
        for eventName,ls in dicti.iteritems():
            self.eventID = self.getEventID(eventName)
            if len(ls)== 2:
                self.callback(self.eventID, getattr(callerClass,ls[0]), ls[1])
            else:
                self.callback(self.eventID, getattr(callerClass, ls[0]))

    def getEventID(self, eventName):
        return self.dictOfEvents.setdefault(eventName,viz.getEventID(eventName))
