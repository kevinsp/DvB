
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
        self.connector = connector

    def open_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.socket = socket.socket()
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.HOSTIP, self.PORT))
            self.socket.listen(self.BACKLOG)

        except socket.error:
            if self.socket:
                self.socket.close()
            # Exception Handeling missing
            traceback.print_exc()
            print ("Cant open Socked, try it again in a few seconds")
            return -1
        return 1


    def run_server(self):
        if self.open_socket() == -1:
            return

        while True:
            try:
                    print "Server is Running"
                    connection, client = self.socket.accept()
                    print "connection established"
                    #connection.settimeout(5)

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

                if self.connector.feedData(data) == "end":
                    print "connection was interuppted by user"
                    break

            except socket.timeout:
                    print "connection timeout"
                    break

            except Exception:
                print "cant recive data"
                traceback.print_exc()
                continue

        self.connector.connectionInteruppted()
        #self.connector.shutdown(socket.SHUT_RDWR)
        connection.close()

