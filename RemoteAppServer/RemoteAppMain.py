__author__ = 'MrLapTop'
import viz

from TestClassEmulateJEvents import EmulateJEvents
import sys

from JasonEventModule import JassonCam
from JasonEventModule import JasonEventRegister
from JasonEventModule import JasonEventSender
from ServerSocket import Serversocket
from Parser import Parser
from Connector import Connector
from server import MyServer

#sys.path.append(r"..\GUI")





"""insert new ip and go"""

class RemoteAppLuncher(object):
    def __init__(self,HostIp,view=None,checkPointList = None):
        self.jEventRegister = JasonEventRegister()
        self.jCam = JassonCam(self.jEventRegister,view) #
        self.jParser = Parser(self.jEventRegister,checkPointList)
        self.connector = Connector(self.jParser)
        self.sSocket = Serversocket(str(HostIp),self.connector)

    def lunch(self):
        self.sSocket.run_server()





if __name__ == "__main__":
    jEventRegister = JasonEventRegister()
    jCam = JassonCam(jEventRegister)
    jParser = Parser(jEventRegister)
    connector = Connector(jParser)
    sSocket = Serversocket("141.82.163.203",connector)




    #jEventEmulator1 = EmulateJEvents(jEventRegister,{"JASON_KEYDOWN_EVENT":[{"key":"w"},{"key":"a"},{"key":"s"},{"key":"d"}]})
    #jEventEmulator2 = EmulateJEvents(jEventHandler,{"JASON_KEYDOWN_EVENT":{"key":"w"}})

    viz.go()
    viz.addChild('piazza.osgb')
    viz.collision(viz.ON)
    #vizcam.KeyboardCamera()
    viz.director(sSocket.run_server)
    #viz.director(jEventEmulator2.startJEvents,1)



