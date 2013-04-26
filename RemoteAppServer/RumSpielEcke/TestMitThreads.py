__author__ = 'MrLapTop'

import viz
from EigenerCamHandlerEx import MyCameraHandler
import vizact
import vizcam

class MainThread():
    def __init__(self):
        viz.go()
        vizcam.AUTO_REGISTER = 0
        viz.cam.setHandler(None)
        self.court = viz.addChild('piazza.osgb')
        man = vizcam.Manager(viz.MainView,vizcam.KeyboardCamera)
        viz.callback(viz.KEYDOWN_EVENT,self.printMe)

        #self.losGehts()
        viz.director(self.losGehts)

    def printMe(self,obj):

        print obj


    def losGehts(self):

        while(True):

            viz.waitFrame(200)
            viz.logNotice("Bin in Schleife")
            #pre = viz.Event(key="ME")
            viz.postEvent(viz.KEYDOWN_EVENT,key='w')


if __name__ == "__main__":
    wtf = MainThread()


