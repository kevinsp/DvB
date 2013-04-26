__author__ = 'MrLapTop'
import viz

class JassonCam():
    MOVE_SPEED = 3.0
    TURN_SPEED = 90.0

    def __init__(self,moveMode=viz.REL_LOCAL,moveScale=1.0,turnScale=1.0):

        #Movement/turn speeds
        self.moveScale = self.MOVE_SPEED * moveScale
        self.turnScale = self.TURN_SPEED * turnScale
        #Translation mode
        self.moveMode = moveMode


        self.typOfMovment = {}

        #Create movements for each typ
        self.typOfMovment['forward'] = viz.Data(index=2,sign=1,move=True)
        self.typOfMovment['backward'] = viz.Data(index=2,sign=-1,move=True)
        self.typOfMovment['left'] = viz.Data(index=0,sign=-1,move=True)
        self.typOfMovment['right'] = viz.Data(index=0,sign=1,move=True)
        self.typOfMovment['up'] = viz.Data(index=1,sign=1,move=True)
        self.typOfMovment['down'] = viz.Data(index=1,sign=-1,move=True)
        self.typOfMovment['turnRight'] = viz.Data(axis=[0,1,0],mode=viz.REL_LOCAL,move=False)
        self.typOfMovment['turnLeft'] = viz.Data(axis=[0,-1,0],mode=viz.REL_LOCAL,move=False)
        self.typOfMovment['pitchDown'] = viz.Data(axis=[1,0,0],mode=viz.REL_LOCAL,move=False)
        self.typOfMovment['pitchUp'] = viz.Data(axis=[-1,0,0],mode=viz.REL_LOCAL,move=False)
        self.typOfMovment['rollRight'] = viz.Data(axis=[0,0,-1],mode=viz.REL_LOCAL,move=False)
        self.typOfMovment['rollLeft'] = viz.Data(axis=[0,0,1],mode=viz.REL_LOCAL,move=False)


    def onJassonKeyDown(self,jE):
        pass

    def onCamUpdate(self,e):
        pass