
class Parser(object):
	def __init__(self, inputFile):
		self.inputFile = inputFile
		self.sortedInput = self.initializeSort()
		#print self.sortedInput
		#for el in self.sortedInput:
		#	print(el),
		'''self.osgt = ''
		bracketCounter = 0
		nodeCounter = -1
		nodeElement = 0
		nodeList = []
		with open(inputFile, 'r') as eingabe:
			for line in eingabe:
				curLine = str(line)
				self.osgt += curLine
				if curLine.find('{'):
					bracketCounter += 1
					curLine = curLine.split('{')[0].strip()
					if bracketCounter == 2:
						nodeElement = 0
						nodeCounter += 1
						nodeList[nodeCounter] = curLine
				elif str(line).find('}'):
					bracketCounter -= 1
				if bracketCounter:
					pass'''
	
	def initializeSort(self):
		self.bracketOpenCounter = 0
		self.bracketCloseCounter = 0
		self.lineCounter = 0
		self.nameCounter = 0
		self.blockLineList = []
		self.blockStarts = []
		self.blockEnds = []
		with open(self.inputFile, 'r') as eingabe:
			for zeile in eingabe:
				self.lineCounter += 1
				zeile = zeile.strip()
				'''if zeile.startswith('Name "'):
					self.nameCounter += 1
					print(str(self.lineCounter)+' '),'''
				if zeile.endswith('{'):
					self.bracketOpenCounter += 1
					self.blockStarts.append(self.lineCounter)
					#print(zeile.split('{')[0].strip())
				if zeile.endswith('}'):
					self.bracketCloseCounter += 1
					self.blockEnds.append(self.lineCounter)
					self.blockLineList.append((self.blockStarts.pop(),self.blockEnds.pop()))
				#if self.bracketCloseCounter == (self.bracketOpenCounter - 1):
					#self.blockLineList.append(())
					#print('Counter gleich -1 '+zeile+' Zeile: '+str(self.lineCounter))
		#print(str(self.bracketCloseCounter)+' close and open '+str(self.bracketOpenCounter))
		print(self.blockLineList)
	
	def preSortOld(self, inputFile):
		osgt = ''
		bracketCounter = 0
		nodeCounter = 0
		#nodeElement = 0
		nodeList = []
		nodeDic = []
		#nodeList[0] = ''
		with open(inputFile, 'r') as eingabe:
			for line in eingabe:
				curLine = str(line)
				if line.endswith('{'):
					bracketCounter += 1
					if bracketCounter == 1:
						continue
					if bracketCounter == 2:
						nodeName = curLine.split('{')[0].strip()
						nodeKey = str(nodeCounter)+' '+str(nodeName)
						osgt = ''
						continue
				osgt += curLine
				if line.endswith('}'):
					bracketCounter -= 1
					if bracketCounter is not 2:
						continue
					nodeList.append((nodeKey, osgt))
					#nodeList[nodeCounter] = nodeDic
					nodeCounter += 1
					osgt = ''
					nodeKey = ''
					continue
		'''with open(inputFile, 'r') as eingabe:
			for line in eingabe:
				curLine = str(line)
				osgt += curLine
				if line.find('{'):
					bracketCounter += 1
					print(bracketCounter),
					#curLine = curLine.split('{')[0].strip()
				if line.find('}'):
					bracketCounter -= 1
					print(bracketCounter),
				if bracketCounter == 2:
					print(bracketCounter),
					print('hello'),
					print(osgt)
					nodeList[nodeCounter] = osgt
					nodeCounter += 1
					osgt = '' '''
		return nodeList


#print self.cad.getStats()


if __name__ == '__main__':
	parser = Parser(r'C:\Users\Kevin\DvB\OSGT_3DS_DEFINE_PROPERTIES\3DSMAX_DEFINE_PROPERTIES_OSGT.osgt')
	
	