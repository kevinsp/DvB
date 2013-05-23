"""Danke, dass Sie sich für unsere Software entschieden haben.
\nHier die wichtigsten Shortcuts zum bedienen des Programmes:
c:   Anzeigen der bereits gesetzten Checkpoints
n:   Anzeigen der bereits gesetzten 3D Notizen
v:   Anzeigen der Vogelperspektive
f:   Flugmodus aktivieren/deaktivieren
h:   Anzeigen dieser Hilfe"""



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


#from ..RemoteAppServer.RemoteAppMain import RemoteAppLuncher

#Eigene Module
import Checkpoints
import Notes
import MouseAndMovement
import BirdView
import Porten
import RemoteAppMain
import GlobalVariables
from RemoteAppMain import RemoteAppLuncher




#viz.go(viz.FULLSCREEN) 
viz.go()



modelIsLoaded = False
mouseMode = False

class Oberflaeche(object):
	
	def __init__(self):
		
		viz.MainWindow.fov(60)
		#viz.window.setFullscreen(True)
		viz.addChild('sky_day.osgb')
		
		neu = RemoteAppMain.RemoteAppLuncher("188.174.41.93")
		
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



		#Steuerung
		viz.mouse(viz.ON)
		viz.mouse.setTrap()
		self.tracker = vizcam.addWalkNavigate(moveScale=2.0)
		self.tracker.setPosition([0,1.8,0])
		self.link = viz.link(self.tracker,viz.MainView)
		viz.mouse.setVisible(False)


		#Erstes Model laden
		self.model = viz.addChild(r'C:\Users\pasca_000\Downloads\CADModellHofner(1).obj')
		modelIsLoaded = True
		self.model.disable(viz.CULL_FACE)
		self.model.setPosition(0,0,60, viz.ABS_GLOBAL)
		self.model.setEuler([0,0,0])
		viz.collision(viz.ON)

		#Boden laden
		self.ground1 = viz.addChild('ground.osgb')
		self.ground2 = viz.addChild('ground.osgb')
		self.ground2.setPosition(0,0,50)
		
		#BegrÃ¼ÃŸungsnachricht
		self.checkPointsPanel = vizinfo.InfoPanel(align=viz.ALIGN_CENTER,fontSize=15,icon=False,key="h")
		self.checkPointsPanel.visible(True)

		
		#Button Definition
		vizact.onbuttondown(self.buttonDateiOeffnen, self.setModel, r'C:\Users\pasca_000\Downloads\CADModellHofner(1).obj' )
		vizact.onbuttondown(self.buttonModelEntfernen, self.deleteModel)

		#Note Buttons
		vizact.onbuttondown(self.buttonNotizEinfuegen, Notes.openTextBox, self.menubar)
		vizact.onbuttondown(self.deleteNoteButton, Notes.delete3DNote, self.menubar)
		vizact.onbuttondown(self.notePortButton, Notes.port3DNote, self.tracker, self.menubar)

		#Checkpoints Buttons
		vizact.onbuttondown(self.checkPointSetzen, Checkpoints.createCheckpoint, self.menubar)
		vizact.onbuttondown(self.checkPointLoeschen, Checkpoints.deleteCheckpoint, self.menubar)
		vizact.onbuttondown(self.checkPortButton, Checkpoints.portCheckPoint, self.tracker, self.menubar)

		#Port Button
		vizact.onbuttondown(self.beliebigPortButton, Porten.porten, self.tracker, self.menubar)
		
	
		#Optionen Buttons
		
		#vizact.onbuttondown(self.AndroidAppButton, neu.lunch)
		viz.director(neu.lunch)
	
		#Shortcuts
		vizact.onkeydown(viz.KEY_CONTROL_L, MouseAndMovement.enableDisableMouse, self.tracker, self.link, self.menubar)
		vizact.onkeydown("c", Checkpoints.checkPoints, False)
		vizact.onkeydown("v", BirdView.enableBirdEyeView)
		vizact.onkeydown("n", Notes.noteView, False)
		vizact.onkeydown("f", self.flugModusOnOff)
	
		#Hoch und runter
		vizact.onkeydown(viz.KEY_SHIFT_L,self.hochUndRunter, self.tracker,  viz.KEY_SHIFT_L)
		vizact.onkeydown(viz.KEY_ALT_L, self.hochUndRunter, self.tracker, viz.KEY_ALT_L)

		#Slider
		vizact.onslider( self.alphaSlider, self.setAlpha )

	
	#Bekomme Slider Position
	def sliderPosition(self, slider):
		return slider.get()
			
	#Setze Alphawert
	def setAlpha(self, slider):
		#self.alpha = self.sliderPosition(slider)
		self.alphaSlider.message( str('%.2f'%(slider)) )
		#ball2.alpha( sliderPOS )
		self.model.alpha(slider)


			
	#Lade neues Model
	def setModel (self, path):
		global model
		global modelIsLoaded
		if not (modelIsLoaded):
			model = viz.addChild(path)
			model.disable(viz.CULL_FACE)
			model.setPosition(0,0,60, viz.ABS_GLOBAL)
			model.setEuler([0,0,0])
			alphaSlider.set(1.0)
			modelIsLoaded = True
			
	#LÃ¶sche Model		
	def deleteModel(self):
		global modelIsLoaded
		model.remove()
		modelIsLoaded = False

	#Hoch und Runter
	def hochUndRunter(self, tracker, direction):
		if (GlobalVariables.flugModus is True):
			MouseAndMovement.moveUpAndDown(tracker, direction)
		else:
			pass
			
	#FlugmodusOnOFF
	def flugModusOnOff(self):
		if (GlobalVariables.flugModus is True):
			GlobalVariables.flugModus = False
			viz.collision(viz.ON)
			GlobalVariables.position = viz.MainView.getPosition()
			self.tracker.setPosition(viz.MainView.getPosition()[0], 1.82, viz.MainView.getPosition()[2])
			
		else:
			GlobalVariables.flugModus = True
			self.tracker.setPosition(viz.MainView.getPosition()[0], 1.82, viz.MainView.getPosition()[2])
			viz.collision(viz.OFF)

if __name__ == "__main__":

		oberflaeche = Oberflaeche()
