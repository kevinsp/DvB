"""Danke, dass Sie sich für unsere Software entschieden haben.
\nHier die wichtigsten Shortcuts zum bedienen des Programmes:
c:   Anzeigen der bereits gesetzten Checkpoints
n:   Anzeigen der bereits gesetzten 3D Notizen
v:   Anzeigen der Vogelperspektive
f:   Flugmodus aktivieren/deaktivieren
h:   Anzeigen dieser Hilfe
p:   Anzeigend er aktuellen Position"""



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

import sys
sys.path.append(r"..\RemoteAppServer")
from RemoteAppMain import RemoteAppLuncher

#Eigene Module
import CheckpointFunktionen
import Notes
import MouseAndMovement
import BirdView
import Porten
import RemoteAppMain
import GlobalVariables
#from RemoteAppMain import RemoteAppLuncher




#viz.go(viz.FULLSCREEN) 
viz.go()



modelIsLoaded = False

class Oberflaeche(object):
	
	def __init__(self):
		
		viz.MainWindow.fov(60)
		viz.collision(viz.ON)
		self.beginZ = viz.MainView.getPosition()[1]

		#viz.window.setFullscreen(True)
		viz.addChild('sky_day.osgb')
		
		
		#Menübar
		self.menubar = vizmenu.add()
		self.menubar.setVisible(False)

		#Bearbeiten
		self.BearbeitenMenu = self.menubar.add("Bearbeiten")
		self.buttonDateiOeffnen = self.BearbeitenMenu.add(viz.BUTTON_LABEL, "Datei öffnen")
		self.buttonModelEntfernen = self.BearbeitenMenu.add(viz.BUTTON_LABEL, "Model entfernen")

		#Ansicht DropDown
		self.AnsichtsMenu = self.menubar.add("Ansicht")
		self.checkPointSetzen = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Checkpoint setzen")
		self.checkPointLoeschen = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Checkpoint löschen")
		self.checkPortButton = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Zu Checkpoint porten")
		self.deleteNoteButton = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Lösche 3D Notiz")
		self.notePortButton = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Zu 3D Notizen porten")
		self.beliebigPortButton = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Porten")

		#EinfÃ¼gen DropDown
		self.EinfuegenMenu = self.menubar.add("Einfügen")
		self.buttonNotizEinfuegen = self.EinfuegenMenu.add(viz.BUTTON_LABEL, "Notiz")

		#Optionen DropDown
		self.OptionenMenu = self.menubar.add("Optionen")
		self.AndroidAppButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Android")

		#Alphaslider
		self.alphaSlider = self.AnsichtsMenu.add(viz.PROGRESS_BAR, "1.00", "Alphawert")
		self.alphaSlider.set(1.0)


		#Theme
		viz.setTheme(GlobalVariables.darkTheme)

		
		#Positionsangabe
		self.textScreen = viz.addText('',viz.SCREEN) 
		self.textScreen.setScale(0.3,0.3,0)
		self.textScreen.alignment(viz.ALIGN_RIGHT_TOP)
		self.textScreen.setPosition([0.99,0.787,0])
		self.textScreen.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
		self.textScreen.setBackdropColor([0,0,0])
		
		#IP-Angabe
		self.ipTextScreen = viz.addText("", viz.SCREEN)
		self.ipTextScreen.setScale(0.3,0.3,0)
		self.ipTextScreen.alignment(viz.ALIGN_RIGHT_TOP)
		self.ipTextScreen.setPosition([0.79,0.99,0])
		self.ipTextScreen.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
		self.ipTextScreen.setBackdropColor([0,0,0])
		
		#Flugmodus angabe
		self.flugModusTextScreen = viz.addText("", viz.SCREEN)
		self.flugModusTextScreen.setScale(0.3,0.3,0)
		self.flugModusTextScreen.alignment(viz.ALIGN_RIGHT_TOP)
		self.flugModusTextScreen.setPosition([0.99,0.75,0])
		self.flugModusTextScreen.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
		self.flugModusTextScreen.setBackdropColor([0,0,0])
		
		""" lieber panel oder textscreen???
		self.checkPointTextScreen = viz.addText("Checkpoints:\n", viz.SCREEN)
		self.checkPointTextScreen.setScale(0.3,0.3,0)
		self.checkPointTextScreen.alignment(viz.ALIGN_LEFT_CENTER)
		self.checkPointTextScreen.setPosition([0.85,0.5,0])

		self.checkPointTextScreen.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
		self.checkPointTextScreen.setBackdropColor([0,0,0])
		self.checkPointTextScreen.visible(True)
		"""


		#Steuerung
		viz.mouse(viz.ON)
		viz.mouse.setTrap()
		
		self.tracker = vizcam.addWalkNavigate(moveScale=2.0)
		self.tracker.setPosition([0,1.8,0])
		self.link = viz.link(self.tracker,viz.MainView)
		viz.mouse.setVisible(False)
		
		

		"""
		#Erstes Model laden
		self.model = viz.addChild(r'C:\Users\pasca_000\Downloads\CADModellHofner(1).obj')
		modelIsLoaded = True
		self.model.disable(viz.CULL_FACE)
		self.model.setPosition(0,0,60, viz.ABS_GLOBAL)
		self.model.setEuler([0,0,0])
		"""

		#Boden laden
		self.ground1 = viz.addChild('ground.osgb')
		self.ground2 = viz.addChild('ground.osgb')
		self.ground2.setPosition(0,0,50)
		
		#Begrueßungsnachricht
		self.checkPointsPanel = vizinfo.InfoPanel(align=viz.ALIGN_CENTER,fontSize=15,icon=False,key="h")
		self.checkPointsPanel.visible(True)

		
		#Button Definition
		vizact.onbuttondown(self.buttonDateiOeffnen, self.setModel)
		vizact.onbuttondown(self.buttonModelEntfernen, self.deleteModel)

		#Note Buttons
		vizact.onbuttondown(self.buttonNotizEinfuegen, Notes.openTextBox, self.menubar)
		vizact.onbuttondown(self.deleteNoteButton, Notes.delete3DNote, self.menubar)
		vizact.onbuttondown(self.notePortButton, Notes.port3DNote, self.tracker, self.menubar)

		#Checkpoints Buttons
		vizact.onbuttondown(self.checkPointSetzen, CheckpointFunktionen.createCheckpoint, self.menubar)
		vizact.onbuttondown(self.checkPointLoeschen, CheckpointFunktionen.deleteCheckpoint, self.menubar)
		vizact.onbuttondown(self.checkPortButton, CheckpointFunktionen.portCheckPoint, self.tracker, self.menubar)

		#Port Button
		vizact.onbuttondown(self.beliebigPortButton, Porten.porten, self.tracker, self.menubar)
		
	
		#Optionen Buttons
		#neu = RemoteAppMain.RemoteAppLuncher("141.82.171.254", self.tracker)
		#viz.director(neu.lunch)
		vizact.onbuttondown(self.AndroidAppButton, self.startAndroid)
	
		#Shortcuts
		vizact.onkeydown(viz.KEY_CONTROL_L, MouseAndMovement.enableDisableMouse, self.tracker, self.link, self.menubar)
		vizact.onkeydown("c", CheckpointFunktionen.checkPoints, False)
		vizact.onkeydown("v", BirdView.enableBirdEyeView)
		vizact.onkeydown("n", Notes.noteView, False)
		vizact.onkeydown("f", self.flugModusOnOff)
		vizact.onkeydown("p", self.zeigePosition)
	
		#Hoch und runter
	
		vizact.onkeydown(viz.KEY_SHIFT_L, MouseAndMovement.moveUpAndDown, self.tracker,  viz.KEY_SHIFT_L)
		vizact.onkeydown(viz.KEY_ALT_L, MouseAndMovement.moveUpAndDown, self.tracker, viz.KEY_ALT_L)
		#Slider
		vizact.onslider( self.alphaSlider, self.setAlpha )

		
	
	#Setze Alphawert
	def setAlpha(self, slider):
		self.alphaSlider.message( str('%.2f'%(slider)) )
		self.model.alpha(slider)
	
	def startAndroid(self):
		self.ipTextScreen.message(str(viz.net.getIP()))
		
		if (GlobalVariables.showIP is False):
			self.ipTextScreen.visible(True)
			GlobalVariables.showIP = True
		else:
			self.ipTextScreen.visible(False)
			GlobalVariables.showIP = False
		
	#	neu = RemoteAppMain.RemoteAppLuncher(viz.net.getIP, self.tracker)
	#	viz.director(neu.lunch)

	#zeige zurzeitige position
	def zeigePosition(self):
		def changeMessage():
			userPosition = viz.MainView.getPosition() #Frage User Position
			message = str(round(userPosition[0],2)) + " " + str(round(userPosition[1],2)) + " " + str(round(userPosition[2],2))
			self.textScreen.message(str(message))
		
		if (GlobalVariables.showPosi is False):
			self.textScreen.visible(True)
			GlobalVariables.showPosi = True
			vizact.ontimer(0.1, changeMessage)
		else:
			self.textScreen.visible(False)
			GlobalVariables.showPosi = False
		
	#Lade neues Model
	def setModel (self):
		global modelIsLoaded
		if not (modelIsLoaded):
			self.alphaSlider.set(1.0)
			self.model = viz.addChild(vizinput.fileOpen())
			self.model.disable(viz.CULL_FACE)
			self.model.setPosition(0,0,60, viz.ABS_GLOBAL)
			self.model.setEuler([0,0,0])
			viz.collision(viz.ON)

			modelIsLoaded = True
			
	#Loesche Model		
	def deleteModel(self):
		global modelIsLoaded
		self.model.remove()
		modelIsLoaded = False
			
	#FlugmodusOnOFF
	def flugModusOnOff(self):
		if (GlobalVariables.flugModus is True):
			GlobalVariables.flugModus = False
			viz.collision(viz.ON)
			GlobalVariables.position = viz.MainView.getPosition()
			self.tracker.setPosition(viz.MainView.getPosition()[0], self.beginZ, viz.MainView.getPosition()[2])
			
		else:
			GlobalVariables.flugModus = True
			#self.tracker.setPosition(viz.MainView.getPosition()[0], 1.82, viz.MainView.getPosition()[2])
			viz.collision(viz.OFF)
		self.flugModusTextScreen.message("Flugmodus: " + str(GlobalVariables.flugModus))

if __name__ == "__main__":

		oberflaeche = Oberflaeche()
