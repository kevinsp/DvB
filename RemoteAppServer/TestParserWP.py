__author__ = 'MrLapTop'
import socket
from RemoteAppMain import RemoteAppLuncher
import viz
import sys

sys.path.append(r"..\GUI")
from Checkpoint import Checkpoint

class AndroidEmu(object):

    def __init__(self,hostIp,hostPort):
        self.HOST = hostIp
        self.PORT = hostPort
        self.BUF_SIZE = 1024

    def run(self):
        c = socket.socket()           # Neuer Socket
        c.connect((self.HOST, self.PORT))       # Verbindung zum Server aufbauen

        while True:

            c.sendall(self.createRequestCreateCp()+ "\n")
            print "Client: " + c.recv(self.BUF_SIZE)

            c.sendall("{\"end\":0}\n" )
            break
        c.close()

    def createRequest(self):
        self.dictReq =  {   "wp"    : 2,
                            "name"  : "test",
                            "c"     : "test1"
                        }
        return str(self.dictReq).replace("'","\"")

    def createRequestCreateCp(self):
        self.dictReq =  {   "wp"    : 1,
                            "name"  : "test",
                            "c"     : "test1"
        }
        return str(self.dictReq).replace("'","\"")

if __name__ == "__main__":
    """
    wpListIn =  []
    wpListIn.append(Checkpoint(1,2,3,"Hans",0,0,0,"FUCK"))
    wpListIn.append(Checkpoint(1,2,3,"Peter",0,0,0,"BLA"))
    wpListIn.append(Checkpoint(1,2,3,"GUSTAV",0,0,0,"FICKMICH"))
        #{'comment': 'lmao', 'name': 'myPoint', 'eulerZ': 0, 'eulerY': 0, 'eulerX': 0, 'posZ': 2, 'posX': 1, 'posY': 3};" \
        #        "{'comment': 'coon', 'name': 'yourPoint', 'eulerZ': 0, 'eulerY': 0, 'eulerX': 0, 'posZ': 4, 'posX': 3, 'posY': 5};" \
        #        "{'comment': 'fegit', 'name': 'hisPoint', 'eulerZ': 0, 'eulerY': 0, 'eulerX': 0, 'posZ': 7, 'posX': 6, 'posY': 8}"

    remoteLuncher = RemoteAppLuncher("127.0.0.1",None,wpListIn)
    androidHandy = AndroidEmu("127.0.0.1",57891)

    viz.go()
    viz.addChild('piazza.osgb')
    viz.collision(viz.ON)

    viz.director(remoteLuncher.lunch)
    viz.director(androidHandy.run)
    """ # Für lokal test

    androidEmu = AndroidEmu("141.82.173.74",57891)
    androidEmu.run()