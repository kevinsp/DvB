
__author__ = 'MrLapTop'
import socket
import viz
import traceback
import errno


class Serversocket(object):

    def __init__(self,hostip,connector,backlog=1,port=57891,buff_size=4096):
        """this class waits for an Android Handy to connect"""

        self.HOSTIP = hostip #: ip-address where this instance is running on
        self.PORT = port #: ip-port
        self.BUFF_SIZE = buff_size #: max byte size on data that we can recevie
        self.BACKLOG = backlog #: leave this at 1 so we are only lisenning to on Android Handy
        self.socket = None
        self.connector = connector
        self.shoudIRun = True #: this is the flag to switch if we want to stop the running serversocket

    def open_socket(self):
        """
        trys to open the socket.

        @return: returns -1 if it fails to open the socket
        """

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.HOSTIP, self.PORT))
            self.socket.listen(self.BACKLOG)

        except socket.error:
            if self.socket:
                self.socket.close()
            traceback.print_exc()
            print ("Server: Can't open Socked, try it again in a few seconds")
            return -1
        return 1


    def run_server(self):
        if self.open_socket() == -1:
            return

        print "Server: Server is Running"
        self.socket.setblocking(0) # now it is possible to stop this method from running
        while self.shoudIRun:
            try:

                    connection, client = self.socket.accept()

                    print "Server: connection established"

                    connection.settimeout(120)

                    self.listenToClient(connection,client)

            except socket.error, e:

                if e.args[0] == errno.EWOULDBLOCK: #exception if no connection was detected
                    print "Server: No Connection was found waiting for 5 sec"
                    viz.waittime(5)
                else:
                    print e

            except Exception:

                    traceback.print_exc()
                    print ("Server: Something Went wrong with accepting a Client")

        print "Server: Shutdown"


    def listenToClient(self,connection,client):
        errorCounter = 0
        while self.shoudIRun:
            try:
                data = connection.recv(self.BUFF_SIZE) # what happens if the recv size is bigger?

                if not data:
                    print "Server: connection interrupted"
                    break

                print ("Server: Data-> % s" % data)

                self.ans = self.connector.feedData(data) #: the return value form the connector/parser

                if self.ans == "end":
                    print "Server: connection was interrupted by user"
                    break
                elif self.ans == "":
                    #noting to send back to the App
                    pass
                else:
                    print "Server: sending back Checkpoint list"
                    helperList = list(self.chunks(self.ans,5)) # our Checkpoint List chopped into chunks

                    for partList in helperList: # sending chunk by chunk gives the App time to breath
                        connection.sendall("".join(partList)+ "\n")

            except socket.timeout:
                    print "Server: connection timeout"
                    break
            except socket.error as e:
                    if e.args[0] == errno.EWOULDBLOCK:   # no data was found
                        continue
                    else:   # maybe it was another socket.error?
                        print e
                        break
            except Exception:
                print "Server: cant recive data"
                traceback.print_exc()
                errorCounter += 1 # not the best way to do this. Try to find something else
                if errorCounter < 5:
                    continue
                else:
                    print "Server: connection cloesd after 5 errors"
                    break

        connection.shutdown(socket.SHUT_RDWR)
        connection.close()
        if self.shoudIRun: # only if we are allowed to run
            self.connector.connectionInteruppted()

    def chunks(self,myList, n):
        """ Yield successive n-sized chunks from list."""

        for i in xrange(0, len(myList), n):
            yield list[i:i+n]
