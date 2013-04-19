
__author__ = 'MrLapTop'
import socket
import traceback

class Serversocket():

    def __init__(self,hostip,backlog=1,port=10070,buff_size=1024):
        self.HOSTIP = hostip
        self.PORT = port
        self.BUFF_SIZE = buff_size
        self.BACKLOG = backlog
        self.socket = None

    def open_socket(self):
        try:
            self.socket = socket.socket()
            self.socket.bind((self.HOSTIP, self.PORT))
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.listen(self.BACKLOG)
        except socket.error:
            if self.socket:
                self.socket.close()
            # Exception Handeling missing
            print ("Cant open Socked")

    def run_server(self):
        self.open_socket()

        while True:
            try:
                client = self.socket.accept()
            except Exception:
                #Exception Handeling missing
                print ("Something Went wrong with accepting a Client")
                continue
