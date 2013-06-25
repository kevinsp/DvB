

class CADinfoClass(object):
	def __init__(self, name='', id=0, centerPosition=(0,0,0), radius=1, volume=10):
		self.name = name
		self.id = id
		self.centerPosition = centerPosition
		self.volume = volume
		self.radius = radius
		
	def getName(self):
		return self.name
		
	def getID(self):
		return self.id
		
	def getCenterPosition(self):
		return self.centerPosition
		
	def getRadius(self):
		return self.radius
		
	def getVolume(self):
		return self.volume