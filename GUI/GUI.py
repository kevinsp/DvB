"""Danke, dass Sie sich fuer unsere Software entschieden haben.
\nHier die wichtigsten Shortcuts zum bedienen des Programmes:
c:     Anzeigen der bereits gesetzten Checkpoints
n:     Anzeigen der bereits gesetzten 3D Notizen
v:     Anzeigen der Vogelperspektive
f:     Flugmodus aktivieren/deaktivieren
h:     Anzeigen dieser Hilfe
p:     Anzeigen der aktuellen Position
+ -:   Erhoehen/Verringern der Bewegungsgeschwindigkeit 1-40
* /:   Erhoehen/Verringern der Fluggeschwindigkeit 0.2-10"""



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
import SettingPanel


#viz.go(viz.QUAD_BUFFER)
viz.go()



modelIsLoaded = False
class Oberflaeche(object):
	
	def __init__(self):
		self.neu = None
		self.model = None
		self.thread = None

		viz.MainWindow.fov(60)
		viz.collision(viz.ON)
		self.beginZ = viz.MainView.getPosition()[1]

		#viz.window.setFullscreen(True)
		viz.addChild('sky_day.osgb')
		
		viz.setOption('viz.fullscreen',1)
		viz.fov(40.0,1.333)
		viz.setOption('viz.stereo', viz.QUAD_BUFFER)
		
		#Menuebar
		self.menubar = vizmenu.add()
		self.menubar.setVisible(False)

		#Model
		self.BearbeitenMenu = self.menubar.add("Model")
		self.buttonDateiOeffnen = self.BearbeitenMenu.add(viz.BUTTON_LABEL, "Datei oeffnen")
		self.buttonModelEntfernen = self.BearbeitenMenu.add(viz.BUTTON_LABEL, "Model entfernen")

		#Funktionen DropDown
		self.FunktionenMenu = self.menubar.add("Funktionen")
		self.checkPointLoeschen = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Checkpoint loeschen")
		self.checkPortButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Zu Checkpoint porten")
		self.deleteNoteButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Loesche 3D Notiz")
		self.notePortButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Zu 3D Notizen porten")
		self.beliebigPortButton = self.FunktionenMenu.add(viz.BUTTON_LABEL, "Porten")
		#Alphaslider
		self.alphaSlider = self.FunktionenMenu.add(viz.PROGRESS_BAR, "1.00", "Alphawert")
		self.alphaSlider.set(1.0)
		
		#Einfuegen DropDown
		self.EinfuegenMenu = self.menubar.add("Einfuegen")
		self.checkPointSetzen = self.EinfuegenMenu.add(viz.BUTTON_LABEL, "Checkpoint setzen")
		self.buttonNotizEinfuegen = self.EinfuegenMenu.add(viz.BUTTON_LABEL, "Notiz")

		#Optionen DropDown
		self.OptionenMenu = self.menubar.add("Optionen")
		self.AndroidAppButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Android Server")
		self.settingButton = self.OptionenMenu.add(viz.BUTTON_LABEL, "Einstellungen")




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
		self.midTextScreen = viz.addText("", viz.SCREEN)
		self.midTextScreen.setScale(0.3,0.3,0)
		self.midTextScreen.alignment(viz.ALIGN_CENTER_CENTER)
		self.midTextScreen.setPosition([0.5,0.5,0])
		self.midTextScreen.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
		self.midTextScreen.setBackdropColor([0,0,0])



		#Steuerung
		viz.mouse(viz.ON)
		viz.mouse.setTrap()
		
		GlobalVariables.tracker = vizcam.addWalkNavigate(moveScale=GlobalVariables.moveSpeed)
		GlobalVariables.tracker.setPosition([0,1.8,0])
		GlobalVariables.link = viz.link(GlobalVariables.tracker,viz.MainView)
		viz.mouse.setVisible(False)

		#Boden laden
		self.ground1 = viz.addChild('ground.osgb')
		self.ground2 = viz.addChild('ground.osgb')
		self.ground2.setPosition(0,0,50)
		
		#Begrue�ungsnachricht
		self.checkPointsPanel = vizinfo.InfoPanel(align=viz.ALIGN_CENTER,fontSize=15,icon=False,key="h")
		self.checkPointsPanel.visible(True)

		#Button Definition
		vizact.onbuttonup(self.buttonDateiOeffnen, self.setModel)
		vizact.onbuttonup(self.buttonModelEntfernen, self.deleteModel)

		#Note Buttons
		vizact.onbuttonup(self.buttonNotizEinfuegen, Notes.openTextBox, self.menubar)
		vizact.onbuttonup(self.deleteNoteButton, Notes.delete3DNote, self.menubar)
		vizact.onbuttonup(self.notePortButton, Notes.port3DNote, self.menubar)

		#Checkpoints Buttons
		vizact.onbuttonup(self.checkPointSetzen, CheckpointFunktionen.createCheckpoint, self.menubar)
		vizact.onbuttonup(self.checkPointLoeschen, CheckpointFunktionen.deleteCheckpoint, self.menubar)
		vizact.onbuttonup(self.checkPortButton, CheckpointFunktionen.portCheckPoint, self.menubar)

		#Port Button
		vizact.onbuttonup(self.beliebigPortButton, Porten.porten, self.menubar)
	
		#Optionen Buttons
		vizact.onbuttonup(self.AndroidAppButton, self.startAndroid)
		vizact.onbuttonup(self.settingButton, SettingPanel.oeffneSettingPanel, self.menubar)
	
		#Shortcuts
		vizact.onkeydown(viz.KEY_CONTROL_L, MouseAndMovement.enableDisableMouse, self.menubar)
		vizact.onkeydown("c", CheckpointFunktionen.checkPoints, False)
		vizact.onkeydown("v", BirdView.enableBirdEyeView)
		vizact.onkeydown("n", Notes.noteView, False)
		vizact.onkeydown("f", self.flugModusOnOff)
		vizact.onkeydown("p", self.zeigePosition)
		vizact.onkeydown(viz.KEY_KP_ADD, self.speedUp)
		vizact.onkeydown(viz.KEY_KP_SUBTRACT, self.speedDown)
		vizact.onkeydown(viz.KEY_KP_DIVIDE, self.flySpeedDown)
		vizact.onkeydown(viz.KEY_KP_MULTIPLY, self.flySpeedUp)
	
		#Hoch und runter
		vizact.onkeydown(viz.KEY_SHIFT_L, MouseAndMovement.moveUpAndDown,  viz.KEY_SHIFT_L)
		vizact.onkeydown(viz.KEY_ALT_L, MouseAndMovement.moveUpAndDown, viz.KEY_ALT_L)
		
		#Progressbar Alphawert
		vizact.onslider( self.alphaSlider, self.setAlpha )
	
	#Setze Alphawert
	def setAlpha(self, slider):
		if self.model is not None:
			self.alphaSlider.message( str('%.2f'%(slider)) )
			self.model.alpha(slider)
	
	def startAndroid(self):
		if GlobalVariables.serverIsRunning is False: #starte nur einen Server, wenn noch keiner laeuft
			self.ipTextScreen.message(str(viz.net.getIP()))
			self.neu = RemoteAppMain.RemoteAppLuncher(str(viz.net.getIP()), GlobalVariables.tracker, GlobalVariables.checkPointsList)
			self.thread = viz.director(self.neu.lunch)
			GlobalVariables.serverIsRunning = True
		else:
			GlobalVariables.serverIsRunning = False
			self.ipTextScreen.message("")
			self.neu.shutdown() #beende Server
			
		

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
			#GlobalVariables.tracker.setPosition(viz.MainView.getPosition()[0], self.beginZ, viz.MainView.getPosition()[2])
			self.midTextScreen.message("Flugmodus: OFF")
			vizact.ontimer2(1, 0, self.midTextScreen.message, "")
			
		else:
			GlobalVariables.flugModus = True
			#GlobalVariables.tracker.setPosition(viz.MainView.getPosition()[0], 1.82, viz.MainView.getPosition()[2])
			viz.collision(viz.OFF)
			self.midTextScreen.message("Flugmodus: ON")
			vizact.ontimer2(1, 0, self.midTextScreen.message, "")

	#erh�he bewegugnsgeschwindigkeit
	def speedUp(self):
		if(GlobalVariables.moveSpeed<40):
			GlobalVariables.moveSpeed += 1
			position = viz.MainView.getPosition()
			euler = viz.MainView.getEuler()
			GlobalVariables.tracker.remove()
			GlobalVariables.tracker = vizcam.addWalkNavigate(moveScale=GlobalVariables.moveSpeed)
			GlobalVariables.link = viz.link(GlobalVariables.tracker, viz.MainView)
			GlobalVariables.tracker.setPosition(position)
			GlobalVariables.tracker.setEuler(euler)
			self.midTextScreen.message("Geschwindigkeit: " + str(GlobalVariables.moveSpeed))
			vizact.ontimer2(1, 0, self.midTextScreen.message, "")
			viz.postEvent(viz.getEventID("VIEW_CHANGED_EVENT"), GlobalVariables.tracker)		
			
	#verringere bewegeungsgeschwindigkeit
	def speedDown(self):		
		if(GlobalVariables.moveSpeed>1):
			GlobalVariables.moveSpeed -=1
			position = viz.MainView.getPosition()
			euler = viz.MainView.getEuler()
			GlobalVariables.tracker.remove()
			GlobalVariables.tracker = vizcam.addWalkNavigate(moveScale=GlobalVariables.moveSpeed)
			GlobalVariables.link = viz.link(GlobalVariables.tracker, viz.MainView)
			GlobalVariables.tracker.setPosition(position)
			GlobalVariables.tracker.setEuler(euler)
			self.midTextScreen.message("Geschwindigkeit: " + str(GlobalVariables.moveSpeed))
			vizact.ontimer2(1, 0, self.midTextScreen.message, "")
			viz.postEvent(viz.getEventID("VIEW_CHANGED_EVENT"), GlobalVariables.tracker)		

	#erh�he Fluggeschwindigkeit
	def flySpeedUp(self):
		if GlobalVariables.flySpeed <=9.8:
			GlobalVariables.flySpeed +=0.2
		self.midTextScreen.message("Fluggeschwindigkeit: " + str(GlobalVariables.flySpeed))
		vizact.ontimer2(1, 0, self.midTextScreen.message, "")
		
	#verringere Fluggeschwindigkeit
	def flySpeedDown(self):
		if GlobalVariables.flySpeed>0.2:
			GlobalVariables.flySpeed -=0.2
		self.midTextScreen.message("Fluggeschwindigkeit: " + str(GlobalVariables.flySpeed))
		vizact.ontimer2(1, 0, self.midTextScreen.message, "")
		
if __name__ == "__main__":

		oberflaeche = Oberflaeche()
