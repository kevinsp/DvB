__author__ = 'MrLapTop'
import viz

from TestClassEmulateJEvents import EmulateJEvents
import thread
from JasonEventModule import JassonCam
from JasonEventModule import JasonEventRegister
from JasonEventModule import JasonEventSender
from ServerSocket import Serversocket
from Parser import Parser
from Connector import Connector
from server import MyServer

"""insert new ip and go"""

if __name__ == "__main__":
    jEventRegister = JasonEventRegister()
    jCam = JassonCam(jEventRegister)
    jParser = Parser(jEventRegister)
    connector = Connector(jParser)
    sSocket = Serversocket("141.82.166.185",connector)




    #jEventEmulator1 = EmulateJEvents(jEventRegister,{"JASON_KEYDOWN_EVENT":[{"key":"w"},{"key":"a"},{"key":"s"},{"key":"d"}]})
    #jEventEmulator2 = EmulateJEvents(jEventHandler,{"JASON_KEYDOWN_EVENT":{"key":"w"}})

    viz.go()
    viz.addChild('piazza.osgb')
    viz.collision(viz.ON)
    #vizcam.KeyboardCamera()
    viz.director(sSocket.run_server)
    #viz.director(jEventEmulator2.startJEvents,1)



