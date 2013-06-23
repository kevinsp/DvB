




class Note(object):
	def __init__(self, posX=0, posZ=0, posY=0, name="_", eulerX=0, eulerZ=0, eulerY=0):
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
		
