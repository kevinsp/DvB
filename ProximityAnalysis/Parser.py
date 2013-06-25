from CADinfoClass import CADinfoClass
from math import sqrt, pow

class Parser(object):
	def __init__(self, inputFile):
		self.inputFile = inputFile
		self.initializeSort()
		self.createInfoBlocks()
		self.parseInfoBlocks()
		self.defineCenterPosition()
		self.cadClasses = []
		print(self.infoList)
		
	def getCADClasses(self):
		return self.cadClasses
	
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
			firstInfo = blockList[0]
			for infoEl in blockList:
				if infoEl.find('Name ') >= 0 and infoEl.find('"') >= 0:
					infos.append(('blockName',infoEl[infoEl.index('"')+1:infoEl.index('"',infoEl.index('"')+1)]))
				if infoEl.find('UniqueID ') >= 0:
					infos.append(('uniqueID',infoEl[infoEl.index(' ')+1:]))
			if firstInfo.find('Array ') >= 0:
				infos.append(('blockName','Array'))
				infos.append(('arrayList',self.convertListToVector(blockList[1:])))
				infos.append(('arrayID',int(firstInfo[firstInfo.index('ArrayID ')+len('ArrayID')+1:firstInfo.index(' ',firstInfo.index('ArrayID ')+len('ArrayID')+2)])))
			if firstInfo.find('Matrix ') >= 0:
				infos.append(('blockName','Matrix'))
				infos.append(('matrixList',self.convertListToVector(blockList[1:])))
			self.infoList[el] = infos
			
	def defineCenterPosition(self):
		for el in self.infoList:
			info = self.infoList[el]
			for listEl in info:
				if listEl[0] == 'arrayList':
					vectors = listEl[1]
					surroundings = self.findSurroundings(vectors)
					info.append(('arraySurrounding', surroundings))
					if len(surroundings) == 8:
						center = (0.5*(surroundings[1][0] + surroundings[4][0]),0.5*(surroundings[1][1] + surroundings[4][1]),0.5*(surroundings[1][2] + surroundings[4][2]))
						info.append(('centerPosition', center))
						radius = sqrt(pow(surroundings[1][0]-surroundings[0][0],2)+pow(surroundings[1][1]-surroundings[0][1],2)+pow(surroundings[1][2]-surroundings[0][2],2))+0.5
						info.append(('radius', radius))
	
	def findSurroundingsLong(self, vectors):
		if len(vectors[0]) == 2:
			(maxX, maxY) = (0, 0)
			(minX, minY) = (0, 0)
			for vector in vectors:
				curX, curY = vector[0], vector[1]
				if curX > maxX:
					maxX = curX
				if curX <= minX:
					minX = curX
				if curY > maxY:
					maxY = curY
				if curY <= minY:
					minY = curY
			return [(minX, minY),(minX, maxY),(maxX, maxY),(maxX, minY)]
		(maxX, maxY, maxZ) = (0, 0, 0)
		(minX, minY, minZ) = (0, 0, 0)
		for vector in vectors:
			curX, curY, curZ = vector[0], vector[1], vector[2]
			if curX > maxX:
				maxX = curX
			if curX <= minX:
				minX = curX
			if curY > maxY:
				maxY = curY
			if curY <= minY:
				minY = curY
			if curZ > maxZ:
				maxZ = curZ
			if curZ <= minZ:
				minZ = curZ
		return [(minX, minY, minZ),(minX, minY, maxZ),(minX, maxY, maxZ),(minX, maxY, minZ),(maxX, maxY, minZ),(maxX, maxY, maxZ),(maxX, minY, maxZ),(maxX, minY, minZ)]
	
	def findSurroundings(self, vectors):
		(maxX, maxY, maxZ) = (0, 0, 0)
		(minX, minY, minZ) = (0, 0, 0)
		vectorBool = (len(vectors[0]) == 3)
		for vector in vectors:
			curX, curY = vector[0], vector[1]
			if curX > maxX:
				maxX = curX
			if curX <= minX:
				minX = curX
			if curY > maxY:
				maxY = curY
			if curY <= minY:
				minY = curY
			if vectorBool:
				curZ = vector[2]
				if curZ > maxZ:
					maxZ = curZ
				if curZ <= minZ:
					minZ = curZ
		if len(vectors[0]) == 3:
			return [(minX, minY, minZ),(minX, minY, maxZ),(minX, maxY, maxZ),(minX, maxY, minZ),(maxX, maxY, minZ),(maxX, maxY, maxZ),(maxX, minY, maxZ),(maxX, minY, minZ)]
		return [(minX, minY),(minX, maxY),(maxX, maxY),(maxX, minY)]
	
	def convertListToVector(self, arrayList):
		vectorArray = []
		for points in arrayList:
			pointList = points.split()
			vector = []
			for point in pointList:
				point = float(point)
				vector.append(point)
			vector = tuple(vector)
			vectorArray.append(vector)
		return vectorArray


if __name__ == '__main__':
	parser = Parser(r'C:\Users\Kevin\DvB\OSGT_3DS_DEFINE_PROPERTIES\3DSMAX_DEFINE_PROPERTIES_OSGT.osgt')
	
	