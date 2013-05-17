import socket
import sys
import json

class MyServer(object):

    def __init__(self):
        # Create a TCP/IP socket
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = socket.socket()

    def run(self):
        # Bind the socket to the port
        server_address = ('141.82.169.30', 57891)
        print >>sys.stderr, 'starting up on %s port %s' % server_address
        self.sock.bind(server_address)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Listen for incoming connections
        self.sock.listen(1)

        while True:
            # Wait for a connection
            print >>sys.stderr, 'waiting for a connection'
            connection, client_address = self.sock.accept()
            # Listen for incoming connections

            try:
                print >>sys.stderr, 'connection from', client_address

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(1024)
                    print >>sys.stderr, 'received "%s"' % data      # to be removed, too
                    if data:
                        print >>sys.stderr, 'handing to parser'
                        if self.parseMovement(data) == "end":
                            break
                    else:
                        print >>sys.stderr, 'no more data from', client_address
                        # might wanna remove this soon, cause spam city while idle

            finally:
                # Clean up the connection
                connection.close()

    def parseMovement(self, jpacket):
        print "..parse here"
        jloadout = json.loads(jpacket)

        # Special cases such as 'Checkpoint' that need own parsing/treatment
        if jloadout.has_key("end"):
            return "end"
        elif jloadout.has_key("cp"):
            return "cp"
        elif jloadout.has_key("nt"):
            return "nt"

        move = jloadout["m"]
        rotate = jloadout["r"]
        elev = jloadout["e"]

        #not sure yet where to put
        self.jsonToMoveKey(move)
        self.jsonToRotKey(rotate)
        if elev == 0:
            pass
        elif elev == 1:
            pass
            #JEventOjbect("r")
        elif elev == -1:
            pass
            #JEventObject("f")


    def jsonToMoveKey(self, move):
        if move["a"] == 0:
            if move["b"] == 0: # no movement
                pass  # hmmmmmm idk idk. Notify to stop looping?
            elif move["b"] == 1: # forward
                pass
                #JEventObj("w")
            elif move["b"] == -1: # backwards
                pass
                #JEventObj("s")
        elif move["a"] == 1:
            if move["b"] == 0: # right
                pass
                #JEventObj("d")
            elif move["b"] == 1: # upper right
                pass
                #JEventObj("w")
                #JEventObj("q")
            elif move["b"] == -1: # lower right
                pass
                #JEventObj("s")
                #JEventObj("q")
        elif move["a"] == -1:
            if move["b"] == 0: # left
                pass
                #JEventObj("a")
            elif move["b"] == 1: # upper left
                pass
                #JEventObj("w")
                #JEventObj("e")
            elif move["b"] == -1: # lower left
                pass
                #JEventObj("s")
                #JEventObj("e")

    def jsonToRotKey(self, rotate):
        if rotate["x"] == 0:
            if rotate["y"] == 0: # no rotation
                pass
            elif rotate["y"] == 1: # turnRight
                pass
                #JEventObj("d")
            elif rotate["y"] == -1: # turnLeft
                pass
                #JEventObj("a")
        elif rotate["x"] == 1:
            if rotate["y"] == 0: # pitchUp
                pass
                #JEventObj("v")
            elif rotate["y"] == 1: # upper right
                pass
                #JEventObj("v")
                #JEventObj("d")
            elif rotate["y"] == -1: # upper left
                pass
                #JEventObj("v")
                #JEventObj("a")
        elif rotate["x"] == -1:
            if rotate["y"] == 0: # pitchDown
                pass
                #JEventObj("c")
            elif rotate["y"] == 1: # lower right
                pass
                #JEventObj("c")
                #JEventObj("d")
            elif rotate["y"] == -1: # lower left
                pass
                #JEventObj("c")
                #JEventObj("a")


if __name__ == "__main__":
    server = MyServer()
    server.run()