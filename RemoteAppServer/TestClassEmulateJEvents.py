__author__ = 'MrLapTop'
import viz

class jEventObj(object):
    def __init__(self,dicti):
        self.__dict__.update(dicti)

class EmulateJEvents():
    def __init__(self,dicti):
        """
        This class is for Emulating JEvents. Testing if the callbackers are working properly.

        dicti - is a dict.His values are also dict's
        """
        self.dict = {}
        for eventName,jEventArgs in  dicti.iteritems():
            #viz.getEventID(str(eventName)) gives us the eventID of the eventName(key in dicti)
            #and makeing it the new Key of self.dict.
            #self.dict.values are jEventObj(wich makes the passedOn dict to his own Attributes)
            self.dict[viz.getEventID(str(eventName))] = jEventObj(jEventArgs)


    def startJEvents(self,frames=50,loops = None):
        #this funktion should be called from another Thread
        self.counter = loops
        if loops:
            for x in xrange(0,loops):
                viz.waitFrame(frames)
                for k in self.dict:
                    self.sendJEvent(k,self.dict[k])
        else:
            while(1):

                for k in self.dict:
                    viz.waitFrame(frames)
                    self.sendJEvent(k,self.dict[k])

    def sendJEvent(self,eventID,jEObj):
        #This command allows us to send events to the main script thread from different threads.
        # The event is saved in a list, which the main thread processes at the beginning of every frame.
        #Callbackers wich are rigistert to the spezific event, will be noteifide and the jEObj will be passed to them
        viz.postEvent(eventID,jEObj)