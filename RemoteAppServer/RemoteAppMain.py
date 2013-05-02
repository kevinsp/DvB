__author__ = 'MrLapTop'
import viz
from JasonEventHandler import JasonEventHandler
from JasonCam import JassonCam
from TestClassEmulateJEvents import EmulateJEvents

if __name__ == "__main__":
    jEventHandler = JasonEventHandler()
    jCam = JassonCam(jEventHandler)


    jEventEmulator = EmulateJEvents({"JASON_KEYDOWN_EVENT":{"key":"w"}})

    viz.go()
    viz.addChild('piazza.osgb')
    viz.director(jEventEmulator.startJEvents,200)


