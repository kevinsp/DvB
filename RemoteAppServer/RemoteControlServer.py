# Copyright 2010 Christian Zommerfelds
# 
# This file is part of RemoteControl for Android.
# 
# RemoteControl for Android is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# RemoteControl for Android is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with RemoteControl for Android.
# If not, see <http://www.gnu.org/licenses/>.

import socket

class ButtonsDefinition(object):
    def __init__(self):
        self.__buttons = {}
        self.__curIndex = 0
        
    def addButton(self, label, func):
        if label == '':
            print('ERROR: addButton(...) name must not be empty')
            return
        self.__buttons[self.__curIndex] = (label, func)
        self.__curIndex += 1
        
    def runFunc(self, num):
        if num in self.__buttons:
            self.__buttons[num][1]()
            
    def getLabel(self, num):
        if num in self.__buttons:
            return self.__buttons[num][0]
        return ''

class Server(object):
    def __init__(self, butDef, verbose=False):
        self._butDef = butDef
        self._verbose = verbose
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self._PORT))
        s.listen(1)
        while True:
            self._write('Waiting for connection, port:', self._PORT)
            conn, addr = s.accept()
            self._write('Connecting with', addr)
            
            data = conn.recv(len(self._HANDSHAKE_IN))
            if not self._HANDSHAKE_IN == data:
            	self._write('Refusing connection: wrong handshake')
            	conn.close()
            	continue
            	
            conn.sendall(self._HANDSHAKE_OUT)
            
            self._write('Sending button labels')
            i = 0
            while True:
                name = self._butDef.getLabel(i)
                if name == '':
                    break
                conn.sendall((name+'\n').encode('UTF-8'))
                i += 1
            conn.sendall(b'\n')
            
            while True:
                data = conn.recv(self._PACKET_SIZE)
                if not data: break
                butnum = ord(data)
                but = self._butDef.getLabel(butnum)
                self._write('Received button press '+str(butnum)+': "'+str(but)+'"')
                self._butDef.runFunc(ord(data))
            conn.close()
            
    def _write(self, *objs):
        if (self._verbose):
            self.stri = ""
            stri += "RemoteControlServer> "



          """print ('RemoteControlServer> ',end='')
            for obj in objs:
                print(obj,sep='',end='')
            print()""" #<- orginal code

    _PORT = 57891
    _PACKET_SIZE = 1
    _HANDSHAKE_OUT = b"remote-control handshake server\n"
    _HANDSHAKE_IN = b"remote-control handshake client\n"
