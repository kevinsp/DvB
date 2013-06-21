__author__ = 'MrLapTop'
import socket
from RemoteAppMain import RemoteAppLuncher
import viz
import sys
import pprint
sys.path.append(r"..\GUI")
from Checkpoint import Checkpoint

import doctest
class AndroidEmu(object):

    def __init__(self,hostIp,hostPort):
        self.HOST = hostIp
        self.PORT = hostPort
        self.BUF_SIZE = 1024

    def run(self,loop,wpNumm,name,commentar,id=None):
        c = socket.socket()           # Neuer Socket
        c.connect((self.HOST, self.PORT))       # Verbindung zum Server aufbauen
        counter = 0
        printString = ""
        while counter < loop:

            c.sendall(self.createRequest(wpNumm,name,commentar,id)+ "\n")

            while True:
                ans = c.recv(self.BUF_SIZE)
                printString += ans

                if self.containsEnd(ans):
                    break


            counter += 1

        print(printString)
        print(len(printString.split(";"))-2)

        c.sendall("{\"end\":0}\n" )
        c.close()

        return [printString,len(printString.split(";"))-2]

    def containsEnd(self,ans):
        if ans.__contains__("(\"(/^_^\)\")"):
            return True
        else:
            return False

    def createRequest(self,wpNumm,name,comment,id):
        if id == None:
            dictReq = {"wp" : wpNumm , "name" : str(name), "c" : str(comment)}
        else:
            dictReq = {"wp" : wpNumm , "id" : id, "c" : str(comment)}
        return str(dictReq).replace("'","\"")


if __name__ == "__main__":

    """
    testing the communication for handling Cp
    wp -> is a Number between 0-3
            0 delete cp
            1 port to cp
            2 request
            3 create cp
    name -> name/id for cp
    comment -> comment for cp

        prepare for Testing
    >>>androidEmu = AndroidEmu("141.82.163.248",57891)

        request the cp list from the server
    >>>ans,anz=androidEmu.run(1,2,"n","n")
    >>>print (ans)
    >>>anz == 0
    True

        create a checkpoint
    >>>ans,anz=androidEmu.run(1,3,"cpByA1","This is a Comment")
    >>>print (ans)
    >>>anz == 1
    True

    #port to checkpoint
    >>>ans,anz=androidEmu.run(1,1,"0","n")
    >>>print (ans)
    >>>ans == ""
    True
    >>>anz == 1
    True

    #delete checkpoint
    >>>ans,anz=androidEmu.run(1,0,"0","n")
    >>>print (ans)
    >>>anz == 0
    True

    """
    #doctest.testmod()

    androidEmu = AndroidEmu("141.82.165.194",57891)

    """request the cp list from the server"""
    #ans,anz=androidEmu.run(1,2,"n","n")

    """create a checkpoint"""
    #ans,anz=androidEmu.run(1,3,"cpByA1","This is a Comment")

    """port to checkpoint"""
    #ans,anz=androidEmu.run(1,1,None,"n",0)

    """delete checkpoint"""
    ans,anz=androidEmu.run(1,0,"0","n",0)