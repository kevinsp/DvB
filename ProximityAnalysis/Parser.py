

class Parser(object):
	def __init__(self, inputFile):
		self.inputFile = inputFile
		self.initializeSort()
		self.createInfoBlocks()
		self.parseInfoBlocks()
		print(self.infoList)
	
	def getInfoBlocks(self):
		return self.infoBlocks
	
	'''
	extract bracket structure from file
	when a bracket opens/closes, save line number to blockStarts/blockEnds
	as a bracket closes, take the last line numbers from blockStarts AND blockEnds
	and save them as a tuple to blockLineList
	afterwards you have a list of cohesive bracket blocks
	'''
	def initializeSort(self):
		self.lineCounter = 0
		self.blockLineList = []
		self.blockStarts = []
		self.blockEnds = []
		self.fileText = []
		with open(self.inputFile, 'r') as eingabe:
			for zeile in eingabe:
				zeile = str(zeile).strip()
				zeile = zeile.replace('ß','ss').replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('\t',' ')
				self.fileText.append(zeile)
				if zeile.endswith('{'):
					self.blockStarts.append(self.lineCounter)
				if zeile.endswith('}'):
					self.blockEnds.append(self.lineCounter)
					self.blockLineList.append((self.blockStarts.pop(),self.blockEnds.pop()))
				self.lineCounter += 1
				
	def createInfoBlocks(self):
		self.infoBlocks = {}
		for block in self.blockLineList:
			blockBoundaries = self.fileText[block[0]:block[1]]
			blockString = []
			infoCounter = 0
			for zeile in blockBoundaries:
				blockString.append(zeile)
				if zeile.endswith('{'):
					if infoCounter == 1:
						break
					infoCounter += 1
			self.infoBlocks[block] = blockString
			
	def parseInfoBlocks(self):
		self.infoList = {}
		for el in self.infoBlocks:
			infos = []
			blockList = self.infoBlocks[el]
			info = blockList[0]
			for info in blockList:
				if info.find('Name') >= 0 and info.find('"') >= 0:
					infos.append(('blockName',info[info.index('"')+1:info.index('"',info.index('"')+1)]))
				if info.find('UniqueID') >= 0:
					infos.append(('ID',info[info.index(' ')+1:]))
				continue
			if info.find('Array') >= 0:
				infos.append(('blockName','Array'))
				infos.append(('arrayList',blockList[1:]))
			if info.find('Matrix') >= 0:
				infos.append(('blockName','Matrix'))
				infos.append(('matrixList',blockList[1:]))
			self.infoList[el] = infos
			


if __name__ == '__main__':
	parser = Parser(r'C:\Users\Kevin\DvB\OSGT_3DS_DEFINE_PROPERTIES\3DSMAX_DEFINE_PROPERTIES_OSGT.osgt')
	
	