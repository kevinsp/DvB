__author__ = 'MrLapTop'
import viz

from TestClassEmulateJEvents import EmulateJEvents
import thread
from JasonEventModule import JassonCam
from JasonEventModule import JasonEventRegister
from JasonEventModule import JasonEventSender

if __name__ == "__main__":
    jEventRegister = JasonEventRegister()
    jCam = JassonCam(jEventRegister)
    jEvSen = JasonEventSender()

    #jEventEmulator1 = EmulateJEvents(jEventRegister,{"JASON_KEYDOWN_EVENT":[{"key":"w"},{"key":"a"},{"key":"s"},{"key":"d"}]})
    #jEventEmulator2 = EmulateJEvents(jEventHandler,{"JASON_KEYDOWN_EVENT":{"key":"w"}})

    viz.go()
    viz.addChild('piazza.osgb')
    #vizcam.KeyboardCamera()
    viz.director(jEvSen.run)
    #viz.director(jEventEmulator2.startJEvents,1)



