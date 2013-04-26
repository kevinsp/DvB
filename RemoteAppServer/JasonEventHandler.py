__author__ = 'MrLapTop'

import viz
import AndroidMSGConvorter

"""This class handels the Events from the Parser for the JasonObj"""
class JasonEventHandler(viz.EventClass):
    def __init__(self,callerClass,**dicti):


        #IMPORTANT: We need to initialize base class
        viz.EventClass.__init__(self)

        #Register callback with our callerClass
        #ls is a list
        #ls[0] is the callbel funk/obj that should be executet when an specifik Event(spezified by eventName) is receved
        #ls[1] is the viz.Pryoriti, if not in list, default is used
        for eventName,ls in dicti.iteritems():
            eventID = viz.getEventID(eventName)
            if len(ls)== 2:
                self.callback(eventID,getattr(callerClass,ls[0]),ls[1])
            else:
                self.callback(eventID,getattr(callerClass,ls[0]))

