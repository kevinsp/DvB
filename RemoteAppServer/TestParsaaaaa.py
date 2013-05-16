__author__ = 'MrLapTop'

from Parser import Parser
import viz
from  JasonEventModule import JasonEventRegister
from JasonEventModule import JassonCam

def do(dict):
    for eventID,jEObjL in dict.iteritems():
        print eventID
        for jEObj in jEObjL:
            print jEObj.key

if __name__ == "__main__":
    dict1 = '{"m":{"a":0,"b":1},"r":{"x":0,"y":0},"e":0}'

    viz.go()
    viz.addChild('piazza.osgb')

    jasonEventRegister = JasonEventRegister()
    jCam = JassonCam(jasonEventRegister)

    parser = Parser(jasonEventRegister)
    parser.parseJson(dict1)
    #viz.director( do ,parser.sender.jEventsToSend)
