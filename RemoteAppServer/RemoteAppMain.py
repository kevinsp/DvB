__author__ = 'MrLapTop'
import viz
from JasonEventHandler import JasonEventHandler
from JasonCam import JassonCam
from TestClassEmulateJEvents import EmulateJEvents
import vizact

if __name__ == "__main__":
    jEventHandler = JasonEventHandler()
    jCam = JassonCam(jEventHandler)


    jEventEmulator1 = EmulateJEvents(jEventHandler,{"JASON_KEYDOWN_EVENT":[{"key":"w"},{"key":"a"},{"key":"s"},{"key":"d"}]})
    #jEventEmulator2 = EmulateJEvents(jEventHandler,{"JASON_KEYDOWN_EVENT":{"key":"w"}})

    viz.go()
    viz.addChild('piazza.osgb')
    #vizcam.KeyboardCamera()
    viz.director(jEventEmulator1.lisenToKeyboard)
    #viz.director(jEventEmulator2.startJEvents,1)



