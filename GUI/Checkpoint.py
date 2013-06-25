
#Checkpoint Objekt
class Checkpoint(object):

    def __init__(self, posX=0, posZ=1.82, posY=0, name="test", eulerX=0, eulerZ=0, eulerY=0, comment=""):
        self.posX = posX
        self.posZ = posZ
        self.posY = posY
        self.name = name
        self.eulerX = eulerX
        self.eulerZ = eulerZ
        self.eulerY = eulerY
        self.comment = comment

    def update(self,dicti):
        for key,value in dicti.iteritems():
            setattr(self,key,value)

