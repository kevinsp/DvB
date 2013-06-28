import viz
from JasonEventModule import JEventObj
from JasonEventModule import JasonEventSender
import json
import traceback
import sys
sys.path.append(r"..\Release1.0\GUI")
from CheckpointFunktionen import createCheckpointAndroid
from CheckpointFunktionen import deleteCheckpointAndroid
from CheckpointFunktionen import porteCheckpointAndroid

###
# Parser takes a String representation of the sent JSONObject to collect and forward the
# data in a processable form.
#
# Incoming data currently diveded into 3 sections, being
# 'move'[a,b]
# 'rotate'[x,y]
# 'elevate'[d]
# all represented by either 0,-1,1 in each parameter.
###

class Parser(object):

    def __init__(self, jasonEventRegister,wayPointList):
        self.jEventReg = jasonEventRegister
        self.sender = JasonEventSender()
        viz.director(self.sender.run)
        self.mreDict = self.createDicti()
        self.wayPointList = wayPointList
        self.msgEndTag = "(\"(/^_^\)\")"


    # Method gets the data 'jpacket' for further use
    def prepareForParsing(self,data,connectionIterupted=False):

        if connectionIterupted:
            self.sender.resetMovements()
            return ""

        self.jsonObjList = data.split("\n")[:-1]

        self.returnMSG = ""
        for jsonObj in self.jsonObjList:

            self.returnMSG = self.parseOneJson(jsonObj)
        return self.returnMSG


    def parseOneJson(self, jpacket):

        try:
            self.jloadout = json.loads(jpacket)
        except ValueError:
            print "json OBJ could not be loaded"
            self.sender.resetMovements()
            return "" #return value "" signels that there is nothing to be send back to the client

        # Special cases such as 'Waypoint' that need own parsing/treatment
        if self.jloadout.has_key("end"):
            #moeglichkeit zum performance test
            return "end"
        elif self.jloadout.has_key("wp"):
            return self.parseWaypoint(self.jloadout)

        # Create a list for the keys for the JEvent (3 spots)
        # Strip out paramters from each section and parse out
        # necessary keystroke depending on pattern (getKey() method)

        self.keyToSend = []
        self.move = self.jloadout["m"]
        self.moveKey = self.getKey("m",self.move["a"],self.move["b"])
        self.keyToSend.append(self.moveKey)

        self.rotate = self.jloadout["r"]
        self.rotateKey = self.getKey("r",self.rotate["x"],self.rotate["y"])
        self.keyToSend.append(self.rotateKey)

        self.elev = self.jloadout["e"]
        self.elevKey = self.getKey("e",self.elev)
        self.keyToSend.append(self.elevKey)

        # Should the JSONObj be 'all zero' aka no action, just return

        if self.moveKey == None and self.rotateKey == None and self.elevKey == None:
            self.sender.resetMovements()
            return ""

            # Push tailored dictionary to next class for posting needed Event

        self.sender.setJEventsObjToSend(self.makeJEventDict())
        return ""

    def parseWaypoint(self, jwaypoint):

        self.wpValue = jwaypoint["wp"]
        # 1 -> porten
        if self.wpValue == 1:
            print "Server: Beam me Up"
            porteCheckpointAndroid(jwaypoint["id"])
            return ["wp;",self.msgEndTag]
        # 0 -> delete a cp
        elif self.wpValue == 0:    #<- Zero if Delte existing, 1 if create new one
            deleteCheckpointAndroid(jwaypoint["id"])
        # 2 -> just send the cp back
        elif self.wpValue == 2:
            pass
        # 3 -> create a cp
        elif self.wpValue == 3:
            print "Server : Cp Successfully created"
            createCheckpointAndroid(jwaypoint["name"], jwaypoint["c"]) #<- crtWp(name, comment)


        wpListStringed =["wp;"]

        for cpId,wp in enumerate(self.wayPointList):
            wp.__dict__["id"] = cpId
            wpListStringed.append( str(wp.__dict__) + ";")

        wpListStringed.append(self.msgEndTag)

        return wpListStringed


    # Method will prepare a dictionary of certain syntax
    # matching what the following classes need for triggering
    # the correkt events.

    def makeJEventDict(self):
        self.jEventDict = {}
        self.eventID = self.jEventReg.getEventID("JASON_KEYDOWN_EVENT")
        self.jEventDict[self.eventID] = []

        for key in self.keyToSend:
            if key:
                if isinstance(key, list):
                    for element in key:
                        self.jEventDict[self.eventID].append(JEventObj({"key": str(element)}))
                else:
                    self.jEventDict[self.eventID].append(JEventObj({"key": str(key)}))
        return self.jEventDict


    def getKey(self, typeArg, firstArg, secondArg=None):
        if (secondArg != None):
            return self.mreDict[typeArg][(firstArg, secondArg)]
        else:
            return self.mreDict[typeArg][firstArg]


    def pShutdown(self):
        self.sender.stop()
        self.jEventDict = None
        self.sender = None
        self.mreDict= None

    # Set of all possible permutations and matching keys.

    def createDicti(self):
        self.dicti = {
            "m" :
                {
                    (0,1): "w",
                    (0,-1) : "s",
                    (1,0) : "e",
                    (-1,0) : "q",

                    (1,1): ["w","e"],
                    (1,-1) : ["s","e"],
                    (-1,1) : ["w","q"],
                    (-1,-1) : ["s","q"],
                    (0,0) : None
                },
            "r" :
                {
                    (0,1): "d",
                    (0,-1) : "a",
                    (1,0) : "h",
                    (-1,0) : "y",

                    (1,1): ["h","d"],
                    (1,-1) : ["h","a"],
                    (-1,1) : ["y","d"],
                    (-1,-1) : ["y","a"],
                    (0,0) : None
                },
            "e" :
                {
                    0 : None,
                    1 : "r",
                    -1 : "f"
                }
        }
        return self.dicti