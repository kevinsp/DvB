__author__ = 'MrLapTop'
import sys
sys.path.append(r"..\GUI")
from Checkpoint import Checkpoint
from Note import Note

from xml.etree import ElementTree
from xml.dom import minidom
try:
    from xml.etree.cElementTree import Element
    from xml.etree.cElementTree import SubElement
except ImportError:
    from xml.etree.ElementTree import Element
    from xml.etree.ElementTree import SubElement
# posX, posZ, posY, name, eulerX, eulerZ, eulerY, comment=""

"""This class is an Obj that holds data"""
class dummyObj(object):
    #the overgiven dict will be convortet into membervarbs (of the createt dummyObj)
    def __init__(self,dicti):
        self.__dict__.update(dicti)
"""
    Mehtode to save Membervarbs to xml file.
    @elementList - list with obj that you want to save
    @filepath - path where you will find the xml file after running this methode
"""
def saveXml(elementList,filepath):
    output_file = open(str(filepath),"w")
    root = Element("root")
    for element in elementList:
        helperDict = dict(element.__dict__)
        #print helperDict
        subelement = SubElement(root,"Subelement")
        for key,value in helperDict.iteritems():
            name = str(key)
            typi = type(value).__name__
            checkpointAttr = SubElement(subelement,name,attrTyp = typi)
            checkpointAttr.text = str(value)

    output_file.write(ElementTree.tostring(root))
    output_file.close()
    #print prettify(root)
"""
    Methode to Load form Xml file. Return value is a list with dummyObj.
    @filepath - file diraytory to the file where you want to load from
"""
def loadXml(filepath):
    input_file = open (str(filepath),"r")
    document = ElementTree.parse(input_file)
    returnList = []
    root = document.getroot()

    for Subelement in root:
        helperDict = dict()
        for subElementAttr in Subelement:
            attrTyp = subElementAttr.attrib["attrTyp"]
            attrTypConv = ""

            if attrTyp == "str":
                attrTypConv = str(subElementAttr.text)
            elif attrTyp == "int":
                attrTypConv = int(subElementAttr.text)

            helperDict[str(subElementAttr.tag)] = attrTypConv
            #print helperDict

        returnList.append(dummyObj(helperDict))
    input_file.close()
    return returnList

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
"""
    This methode takes a list and fills it with my Object.
    @myList - the List i want to be filled
    @filepath - file diraytory to the file where you want to load from
    @consti - the name of the constructor i want to have. example "MyObj()" where MyObj is the obj you want
"""
def buildMyObjList(myList,filepath,consti):
    loadList = loadXml(filepath)
    #transforms the dummyObj into your obj
    for elm in loadList:
        obj = eval(consti) # replace this, with the obj you want
        obj.update(elm.__dict__)
        myList.append(obj)


# posX, posZ, posY, name, eulerX, eulerZ, eulerY, comment=""
cp1 = Checkpoint(0,0,0,"Blub",0,0,0,"FUCK")
cp2 = Checkpoint(1,1,1,"Noob",1,1,1,"OHla")
nt1 = Note(0,0,0,"Blue",0,0,0)
nt2 = Note(1,1,1,"Red",1,1,1)

cpList = [cp1,cp2]
ntList = [nt1,nt2]

saveXml(ntList,"noteXml.xml")
saveXml(cpList,"cpXml.xml")

myListCP = []
buildMyObjList(myListCP,"cpXml.xml","Checkpoint()")
print "Cp1 and xmListCP[0] are equal?"
print  myListCP[0].__dict__ == cp1.__dict__

myListNT= []
buildMyObjList(myListNT,"noteXml.xml","Note()")
print "nt1 and xmListNT[0] are equal?"
print nt1.__dict__ == myListNT[0].__dict__




