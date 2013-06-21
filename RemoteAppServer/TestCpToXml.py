__author__ = 'MrLapTop'
import sys
sys.path.append(r"..\GUI")
from Checkpoint import Checkpoint

from xml.etree import ElementTree
from xml.dom import minidom
try:
    from xml.etree.cElementTree import Element
    from xml.etree.cElementTree import SubElement
except ImportError:
    from xml.etree.ElementTree import Element
    from xml.etree.ElementTree import SubElement
# posX, posZ, posY, name, eulerX, eulerZ, eulerY, comment=""


def saveCp(cpList):
    output_file = open("cpXml.xml","w")
    checkpoints = Element("checkpoints")
    for cp in cpList:
        helperDict = dict(cp.__dict__)
        #print helperDict
        checkpoint = SubElement(checkpoints,"checkpoint")
        for key,value in helperDict.iteritems():
            name = str(key)
            typi = type(value).__name__
            checkpointAttr = SubElement(checkpoint,name,attrTyp = typi)
            checkpointAttr.text = str(value)

    output_file.write(ElementTree.tostring(checkpoints))
    output_file.close()
    #print prettify(checkpoints)

def loadCp():
    input_file = open ("cpXml.xml","r")
    document = ElementTree.parse(input_file)
    cpList = []
    checkpoints = document.getroot()

    for checkpoint in checkpoints:
        helperDict = dict()
        for checkpointAttr in checkpoint:
            attrTyp = checkpointAttr.attrib["attrTyp"]
            attrTypConv = ""

            if attrTyp == "str":
                attrTypConv = str(checkpointAttr.text)
            elif attrTyp == "int":
                attrTypConv = int(checkpointAttr.text)

            helperDict[str(checkpointAttr.tag)] = attrTypConv
            #print helperDict
        cp = Checkpoint(0,0,0,"_",0,0,0,"_")
        print cp.__dict__
        print cp.__dict__.update(helperDict)
        cpList.append()
    input_file.close()
    return cpList

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


# posX, posZ, posY, name, eulerX, eulerZ, eulerY, comment=""
cp1 = Checkpoint(0,0,0,"Blub",0,0,0,"FUCK")

saveCp([cp1])
cpList = loadCp()
print cpList[0].__dict__ == cp1.__dict__