__author__ = 'MrLapTop'

import viz
import threading

"""This class is an Obj that holds data"""
class JEventObj(object):
    #the overgiven dict will be convortet into membervarbs (of the createt jEventObj)
    def __init__(self,dicti):
        self.__dict__.update(dicti)

"""This class handels the EventIDs and registers callbacks"""
class JasonEventRegister(viz.EventClass):

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


"""This class sends JassonEvents to viz and can be threaded"""

class JasonEventSender(object):
    def __init__(self):
        self.jEventsToSend = {}
        self.shouldIRun = True
        self.lock = threading.Lock()


    def setJEventsObjToSend(self,dicti):
        with self.lock:
                self.jEventsToSend = dicti

    def run(self):
        self.shouldIRun = True
        while True:
            with self.lock:
                if self.shouldIRun:
                    for eventID,jEventObjList in self.jEventsToSend.iteritems():
                        for jEventObj in jEventObjList:
                           self.postJEvent(eventID,jEventObj)

                    #print self.jEventsToSend

                else:
                    self.jEventsToSend.clear()
                    break

            viz.waitFrame(1)

    def stop(self):
        with self.lock:
            self.shouldIRun = False

    def postJEvent(self,eventID,jEObj):
    #This command allows us to send events to the main script thread from different threads.
    # The event is saved in a list, which the main thread processes at the beginning of every frame.
    #Callbackers wich are rigistert to the spezific event, will be noteifide and the jEObj will be passed to them
        viz.postEvent(eventID,jEObj)


"""This Class will interpret the JasonEvents to CamaraMovments"""

class JassonCam():
    #constant definitions
    MOVE_SPEED = 3.0
    TURN_SPEED = 90.0

    def __init__(self,jasonEventRegister,forward='w',backward='s',left='q',right='e',up='r',down='f',turnRight='d',turnLeft='a',pitchDown='h',pitchUp='y',rollRight='j',rollLeft='g',moveMode=viz.REL_LOCAL,moveScale=1.0,turnScale=1.0):
        self.myHandler = jasonEventRegister

        #Register funkt with Events
        self.myHandler.registerCallback(self,JASON_KEYDOWN_EVENT=["onJassonKeyDown"],UPDATE_EVENT=["onCamUpdate"])

        #Movement/turn speeds
        self.moveScale = self.MOVE_SPEED * moveScale
        self.turnScale = self.TURN_SPEED * turnScale
        #Translation mode
        self.moveMode = moveMode

        #set of movement for the next Frame
        self.moveSet = set()
        #helper dict for getting the keys into the moveSet
        self.helperDict = {}

        self.typOfMovment = {}
        #Create movements for each typ
        self.typOfMovment[forward] = viz.Data(index=2,sign=1,move=True)
        self.typOfMovment[backward] = viz.Data(index=2,sign=-1,move=True)
        self.typOfMovment[left] = viz.Data(index=0,sign=-1,move=True)
        self.typOfMovment[right] = viz.Data(index=0,sign=1,move=True)
        self.typOfMovment[up] = viz.Data(index=1,sign=1,move=True)
        self.typOfMovment[down] = viz.Data(index=1,sign=-1,move=True)
        self.typOfMovment[turnRight] = viz.Data(axis=[0,1,0],mode=viz.REL_LOCAL,move=False)
        self.typOfMovment[turnLeft] = viz.Data(axis=[0,-1,0],mode=viz.REL_LOCAL,move=False)
        self.typOfMovment[pitchDown] = viz.Data(axis=[1,0,0],mode=viz.REL_LOCAL,move=False)
        self.typOfMovment[pitchUp] = viz.Data(axis=[-1,0,0],mode=viz.REL_LOCAL,move=False)
        self.typOfMovment[rollRight] = viz.Data(axis=[0,0,-1],mode=viz.REL_LOCAL,move=False)
        self.typOfMovment[rollLeft] = viz.Data(axis=[0,0,1],mode=viz.REL_LOCAL,move=False)

        for typeOfMovment,vizDataObj in self.typOfMovment.iteritems():
            self.__fillHelperDictWithSets(typeOfMovment, vizDataObj)

            #print self.helperDict

    def __fillHelperDictWithSets(self, key, vizDataObj):
        self.helperDict.setdefault(key,set()).add(vizDataObj)


    def onJassonKeyDown(self, jE):
        #print jE.key
        self.moveSet.update(self.helperDict[jE.key])

    def onCamUpdate(self, e):
        #Iterate throught movements that are currently down
        #print self.moveSet
        if self.moveSet:
            move = [0, 0, 0]
            for k in self.moveSet:
                if k.move:
                    move[k.index] += k.sign * e.elapsed * self.moveScale
                else:
                    viz.MainView.setAxisAngle(k.axis[0],k.axis[1],k.axis[2],e.elapsed * self.turnScale,viz.HEAD_ORI,k.mode)
            viz.MainView.setPosition(move,self.moveMode)
            self.moveSet.clear()


