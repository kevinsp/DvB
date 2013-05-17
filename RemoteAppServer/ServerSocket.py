
__author__ = 'MrLapTop'
import socket
import Connector

class Serversocket(object):

    def __init__(self,hostip,connector,backlog=1,port=57891,buff_size=1024):
        self.HOSTIP = hostip
        self.PORT = port
        self.BUFF_SIZE = buff_size
        self.BACKLOG = backlog
        self.socket = None
        self.connector = connector

    def open_socket(self):
        try:
            print "1"
            #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = socket.socket()
            print "2"
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print "3"
            self.socket.bind((self.HOSTIP, self.PORT))
            print "4"

            self.socket.listen(self.BACKLOG)

        except socket.error:
            if self.socket:
                self.socket.close()
            # Exception Handeling missing
            print ("Cant open Socked")

    def run_server(self):
        self.open_socket()

        while True:
            print "Server is Running"
            try:
                 connection, client = self.socket.accept()

                 data = connection.recv(self.BUFF_SIZE)

                 print ("Data: % s" % data)
                 if data:
                     if self.connector.feedData(data) == "end":
                         connection.close()
                         break
            except Exception:
                #Exception Handeling missing
                print ("Something Went wrong with accepting a Client")
                continue
