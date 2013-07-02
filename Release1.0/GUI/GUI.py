



#"""import vizard Module"""
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


#"""import  XML Module"""
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

#"""Eigene Module"""
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



ModellIsLoaded = False





class DummyObj(object):
        """This class is an Obj that holds data"""
        
	
	def __init__(self,dicti):
                """the overgiven dict will be convortet into membervarbs (of the createt dummyObj)"""
                
		self.__dict__.update(dicti)





class Oberflaeche(object):
        """Die Hauptklasse/Oberflaeche"""
        
	def __init__(self):
                """Initialisiere die Oberflaeche"""
                
                self.message = """Danke, dass Sie sich fuer unsere Software entschieden haben.

Hier die wichtigsten Shortcuts zum bedienen des Programmes:
    c:     Anzeigen der bereits gesetzten Checkpoints
    n:     Anzeigen der bereits gesetzten 3D Notizen
    v:     Anzeigen der Vogelperspektive
    f:     Flugmodus aktivieren/deaktivieren
    h:     Anzeigen dieser Hilfe
    p:     Anzeigen der aktuellen Position
    + -:   Erhoehen/Verringern der Bewegungsgeschwindigkeit 0.2-40
    * /:   Erhoehen/Verringern der Fluggeschwindigkeit 0.05-10"""

                self.neu = None
		self.modell = None
		self.thread = None

		viz.MainWindow.fov(60)
		viz.collision(viz.ON)

		viz.window.setFullscreen(True)
		#"""Umgebung laden"""
		viz.addChild('sky_day.osgb') 
		
		viz.setOption('viz.fullscreen',1)
		viz.fov(40.0,1.333)
		viz.setOption('viz.stereo', viz.QUAD_BUFFER)
		
		#"""Menuebar"""
		self.menubar = vizmenu.add()
		self.menubar.setVisible(False)

		#"""modell DropDownMenu"""
		self.BearbeitenMenu = self.menubar.add("Modell")
		self.buttonDateiOeffnen = self.BearbeitenMenu.add(viz.BUTTON_LABEL, "Modell oeffnen")
		self.buttonModellEntfernen = self.BearbeitenMenu.add(viz.BUTTON_LABEL, "Modell entfernen")

		#"""Funktionen DropDownMenu"""
		self.FunktionenMenu = self.menubar.add("Funktionen")
		self.checkPointLoeschen = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Checkpoint loeschen")
		self.checkPortButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Zu Checkpoint springen")
		self.deleteNoteButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "3D Notiz loeschen")
		self.notePortButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Zu 3D Notizen springen")
		self.beliebigPortButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Springen zu")
		#"""Alphaslider"""
		self.alphaSlider = self.FunktionenMenu.add(viz.PROGRESS_BAR, "1.00", "Alphawert")
		self.alphaSlider.set(1.0)
		
		#"""Einfuegen DropDownMenu"""
		self.EinfuegenMenu = self.menubar.add("Einfuegen")
		self.checkPointSetzen = self.EinfuegenMenu.add(viz.BUTTON_LABEL, "Checkpoint")
		self.buttonNotizEinfuegen = self.EinfuegenMenu.add(viz.BUTTON_LABEL, "Notiz")

		#"""Optionen DropDownMenu"""
		self.OptionenMenu = self.menubar.add("Optionen")
		self.AndroidAppButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Android Server")
		self.settingButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Einstellungen")
		self.speichernButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Speichern")
		self.ladenButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Laden")
		#"""Menuebar Theme"""
		viz.setTheme(GlobalVariables.darkTheme)
		
		#"""Position Anzeige"""
		self.textScreen = viz.addText('',viz.SCREEN) 
		self.textScreen.setScale(0.3,0.3,0)
		self.textScreen.alignment(viz.ALIGN_RIGHT_TOP)
		self.textScreen.setPosition([0.99,0.787,0])
		self.textScreen.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
		self.textScreen.setBackdropColor([0,0,0])
		
		#"""IP-Anzeige"""
		self.ipTextScreen = viz.addText("", viz.SCREEN)
		self.ipTextScreen.setScale(0.3,0.3,0)
		self.ipTextScreen.alignment(viz.ALIGN_RIGHT_TOP)
		self.ipTextScreen.setPosition([0.79,0.99,0])
		self.ipTextScreen.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
		self.ipTextScreen.setBackdropColor([0,0,0])
		
		#"""Steuerung"""
		viz.mouse(viz.ON)
		#"""Maus kann nicht aus dem Fenster gehen"""
		viz.mouse.setTrap() 
		
                #"""Initialisieren Tracker mit bestimmter Geschwindigkeit"""
		GlobalVariables.tracker = vizcam.addWalkNavigate(moveScale=GlobalVariables.moveSpeed)
		# """Setze Tracker Position"""
		GlobalVariables.tracker.setPosition([0,1.8,0])
		# """Verlinke Tracker mit MainView"""
		GlobalVariables.link = viz.link(GlobalVariables.tracker,viz.MainView)
		viz.mouse.setVisible(False)

		#"""Boden laden"""
		self.ground1 = viz.addChild('ground.osgb')
		self.ground2 = viz.addChild('ground.osgb')
		self.ground2.setPosition(0,0,50)
		
		#"""Begruessungsnachricht"""
		self.checkPointsPanel = vizinfo.InfoPanel(self.message, align=viz.ALIGN_CENTER,fontSize=15,icon=False,key="h")
		self.checkPointsPanel.visible(True)

               # """Button Definition"""

		#"""Modell Buttons"""
		vizact.onbuttonup(self.buttonDateiOeffnen, self.setModell)
		vizact.onbuttonup(self.buttonModellEntfernen, self.deleteModell)

		#"""Note Buttons"""
		vizact.onbuttonup(self.buttonNotizEinfuegen, Notes.openTextBox, self.menubar)
		vizact.onbuttonup(self.deleteNoteButton, Notes.delete3DNote, self.menubar)
		vizact.onbuttonup(self.notePortButton, Notes.port3DNote, self.menubar)

		#"""Checkpoints Buttons"""
		vizact.onbuttonup(self.checkPointSetzen, CheckpointFunktionen.createCheckpoint, self.menubar)
		vizact.onbuttonup(self.checkPointLoeschen, CheckpointFunktionen.deleteCheckpoint, self.menubar)
		vizact.onbuttonup(self.checkPortButton, CheckpointFunktionen.portCheckPoint, self.menubar)

		#"""Port Button"""
		vizact.onbuttonup(self.beliebigPortButton, Porten.porten, self.menubar)
	
		#"""Optionen Buttons"""
		vizact.onbuttonup(self.AndroidAppButton, self.startAndroid)
		vizact.onbuttonup(self.settingButton, SettingPanel.oeffneSettingPanel, self.menubar)
		vizact.onbuttonup(self.speichernButton, self.save)
		vizact.onbuttonup(self.ladenButton, self.load)
	
		#"""Shortcuts"""
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
		vizact.onkeydown(viz.KEY_RIGHT, MouseAndMovement.speedUp)
		vizact.onkeydown(viz.KEY_LEFT, MouseAndMovement.speedDown)
		vizact.onkeydown(viz.KEY_UP, MouseAndMovement.flySpeedUp)
		vizact.onkeydown(viz.KEY_DOWN, MouseAndMovement.flySpeedDown())
		vizact.onkeydown(viz.KEY_SHIFT_L, MouseAndMovement.moveUpAndDown,  viz.KEY_SHIFT_L)
		vizact.onkeydown(viz.KEY_ALT_L, MouseAndMovement.moveUpAndDown, viz.KEY_ALT_L)
		
		
		#"""Progressbar Alphawert"""
		vizact.onslider( self.alphaSlider, self.setAlpha )
	
	
	def setAlpha(self, slider):
                """Setze Alphawert"""
	
		#"""Falls ein Modell vorhanden ist"""
		if self.Modell is not None:
			self.alphaSlider.message( str('%.2f'%(slider)) )
			self.Modell.alpha(slider)

	
	def startAndroid(self):
                """Starte Server fuer Android"""
                
		#"""starte nur einen Server, wenn noch keiner laeuft"""
		if GlobalVariables.serverIsRunning is False:
                       # """Zeige IP-Adresse an"""
			self.ipTextScreen.message(str(viz.net.getIP())) 
			self.neu = RemoteAppMain.RemoteAppLuncher(str(viz.net.getIP()), GlobalVariables.tracker, GlobalVariables.checkPointsList)
			#"""Starte Server in neuem Thread"""
			self.thread = viz.director(self.neu.lunch) 
			GlobalVariables.serverIsRunning = True
		#"""Falls bereits ein Server laeuft"""
		else:
			GlobalVariables.serverIsRunning = False
			self.ipTextScreen.message("")
			#"""beende Server"""
			self.neu.shutdown() 
			
	
	def zeigePosition(self):
                """Zeige zurzeitige Position"""
                
		
		def changeMessage():
                        """Aendere die Positionsanzeige"""

                        #"""Frage User Position"""
			userPosition = viz.MainView.getPosition() 
			message = str(round(userPosition[0],2)) + " " + str(round(userPosition[1],2)) + " " + str(round(userPosition[2],2))
			#"""Setze Anzeige auf neue Position"""
			self.textScreen.message(str(message)) 
			
		#"""Falls Position noch nicht gezeigt wird"""
		if (GlobalVariables.showPosi is False):
			self.textScreen.visible(True)
			GlobalVariables.showPosi = True
			#"""Aktualisiere durchgehend die Positionsangabe"""
			vizact.ontimer(0.1, changeMessage) 
		else:
			self.textScreen.visible(False)
			GlobalVariables.showPosi = False
		
	
	def setModell (self):
                """Lade neues Modell"""
                
		global ModellIsLoaded
		#"""Falls noch kein Modell geladen ist"""
		if not (ModellIsLoaded):
                         #"""Setze AlphaSlider zurueck"""
			self.alphaSlider.set(1.0)
			# """Oeffne Menue zum auswaehlen der Datei"""
			self.Modell = viz.addChild(vizinput.fileOpen())
			self.Modell.disable(viz.CULL_FACE)
			self.Modell.setPosition(0,0,60, viz.ABS_GLOBAL)
			self.Modell.setEuler([0,0,0])
			viz.collision(viz.ON)
			ModellIsLoaded = True
			
			
	def deleteModell(self):
                """Loesche Modell"""
                
		global ModellIsLoaded
		self.Modell.remove()
		ModellIsLoaded = False


	
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
		#"""transforms the dummyObj into your obj"""
		for elm in loadList:
                         #"""replace this, with the obj you want"""
			obj = eval(consti)
			obj.update(elm.__dict__)
			myList.append(obj)
			
		#"""Setze die 3D Notes wieder in die Umgebung"""
		for a in GlobalVariables.noteList:
			text3D = viz.addText3D(a.name, pos = [a.posX, a.posZ, a.posY])
			text3D.setScale(0.2, 0.2, 0.2)
			text3D.color(viz.RED)
			GlobalVariables.noteListObjects.append(text3D)
		#"""Aktualisiere die angezeigte Liste"""
		if CheckpointFunktionen.checkPointsVisible:
			CheckpointFunktionen.checkPoints(False)
			CheckpointFunktionen.checkPoints(False)
		elif Notes.checkNotesVisible:
			Notes.noteView(False)
			Notes.noteView(False)
		
if __name__ == "__main__":

		oberflaeche = Oberflaeche()
