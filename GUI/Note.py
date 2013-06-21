




class Note(object):
	def __init__(self, posX, posZ, posY, name, eulerX, eulerZ, eulerY):
		self.posX = posX
		self.posZ = posZ
		self.posY = posY
		self.name = name
		self.eulerX = eulerX
		self.eulerZ = eulerZ
		self.eulerY = eulerY
		
	def update(self,dicti):
		for key,value in dicti.iteritems():
			setattr(self,key,value)
		
