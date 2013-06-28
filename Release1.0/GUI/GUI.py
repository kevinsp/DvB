
"""Danke, dass Sie sich fuer unsere Software entschieden haben.
\nHier die wichtigsten Shortcuts zum bedienen des Programmes:
c:     Anzeigen der bereits gesetzten Checkpoints
n:     Anzeigen der bereits gesetzten 3D Notizen
v:     Anzeigen der Vogelperspektive
f:     Flugmodus aktivieren/deaktivieren
h:     Anzeigen dieser Hilfe
p:     Anzeigen der aktuellen Position
+ -:   Erhoehen/Verringern der Bewegungsgeschwindigkeit 0.2-40
* /:   Erhoehen/Verringern der Fluggeschwindigkeit 0.05-10"""



"""import vizard Module"""
import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizpopup
import vizact
import viznet


"""import  XML Module"""
from xml.etree import ElementTree
from xml.dom import minidom

try:
	from xml.etree.cElementTree import Element
	from xml.etree.cElementTree import SubElement
except ImportError:
	from xml.etree.ElementTree import Element
	from xml.etree.ElementTree import SubElement



import sys
sys.path.append(r"..\RemoteAppServer")
from RemoteAppMain import RemoteAppLuncher

"""Eigene Module"""
import CheckpointFunktionen
from Checkpoint import Checkpoint
import Notes
from Note import Note
import MouseAndMovement
import BirdView
import Porten
import RemoteAppMain
import GlobalVariables
import SettingPanel


viz.go(viz.QUAD_BUFFER)
#viz.go()



modelIsLoaded = False





class DummyObj(object):
        """This class is an Obj that holds data"""
        
	"""the overgiven dict will be convortet into membervarbs (of the createt dummyObj)"""
	def __init__(self,dicti):
		self.__dict__.update(dicti)





class Oberflaeche(object):
        """Die Hauptklasse/Oberflaeche"""
        
	def __init__(self):
                """Initialisiere die Oberflaeche"""
		self.neu = None
		self.model = None
		self.thread = None

		viz.MainWindow.fov(60)
		viz.collision(viz.ON)

		viz.window.setFullscreen(True)
                """Umgebung laden"""
		viz.addChild('sky_day.osgb')
		
		viz.setOption('viz.fullscreen',1)
		viz.fov(40.0,1.333)
		viz.setOption('viz.stereo', viz.QUAD_BUFFER)
		
		"""Menuebar"""
		self.menubar = vizmenu.add()
		self.menubar.setVisible(False)

		"""Model DropDownMenu"""
		self.BearbeitenMenu = self.menubar.add("Model")
		self.buttonDateiOeffnen = self.BearbeitenMenu.add(viz.BUTTON_LABEL, "Datei oeffnen")
		self.buttonModelEntfernen = self.BearbeitenMenu.add(viz.BUTTON_LABEL, "Model entfernen")

		"""Funktionen DropDownMenu"""
		self.FunktionenMenu = self.menubar.add("Funktionen")
		self.checkPointLoeschen = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Checkpoint loeschen")
		self.checkPortButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Zu Checkpoint springen")
		self.deleteNoteButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "3D Notiz loeschen")
		self.notePortButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Zu 3D Notizen springen")
		self.beliebigPortButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Springen zu")
		"""Alphaslider"""
		self.alphaSlider = self.FunktionenMenu.add(viz.PROGRESS_BAR, "1.00", "Alphawert")
		self.alphaSlider.set(1.0)
		
		"""Einfuegen DropDownMenu"""
		self.EinfuegenMenu = self.menubar.add("Einfuegen")
		self.checkPointSetzen = self.EinfuegenMenu.add(viz.BUTTON_LABEL, "Checkpoint")
		self.buttonNotizEinfuegen = self.EinfuegenMenu.add(viz.BUTTON_LABEL, "Notiz")

		"""Optionen DropDownMenu"""
		self.OptionenMenu = self.menubar.add("Optionen")
		self.AndroidAppButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Android Server")
		self.settingButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Einstellungen")
		self.speichernButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Speichern")
		self.ladenButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Laden")
		"""Menuebar Theme"""
		viz.setTheme(GlobalVariables.darkTheme)
		
		"""Position Anzeige"""
		self.textScreen = viz.addText('',viz.SCREEN) 
		self.textScreen.setScale(0.3,0.3,0)
		self.textScreen.alignment(viz.ALIGN_RIGHT_TOP)
		self.textScreen.setPosition([0.99,0.787,0])
		self.textScreen.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
		self.textScreen.setBackdropColor([0,0,0])
		
		"""IP-Anzeige"""
		self.ipTextScreen = viz.addText("", viz.SCREEN)
		self.ipTextScreen.setScale(0.3,0.3,0)
		self.ipTextScreen.alignment(viz.ALIGN_RIGHT_TOP)
		self.ipTextScreen.setPosition([0.79,0.99,0])
		self.ipTextScreen.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
		self.ipTextScreen.setBackdropColor([0,0,0])
		
		"""Steuerung"""
		viz.mouse(viz.ON)
		viz.mouse.setTrap() """Maus kann nicht aus dem Fenster gehen"""

		GlobalVariables.tracker = vizcam.addWalkNavigate(moveScale=GlobalVariables.moveSpeed) """Initialisieren Tracker mit bestimmter Geschwindigkeit"""
		GlobalVariables.tracker.setPosition([0,1.8,0]) """Setze Tracker Position"""
		GlobalVariables.link = viz.link(GlobalVariables.tracker,viz.MainView) """Verlinke Tracker mit MainView"""
		viz.mouse.setVisible(False)

		"""Boden laden"""
		self.ground1 = viz.addChild('ground.osgb')
		self.ground2 = viz.addChild('ground.osgb')
		self.ground2.setPosition(0,0,50)
		
		"""Begrue�ungsnachricht"""
		self.checkPointsPanel = vizinfo.InfoPanel(align=viz.ALIGN_CENTER,fontSize=15,icon=False,key="h")
		self.checkPointsPanel.visible(True)

                               """Button Definition"""

		"""Model Buttons"""
		vizact.onbuttonup(self.buttonDateiOeffnen, self.setModel)
		vizact.onbuttonup(self.buttonModelEntfernen, self.deleteModel)

		"""Note Buttons"""
		vizact.onbuttonup(self.buttonNotizEinfuegen, Notes.openTextBox, self.menubar)
		vizact.onbuttonup(self.deleteNoteButton, Notes.delete3DNote, self.menubar)
		vizact.onbuttonup(self.notePortButton, Notes.port3DNote, self.menubar)

		"""Checkpoints Buttons"""
		vizact.onbuttonup(self.checkPointSetzen, CheckpointFunktionen.createCheckpoint, self.menubar)
		vizact.onbuttonup(self.checkPointLoeschen, CheckpointFunktionen.deleteCheckpoint, self.menubar)
		vizact.onbuttonup(self.checkPortButton, CheckpointFunktionen.portCheckPoint, self.menubar)

		"""Port Button"""
		vizact.onbuttonup(self.beliebigPortButton, Porten.porten, self.menubar)
	
		"""Optionen Buttons"""
		vizact.onbuttonup(self.AndroidAppButton, self.startAndroid)
		vizact.onbuttonup(self.settingButton, SettingPanel.oeffneSettingPanel, self.menubar)
		vizact.onbuttonup(self.speichernButton, self.save)
		vizact.onbuttonup(self.ladenButton, self.load)
	
		"""Shortcuts"""
		vizact.onkeydown(viz.KEY_CONTROL_L, MouseAndMovement.enableDisableMouse, self.menubar)
		vizact.onkeydown("c", CheckpointFunktionen.checkPoints, False)
		vizact.onkeydown("v", BirdView.enableBirdEyeView)
		vizact.onkeydown("n", Notes.noteView, False)
		vizact.onkeydown("f", MouseAndMovement.flugModusOnOff)
		vizact.onkeydown("p", self.zeigePosition)
		vizact.onkeydown("C", CheckpointFunktionen.checkPoints, False)
		vizact.onkeydown("V", BirdView.enableBirdEyeView)
		vizact.onkeydown("N", Notes.noteView, False)
		vizact.onkeydown("F", MouseAndMovement.flugModusOnOff)
		vizact.onkeydown("P", self.zeigePosition)
		vizact.onkeydown(viz.KEY_KP_ADD, MouseAndMovement.speedUp)
		vizact.onkeydown(viz.KEY_KP_SUBTRACT, MouseAndMovement.speedDown)
		vizact.onkeydown(viz.KEY_KP_DIVIDE, MouseAndMovement.flySpeedDown)
		vizact.onkeydown(viz.KEY_KP_MULTIPLY, MouseAndMovement.flySpeedUp)
		vizact.onkeydown(viz.KEY_SHIFT_L, MouseAndMovement.moveUpAndDown,  viz.KEY_SHIFT_L)
		vizact.onkeydown(viz.KEY_ALT_L, MouseAndMovement.moveUpAndDown, viz.KEY_ALT_L)
		
		
		"""Progressbar Alphawert"""
		vizact.onslider( self.alphaSlider, self.setAlpha )
	
	
	def setAlpha(self, slider):
                """Setze Alphawert"""
	
		"""Falls ein Model vorhanden ist"""
		if self.model is not None:
			self.alphaSlider.message( str('%.2f'%(slider)) )
			self.model.alpha(slider)

	
	def startAndroid(self):
                """Starte Server fuer Android"""
                
		"""starte nur einen Server, wenn noch keiner laeuft"""
		if GlobalVariables.serverIsRunning is False: 
			self.ipTextScreen.message(str(viz.net.getIP())) """Zeige IP-Adresse an"""
			self.neu = RemoteAppMain.RemoteAppLuncher(str(viz.net.getIP()), GlobalVariables.tracker, GlobalVariables.checkPointsList)
			self.thread = viz.director(self.neu.lunch) """Starte Server in neuem Thread"""
			GlobalVariables.serverIsRunning = True
		"""Falls bereits ein Server laeuft"""
		else:
			GlobalVariables.serverIsRunning = False
			self.ipTextScreen.message("")
			self.neu.shutdown() """beende Server"""
			
	
	def zeigePosition(self):
                """Zeige zurzeitige Position"""
                
		
		def changeMessage():
                        """Aendere die Positionsanzeige"""
                        
			userPosition = viz.MainView.getPosition() """Frage User Position"""
			message = str(round(userPosition[0],2)) + " " + str(round(userPosition[1],2)) + " " + str(round(userPosition[2],2))
			self.textScreen.message(str(message)) """Setze Anzeige auf neue Position"""
			
		"""Falls Position noch nicht gezeigt wird"""
		if (GlobalVariables.showPosi is False):
			self.textScreen.visible(True)
			GlobalVariables.showPosi = True
			vizact.ontimer(0.1, changeMessage) """Aktualisiere durchgehend die Positionsangabe"""
		else:
			self.textScreen.visible(False)
			GlobalVariables.showPosi = False
		
	
	def setModel (self):
                """Lade neues Model"""
                
		global modelIsLoaded
		"""Falls noch kein Model geladen ist"""
		if not (modelIsLoaded):
			self.alphaSlider.set(1.0) """Setze AlphaSlider zurueck"""
			self.model = viz.addChild(vizinput.fileOpen()) """Oeffne Menue zum auswaehlen der Datei"""
			self.model.disable(viz.CULL_FACE)
			self.model.setPosition(0,0,60, viz.ABS_GLOBAL)
			self.model.setEuler([0,0,0])
			viz.collision(viz.ON)
			modelIsLoaded = True
			
			
	def deleteModel(self):
                """Loesche Model"""
                
		global modelIsLoaded
		self.model.remove()
		modelIsLoaded = False


	
	def save(self):
                """Speichere alle Checkpoints und 3D Notizen in XML Dateien"""
                
		self.saveXml(GlobalVariables.checkPointsList, "Checkpoints.xml")
		self.saveXml(GlobalVariables.noteList, "3D Notizen.xml")
	
	
	def load(self):
                """Lade alle Checkpoints und 3D Notizen aus XML Dateien"""
                
		self.buildMyObjList(GlobalVariables.checkPointsList, "Checkpoints.xml", "Checkpoint()")
		self.buildMyObjList(GlobalVariables.noteList, "3D Notizen.xml", "Note()")


	def saveXml(self, elementList,filepath):
                """
		Mehtode to save Membervarbs to xml file.
		@elementList - list with obj that you want to save
		@filepath - path where you will find the xml file after running this methode
                """
                
		output_file = open(str(filepath),"w")
		root = Element("root")
		for element in elementList:
			helperDict = dict(element.__dict__)
			subelement = SubElement(root,"Subelement")
			for key,value in helperDict.iteritems():
				name = str(key)
				typi = type(value).__name__
				checkpointAttr = SubElement(subelement,name,attrTyp = typi)
				checkpointAttr.text = str(value)
		output_file.write(ElementTree.tostring(root))
		output_file.close()

	def loadXml(self, filepath):
                """
		Methode to Load form Xml file. Return value is a list with dummyObj.
		@filepath - file diraytory to the file where you want to load from
                """
                
		input_file = open (str(filepath),"r")

		document = ElementTree.parse(input_file)
		returnList = []
		root = document.getroot()
		for Subelement in root:
			helperDict = dict()
			for subElementAttr in Subelement:
				attrTyp = subElementAttr.attrib["attrTyp"]
				attrTypConv = ""
				if attrTyp == "str":
					attrTypConv = str(subElementAttr.text)
				elif attrTyp == "int":
					attrTypConv = int(subElementAttr.text)
				elif attrTyp == "float":
					attrTypConv = float(subElementAttr.text)
				helperDict[str(subElementAttr.tag)] = attrTypConv
				
			returnList.append(DummyObj(helperDict))
		input_file.close()
		return returnList
			
	def prettify(self, elem):
		"""Return a pretty-printed XML string for the Element."""
		
		rough_string = ElementTree.tostring(elem, 'utf-8')
		reparsed = minidom.parseString(rough_string)
		return reparsed.toprettyxml(indent="  ")
		
		

	def buildMyObjList(self, myList,filepath,consti):
                """
		This methode takes a list and fills it with my Object.
		@myList - the List i want to be filled
		@filepath - file diraytory to the file where you want to load from
		@consti - the name of the constructor i want to have. example "MyObj()" where MyObj is the obj you want
                """
                
		loadList = self.loadXml(filepath)
		"""transforms the dummyObj into your obj"""
		for elm in loadList:
			obj = eval(consti) """replace this, with the obj you want"""
			obj.update(elm.__dict__)
			myList.append(obj)
			
		"""Setze die 3D Notes wieder in die Umgebung"""
		for a in GlobalVariables.noteList:
			text3D = viz.addText3D(a.name, pos = [a.posX, a.posZ, a.posY])
			text3D.setScale(0.2, 0.2, 0.2)
			text3D.color(viz.RED)
			GlobalVariables.noteListObjects.append(text3D)
		"""Aktualisiere die angezeigte Liste"""
		if CheckpointFunktionen.checkPointsVisible:
			CheckpointFunktionen.checkPoints(False)
			CheckpointFunktionen.checkPoints(False)
		elif Notes.checkNotesVisible:
			Notes.noteView(False)
			Notes.noteView(False)
		
if __name__ == "__main__":

		oberflaeche = Oberflaeche()
