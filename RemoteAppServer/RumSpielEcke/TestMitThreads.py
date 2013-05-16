__author__ = 'MrLapTop'

import viz
from SubThread import SubThread
import vizcam
import random


class MainThread():
    def __init__(self):
        viz.go()
        vizcam.AUTO_REGISTER = 0

        self.court = viz.addChild('piazza.osgb')

    def stopThread(self,thread):
        viz.waitTime(10)
        thread.stop()
        return

    def manageThread(self,thread):
        lsAll =[["a","b","c"],[1,2,3],[4,5,6],[]]
        for ls in lsAll:
            thread.changeData(ls)
            viz.waitTime(5)
        thread.stop()



if __name__ == "__main__":
    wtf = MainThread()
    subThread = SubThread()


    viz.director(subThread.run)
    viz.director(wtf.manageThread,subThread)


