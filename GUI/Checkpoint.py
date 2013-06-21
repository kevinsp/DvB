

class Checkpoint(object):

    def __init__(self, posX, posZ, posY, name, eulerX, eulerZ, eulerY, comment=""):
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

