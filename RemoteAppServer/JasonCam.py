__author__ = 'MrLapTop'
import viz
from JasonEventModule import JasonEventHandler

"""our Cam that will interpret the JasonEvents to CamaraMovments"""
class JassonCam():
    #constant definitions
    MOVE_SPEED = 3.0
    TURN_SPEED = 90.0

    def __init__(self,jasonEventHandler,forward='w',backward='s',left='q',right='e',up='r',down='f',turnRight='d',turnLeft='a',pitchDown='h',pitchUp='y',rollRight='j',rollLeft='g',moveMode=viz.REL_LOCAL,moveScale=1.0,turnScale=1.0):
        self.myHandler = jasonEventHandler

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