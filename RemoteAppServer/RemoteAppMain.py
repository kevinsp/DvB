__author__ = 'MrLapTop'
import viz
from JasonEventHandler import JasonEventHandler
from JasonCam import JassonCam
from TestClassEmulateJEvents import EmulateJEvents

if __name__ == "__main__":
    jCam = JassonCam()
    jEHandler = JasonEventHandler(jCam,JASON_KEYDOWN_EVENT=["onJassonKeyDown"])

    jEventEmulator = EmulateJEvents({"JASON_KEYDOWN_EVENT":{"blub":"Cool"}})

    viz.go()
    viz.addChild('piazza.osgb')
    viz.director(jEventEmulator.startJEvents,200)


