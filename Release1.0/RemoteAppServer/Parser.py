from datetime import time
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

class Parser(object):
    """
        The Parser class takes a String representation of the sent JSONObject,
        brings it's content into useable form and forwards the data
        to the responsible instances.
        Incoming data either has the movement or waypoint pattern - closer
        described in the documentation.
        Simple examples of two possiblities:
        C{ {m:{a: 0,b: 0}, r:{x: 0, y: 0}, e: 0} }
        C{ {wp: 3, name: MyWaypoint, comment: very exciting view} }
    """

    def __init__(self, jasonEventRegister,wayPointList):
        """
            Has global EventHandler and Waypointlist referenced.
            Also create mreDict, the hardcoded dictionary with
            the permutations of our movement parameters.
        """
        self.jEventReg = jasonEventRegister
        self.sender = JasonEventSender()
        viz.director(self.sender.run)
        self.mreDict = self.createDicti()
        self.wayPointList = wayPointList
        self.msgEndTag = "(\"(/^_^\)\")"
            # msgEndTag is a hardcoded String attached at message end
            # to enable detection when to stop listening for more data.


    def prepareForParsing(self,data,connectionIterupted=False):
        """
            First method to be traversed by the data from the Android App.
            Since it is very possible to receive multiple chunks of JSON data
            from the client, these will have to be seperated and parsed one by one.

            @type  data: JSONString
            @param data: Raw data sent from the Android App in JSON notation.

            @rtype:      String
            @return:     Either empty String, so Socket knows not to send anything back,
                         or 'end' / the actual stringed waypoint list.
        """
        if connectionIterupted:
            self.sender.resetMovements()
            return ""

        self.jsonObjList = data.split("\n")[:-1]

        self.returnMSG = ""
        for jsonObj in self.jsonObjList:
            self.returnMSG = self.parseOneJson(jsonObj)
        return self.returnMSG


    def parseOneJson(self, jpacket):
        """
            The parseOneJson method works with a single JSON String that needs parsing
            and will
                1. Pull the data given and put it in a dictionary 'jloadout'.
                2. Look for determined identifier signaling what data it's dealing with (waypoint, movement or end)
                3. In case
                    - 'end' return 'end" to signal ending the communication.
                    - 'wp' (waypoint) enter the waypoint parsing function that will return the full waypointlist.
                    - normal movement will strip out the parameters and assign fitting events to the eventHandler
                      and then return empty String, so the Socket just continues.

            @type  jpacket: JSONString
            @param jpacket: Single full entity of a JSON'ed comment from Android.

            @rtype:         String
            @return:        Either empty String, so Socket knows not to send anything back,
                            or 'end' / the actual stringed waypoint list.
        """
        try:
            self.jloadout = json.loads(jpacket)
        except ValueError:
            print "json OBJ could not be loaded"
            self.sender.resetMovements()
            return ""

            # Special cases such as 'Waypoint' that need own parsing/treatment
        if self.jloadout.has_key("end"):
            return "end"
        elif self.jloadout.has_key("wp"):
            return self.parseWaypoint(self.jloadout)

            # Create a list for the keys for the JEvent (3 spots)
            # Strip out paramters from each section (move, rotate, elevate) and parse out
            # necessary keystroke depending on pattern (getKey() method)

        self.keyToSend = []
            # project content of sent data to which sector they belong and
            # match with fitting tuple in mreDict to determine keystroke to send.
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

            # Push tailored dictionary to next class for posting needed Event to Vizard world

        self.sender.setJEventsObjToSend(self.makeJEventDict())
        return ""

    def parseWaypoint(self, jwaypoint):
        """
            Here the info sent for handling waypoints is analyzed for
            the required action, appropriate routine is started and
            the updated waypoint list is returned to make the list
            on Android side up to date.

            @type  jwaypoint: dict
            @param jwaypoint: Information for waypoint handling all in one dictionary.

            @rtype:           String
            @return:          fully toString'ed list of existing waypoints, seperated by semicolon
                              and tail-ended with our endTag.
        """
        self.wpValue = jwaypoint["wp"]
            # 0 -> Delete a waypoint by name.
        if self.wpValue == 0:
            deleteCheckpointAndroid(jwaypoint["id"])
            # 1 -> Set the user to the position of the where the waypoint lies.
        elif self.wpValue == 1:
            print "Server: Beam me Up"
            porteCheckpointAndroid(jwaypoint["id"])
            return ["wp;",self.msgEndTag]
            # 2 -> Just request a version of the list.
        elif self.wpValue == 2:
            pass
            # 3 -> Create a waypoint by name and comment at current position.
        elif self.wpValue == 3:
            print "Server : Cp Successfully created"
            createCheckpointAndroid(jwaypoint["name"], jwaypoint["c"])


        wpListStringed =["wp;"]

        for cpId,wp in enumerate(self.wayPointList):
            wp.__dict__["id"] = cpId
            wpListStringed.append( str(wp.__dict__) + ";")

        wpListStringed.append(self.msgEndTag)

            # return the list in the format
            # " wp;<waypoint1infoToString>;<waypoint2infoToString> "
        return wpListStringed


    def makeJEventDict(self):
        """
            Method will prepare a dictionary of certain syntax
            match what the following classed need for triggerung the correct events.

            @rtype:  dict
            @return: A dictionary containing assigned eventIDs with the matching key literal
                     so the eventHandling routine can work with it.
        """
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
        """
            Simple function to determine correct key matching
            the input tuple or single paramter.

            @type typeArg:    String
            @param typeArg:   Key to look in correct sector (m/r/e)
            @type firstArg:   number
            @param firstArg:  first paramter in JSON tuple
            @type secondArg:  number
            @param secondArg: second paramter in JSON tuple

            @rtype:           dict
            @return:          Element from MRE-Dict, that has the key literals
                              for each paramter combination.
        """
        if (secondArg != None):
            return self.mreDict[typeArg][(firstArg, secondArg)]
        else:
            return self.mreDict[typeArg][firstArg]


    def pShutdown(self):
        """
            Cleanup after usage
        """
        self.sender.stop()
        self.jEventDict = None
        self.sender = None
        self.mreDict= None


    def createDicti(self):
        """
            Set of all possible permutations and keys.
            Different movement combinations require different keystrokes,
            which are hardcoded in this section.

            @rtype:  dict
            @return: return its dictionary with the stated content.
        """
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