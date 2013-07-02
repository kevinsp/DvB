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
        """
        creates all nessecery files and deppendences

        @param HostIp: the ip-address where the Serversocket is running on
        @type HostIp: str

        @param view: the view/tracker will be manupilated by the jEventCam
        @type view: in our case a Tracker

        @param checkPointList: is a list overgiven list with or without checkpoints in it
        @type checkPointList: list
        """

        self.jEventRegister = JasonEventRegister()
        self.jCam = JassonCam(self.jEventRegister,view) #
        self.jParser = Parser(self.jEventRegister,checkPointList)
        self.connector = Connector(self.jParser)
        self.sSocket = Serversocket(str(HostIp),self.connector)

    def lunch(self):
        """starts the whole thing"""

        self.sSocket.run_server()

    def shutdown(self):
        """ends the whole thing"""

        self.sSocket.shoudIRun = False
        return True




if __name__ == "__main__":
    pass
    #jEventEmulator1 = EmulateJEvents(jReg,{"JASON_KEYDOWN_EVENT":[{"key":"w"},{"key":"a"},{"key":"s"},{"key":"d"}]})
