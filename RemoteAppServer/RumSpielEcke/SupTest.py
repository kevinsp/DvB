__author__ = 'MrLapTop'

import viz
import vizmat
import math

class KeyboardCamera():

    MOVE_SPEED = 3.0

    TURN_SPEED = 90.0

    def __init__(self,forward='w',backward='s',left='q',right='e',up='r',down='f',turnRight='d',turnLeft='a',pitchDown='h',pitchUp='y',rollRight='j',rollLeft='g',moveMode=viz.REL_LOCAL,moveScale=1.0,turnScale=1.0):

        #Camera.__init__(self)

        #Movement/turn speeds
        self.moveScale = self.MOVE_SPEED * moveScale
        self.turnScale = self.TURN_SPEED * turnScale

        #Translation mode
        self.moveMode = moveMode

        #Maps a key to a set of movements
        self.keys = {}

        #Set of movements that are currently down
        self.downKeys = set()

        #Maps a name to movement
        self.keyNames = {}

        #Create movements for each key
        self.keyNames['forward'] = viz.Data(key=forward,index=2,sign=1,move=True)
        self.keyNames['backward'] = viz.Data(key=backward,index=2,sign=-1,move=True)
        self.keyNames['left'] = viz.Data(key=left,index=0,sign=-1,move=True)
        self.keyNames['right'] = viz.Data(key=right,index=0,sign=1,move=True)
        self.keyNames['up'] = viz.Data(key=up,index=1,sign=1,move=True)
        self.keyNames['down'] = viz.Data(key=down,index=1,sign=-1,move=True)
        self.keyNames['turnRight'] = viz.Data(key=turnRight,axis=[0,1,0],mode=viz.REL_LOCAL,move=False)
        self.keyNames['turnLeft'] = viz.Data(key=turnLeft,axis=[0,-1,0],mode=viz.REL_LOCAL,move=False)
        self.keyNames['pitchDown'] = viz.Data(key=pitchDown,axis=[1,0,0],mode=viz.REL_LOCAL,move=False)
        self.keyNames['pitchUp'] = viz.Data(key=pitchUp,axis=[-1,0,0],mode=viz.REL_LOCAL,move=False)
        self.keyNames['rollRight'] = viz.Data(key=rollRight,axis=[0,0,-1],mode=viz.REL_LOCAL,move=False)
        self.keyNames['rollLeft'] = viz.Data(key=rollLeft,axis=[0,0,1],mode=viz.REL_LOCAL,move=False)

        #Save movements in keys set
        for k in self.keyNames.itervalues():
            print "%s : %s" % (k,k.key)


blub = KeyboardCamera()