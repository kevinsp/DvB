
__author__ = 'MrLapTop'
import socket
import viz
import traceback

class Serversocket(object):

    def __init__(self,hostip,connector,backlog=1,port=57891,buff_size=1024):
        self.HOSTIP = hostip
        self.PORT = port
        self.BUFF_SIZE = buff_size
        self.BACKLOG = backlog
        self.socket = None
        #self.connector = connector

    def open_socket(self):
        try:
            #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = socket.socket()
            self.socket.settimeout(5)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.HOSTIP, self.PORT))
            self.socket.listen(self.BACKLOG)

        except socket.error:
            if self.socket:
                self.socket.close()
                # Exception Handeling missing
            print ("Cant open Socked")



    def run_server(self):
        self.open_socket()

        try:
            print "Server is Running"
            connection, client = self.socket.accept()
            print "connection established"
            self.listenToClient(connection,client)

        except Exception:
            #Exception Handeling missing
            traceback.print_exc()
            print ("Something Went wrong with accepting a Client")



    def listenToClient(self,connection,client):
        while True:
            try:
                data = connection.recv(self.BUFF_SIZE)

                print ("Data: % s" % data)

                if not data:
                    print "connection is interuppted"
                    break

                if self.connector.feedData(data) == "end":
                    print "connection is interuppted by user"
                    break

            except Exception:
                print "cant recive data"
                traceback.print_exc()
                continue
        self.connector.connectionInteruppted()
        #self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

        viz.director(self.run_server())