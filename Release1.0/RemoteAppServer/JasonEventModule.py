__author__ = 'MrLapTop'

import viz
import threading


class JEventObj(object):
    """This class is an Obj that holds data"""

    def __init__(self,dicti):
        """the overgiven dict will be convortet into membervarbs (of the createt jEventObj)"""
        self.__dict__.update(dicti)


class JasonEventRegister(viz.EventClass):
    """This class handels the EventIDs and registers callbacks"""

    def __init__(self):

        viz.EventClass.__init__(self) #: IMPORTANT: We need to initialize base class
        self.dictOfEvents = {} #: A dict. where the key = eventName and the value = eventID

    def registerCallback(self, callerClass, **dicti):
        """
        Registers callback with our callerClass and manages the eventID's

        @param dicti: key = eventName and value = a list.
            list[0] is the callable funk/obj that should be executed when an specific Event(specified by eventName) is received.
            list[1] is the viz.Priority, if not specified , default is used.
        @type dicti: dict
        """

        for eventName,ls in dicti.iteritems():
            self.eventID = self.getEventID(eventName)
            if len(ls)== 2:
                self.callback(self.eventID, getattr(callerClass,ls[0]), ls[1])
            else:
                self.callback(self.eventID, getattr(callerClass, ls[0]))

    def getEventID(self, eventName):
        """a methode to get an eventID from viz."""

        return self.dictOfEvents.setdefault(eventName,viz.getEventID(eventName))



class JasonEventSender(object):
    def __init__(self):
        """
        This class sends JassonEvents to viz and must be started via viz.director()

        @param jEventsToSend: is a dict. where key = eventID and value = is a list.
            The list contains jEventObj.
        @type jEventsToSend: dict.

        @param shouldIRun: tells the JasonEventSender Obj to keep running or not
        @type shouldIRun: bool

        @param lock: a Lock obj for synchronisation purposes
        @type lock: threading.Lock
        """

        self.jEventsToSend = {}
        self.shouldIRun = True
        self.lock = threading.Lock()

    def resetMovements(self):
        """This resets the Sender dict., if we want to stop posting jEvents."""

        with self.lock:
            self.jEventsToSend = {}

    def setJEventsObjToSend(self,dicti):
        """replaces the old one"""

        with self.lock:
                self.jEventsToSend = dicti

    def run(self):
        """
        start posting jEvents.
            1. Check if we good to go. If not look at E{5}.
            2. iterate throu the jEventsToSend
            3. iterate throu the value list from jEventsToSend
            4. post the jEvent with the eventID from step E{2} and the jEventObj from step E{3}
            5. clear the jEventsToSend dict. and stop running.
        """

        self.shouldIRun = True #: mabye the JasonEventSender has stopt sending before, but we want to run it again
        while True:
            with self.lock:
                if self.shouldIRun:
                    for eventID,jEventObjList in self.jEventsToSend.iteritems():
                        for jEventObj in jEventObjList:
                           self.postJEvent(eventID,jEventObj)
                else:
                    self.jEventsToSend.clear()
                    break

            viz.waitFrame(1)

    def stop(self):
        """stop to send jEvents"""

        with self.lock:
            self.shouldIRun = False

    def postJEvent(self,eventID,jEObj):
        """
        This command allows us to send events to the running viz from different threads.
        The event is saved in a list, which the viz thread processes at the beginning of every frame.
        Callback's which are registered to the specific event, will be notified and the jEObj will be passed on to them
        """

        viz.postEvent(eventID,jEObj)




class JassonCam():

    MOVE_SPEED = 3.0
    TURN_SPEED = 50.0
    """constant definitions"""

    def __init__(self,jasonEventRegister,view=None,forward='w',backward='s',left='q',right='e',up='r',down='f',turnRight='d',turnLeft='a',pitchDown='h',pitchUp='y',rollRight='j',rollLeft='g',moveMode=viz.REL_PARENT,moveScale=1.0,turnScale=1.0):
        """This Class will interpret the JasonEvents to CamaraMovments"""

        self.myHandler = jasonEventRegister #: needed for Registering

        if view == None:
            self.view = viz.MainView
        else:
            self.view = view #: if the view is diffrent than viz.MainView

        self.myHandler.registerCallback(self,JASON_KEYDOWN_EVENT=["onJassonKeyDown"],UPDATE_EVENT=["onCamUpdate"],VIEW_CHANGED_EVENT=["onViewChanged"]) #: Register funkt with Events

        self.moveScale = self.MOVE_SPEED * moveScale #: the actual Movement speed
        self.turnScale = self.TURN_SPEED * turnScale #: the actual turn speed

        self.moveMode = moveMode #: Translation mode

        self.moveSet = set() #: these are the movments that must be realised

        self.helperDict = {} #: helper dict for getting the keys into the moveSet

        self.typOfMovment = {} #: consist movements for each type
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

    def __fillHelperDictWithSets(self, key, vizDataObj):
        self.helperDict.setdefault(key,set()).add(vizDataObj)


    def onJassonKeyDown(self, jE):
        """
        the helperDict looks like this.{ "w" : set(viz.Data(index=2,sign=1,move=True)), "s" : set(viz.Data(index=2,sign=-1,move=True)), ....}.
        1.The methode takes the jE.key as the Key for the helperDict
        2.Now we get the Value form the helperDict, which is a set that contains only one viz.Data obj.
        3.Then it adds the set from E{2} to the moveSet
        """

        self.moveSet.update(self.helperDict[jE.key])

    def onCamUpdate(self, e):
        """
        This funk. will be executed every new Frame. Since the UpdateEvent is triggered by Viz.

        1.Iterate through the moveSet, to look which movements must be realised
        2.updates the blank Vector with the information contained in the viz.Data Obj
        3.executes the viz funk. .setAxisAngle() and .setPosition() to change the Position and Angle of the view

        """

        if self.moveSet:
            move = [0, 0, 0] #: a blank Vector [x,z,y]
            for k in self.moveSet:
                if k.move:
                    move[k.index] += k.sign * e.elapsed * self.moveScale
                else:
                    self.view.setAxisAngle(k.axis[0],k.axis[1],k.axis[2],e.elapsed * self.turnScale,viz.HEAD_ORI,k.mode)
            self.view.setPosition(move,self.moveMode)
            self.moveSet.clear()


    def onViewChanged(self,newView):
        self.view = newView