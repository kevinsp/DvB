

class CADinfoClass(object):
	def __init__(self, name, id, volume):
		self.name = name
		self.id = id
		self.volume = volume
		
	def getName(self):
		return self.name
		
	def getUniqueID(self):
		return self.id
		
	def getVolume(self):
		return self.volume