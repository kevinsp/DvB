
import viz
from JasonEventModule import JEventObj
from JasonEventModule import JasonEventSender
import json

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

    def __init__(self, jasonEventRegister):
        self.jEventReg = jasonEventRegister
        self.sender = JasonEventSender()
        viz.director(self.sender.run)
        self.mreDict = self.createDicti()

            #    Method gets the data 'jpacket' for further use
    def parseJson(self, jpacket):
        jloadout = json.loads(jpacket)

            #   Special cases such as 'Checkpoint' that need own parsing/treatment
        if jloadout.has_key("end"):
            return "end"
        elif jloadout.has_key("cp"):
            return "cp"
        elif jloadout.has_key("nt"):
            return "nt"

            #   Create a list for the keys for the JEvent (3 spots)
            #   Strip out paramters from each section and parse out
            #   necessary keystroke depending on pattern (getKey() method)

        self.keyToSend = []
        self.move = jloadout["m"]
        self.moveKey = self.getKey("m",self.move["a"],self.move["b"])
        self.keyToSend.append(self.moveKey)

        self.rotate = jloadout["r"]
        self.rotateKey = self.getKey("r",self.rotate["x"],self.rotate["y"])
        self.keyToSend.append(self.rotateKey)

        self.elev = jloadout["e"]
        self.elevKey = self.getKey("e",self.elev)
        self.keyToSend.append(self.elevKey)

            #   Should the JSONObj be 'all zero' aka no action, just return

        if self.moveKey == None and self.rotateKey == None and self.elevKey == None:
            return

            #   Push tailored dictionary to next class for posting needed Event

        self.sender.setJEventsObjToSend(self.makeJEventDict())


            #   Method will prepare a dictionary of certain syntax
            #   matching what the following classes need for triggering
            #   the correkt events.

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


            #   Set of all possible permutations and matching keys

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