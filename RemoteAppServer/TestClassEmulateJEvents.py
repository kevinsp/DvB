__author__ = 'MrLapTop'
import viz
import vizact

class JEventObj(object):
    #the overgiven dict will be convortet into membervarbs (of the createt jEventObj)
    def __init__(self,dicti):
        self.__dict__.update(dicti)

class EmulateJEvents():
    def __init__(self,jEHandler,dicti):
        """
        This class is for Emulating JEvents. Testing if the callbackers are working properly.

        dicti - is a dict -> His values are lists -> Which values are dicts. Example:
          {"JASON_KEYDOWN_EVENT":[{"key":"w"},{"key":"a"}],
           "JASON_IDONTCARE_EVENT": [{"key":"anykey"}]
           }
        """
        self.jEHandler = jEHandler
        #needed for Lisening to the Keybord
        self.listForVizact = []

        self.dict = {}
        #after that self.dict looks like that {"eventID1" : [JEventObj1,JEventObj2], "eventID2" : [JEventObj3]}
        for eventName,jEventArgsList in  dicti.iteritems():
            #jEHandler.getEventID(str(eventName)) gives us the eventID of the eventName
            eventID = jEHandler.getEventID(str(eventName))
            #and makeing it the new Key of self.dict. His value is a freesh list
            self.dict[eventID] = []
            for jEventArgs in jEventArgsList:
                #makeing all ellements from JeventArgsList to JEventObj. Adding them to a list where They belong
                self.dict[eventID].append(JEventObj(jEventArgs))


    #while a spezifik key is down, jEvents will trigger
    def lisenToKeyboard(self):

        for ls in self.dict.itervalues():
           for jEObj in ls:
                if jEObj.key:
                    vizactEObj = vizact.whilekeydown(jEObj.key,self.sendJEvent,self.jEHandler.getEventID("JASON_KEYDOWN_EVENT")
                                                    ,jEObj)
                    self.listForVizact.append(vizactEObj)
        #if we hit spacebar the programm stops reakting to keyboadevents
        unLisen = vizact.onkeydown(" ", self.unLisenToKeyboard)
        self.listForVizact.append(unLisen)

    def unLisenToKeyboard(self):
        for vizactEObj in self.listForVizact:
            vizactEObj.setEnabled(False)


    def sendJEvent(self,eventID,jEObj):
        #This command allows us to send events to the main script thread from different threads.
        # The event is saved in a list, which the main thread processes at the beginning of every frame.
        #Callbackers wich are rigistert to the spezific event, will be noteifide and the jEObj will be passed to them
        viz.postEvent(eventID,jEObj)