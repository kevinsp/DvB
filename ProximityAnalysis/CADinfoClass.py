

class CADinfoClass(object):
	def __init__(self, name, id, centerPosition, volume):
		self.name = name
		self.id = id
		self.centerPosition = centerPosition
		self.volume = volume
		
	def getName(self):
		return self.name
		
	def getUniqueID(self):
		return self.id
		
	def getCenterPosition(self):
		return self.centerPosition
		
	def getVolume(self):
		return self.volume