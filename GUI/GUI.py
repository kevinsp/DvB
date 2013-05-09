# -*- coding: utf-8 -*-
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

#Eigene Module
import checkpoints
import notes
import mouse
import birdView
import porten


#viz.go(viz.FULLSCREEN) 
viz.go()

modelIsLoaded = False
mouseMode = False

class Oberflaeche(object):
	
	def __init__(self):
		#viz.window.setFullscreen(True)

		viz.MainWindow.fov(60)
		#viz.window.setFullscreen(True)


		#Popups
		fullscreenItem = vizpopup.Item('Fullscreen')

		mymenu = vizpopup.Menu('Main',[fullscreenItem])



		#Bei Rechtklick Menüaufruf
		vizact.onmouseup(viz.MOUSEBUTTON_RIGHT, self.showMenu)

		#Fullscreen on/off
		vizpopup.onMenuItem(fullscreenItem,viz.window.setFullscreen,viz.TOGGLE)


		#Menübar
		self.menubar = vizmenu.add()
		self.menubar.setVisible(False)

		#Bearbeiten
		self.BearbeitenMenu = self.menubar.add("Bearbeiten")
		self.buttonDateiOeffnen = self.BearbeitenMenu.add(viz.BUTTON_LABEL, "Datei öffnen")
		self.buttonModelEntfernen = self.BearbeitenMenu.add(viz.BUTTON_LABEL, "Model entfernen")

		#Ansicht DropDown
		self.AnsichtsMenu = self.menubar.add("Ansicht")
		self.checkRohre = self.AnsichtsMenu.add(viz.CHECKBOX, "Rohre")
		self.checkWaende = self.AnsichtsMenu.add(viz.CHECKBOX, "Wände")
		self.checkBirdEyeView = self.AnsichtsMenu.add(viz.CHECKBOX, "Vogelperspektive")
		self.checkPointsView = self.AnsichtsMenu.add(viz.CHECKBOX, "Checkpoints")
		self.checkPointSetzen = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Checkpoint setzen")
		self.checkPointLoeschen = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Checkpoint löschen")
		self.checkPortButton = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Zu Checkpoints porten")
		self.noteViewButton = self.AnsichtsMenu.add(viz.CHECKBOX, "Notizen")
		self.deleteNoteButton = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Lösche 3D Notiz")
		self.notePortButton = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Zu 3D Notizen porten")
		self.beliebigPortButton = self.AnsichtsMenu.add(viz.BUTTON_LABEL, "Porten")

		#Einfügen DropDown
		self.EinfuegenMenu = self.menubar.add("Einfügen")
		self.buttonNotizEinfuegen = self.EinfuegenMenu.add(viz.BUTTON_LABEL, "Notiz")

		#Optionen DropDown
		self.OptionenMenu = self.menubar.add("Optionen")

		#Alphawert
		self.alphaSlider = self.AnsichtsMenu.add(viz.SLIDER, "Alphawert")
		self.alphaSlider.set(1.0)

		#Steuerung
		viz.mouse(viz.ON)
		viz.mouse.setTrap()
		self.tracker = vizcam.addWalkNavigate(moveScale=2.0)
		self.tracker.setPosition([0,1.8,0])
		self.link = viz.link(self.tracker,viz.MainView)
		viz.mouse.setVisible(False)


		#Erstes Model laden
		self.model = viz.addChild(r'C:\Users\pasca_000\Downloads\CADModellHofner.obj')
		modelIsLoaded = True
		self.model.disable(viz.CULL_FACE)
		self.model.setPosition(0,0,60, viz.ABS_GLOBAL)
		self.model.setEuler([0,0,0])
		viz.collision(viz.ON)

		#Boden laden
		self.ground1 = viz.addChild('ground.osgb')
		self.ground2 = viz.addChild('ground.osgb')
		self.ground2.setPosition(0,0,50)
		
		#Begrüßungsnachricht
		message = """Danke, dass Sie sich für unsere Software entschieden haben.
		\nHier die wichtigsten Shortcuts zum bedienen des Programmes:
		C:   Anzeigen der bereits gesetzten Checkpoints
		N:   Anzeigen der bereits gesetzten 3D Notizen
		V:   Anzeigen der Vogelperspektive
		H:   Anzeigen dieser Hilfe"""
		checkPointsPanel = vizinfo.InfoPanel(message,align=viz.ALIGN_CENTER,fontSize=15,icon=False,key="h")
		checkPointsPanel.visible(True)
		
		
		#Button Definition
		vizact.onbuttondown(self.buttonDateiOeffnen, self.setModel, r'C:\Users\pasca_000\Downloads\CADModellHofner.obj' )
		vizact.onbuttondown(self.buttonModelEntfernen, self.deleteModel)

		#Note Buttons
		vizact.onbuttondown(self.buttonNotizEinfuegen, notes.openTextBox)
		vizact.onbuttondown(self.noteViewButton, notes.noteView, False)
		vizact.onbuttonup(self.noteViewButton, notes.noteView, False)
		vizact.onbuttondown(self.deleteNoteButton, notes.delete3DNote)
		vizact.onbuttondown(self.notePortButton, notes.port3DNote, self.tracker)

		#BirdEyeView Buttons
		vizact.onbuttondown(self.checkBirdEyeView, birdView.enableBirdEyeView)
		vizact.onbuttonup(self.checkBirdEyeView, birdView.enableBirdEyeView)

		#Checkpoints Buttons
		vizact.onbuttondown(self.checkPointsView, checkpoints.checkPoints, False)
		vizact.onbuttonup(self.checkPointsView, checkpoints.checkPoints, False)
		vizact.onbuttondown(self.checkPointSetzen, checkpoints.createCheckpoint)
		vizact.onbuttondown(self.checkPointLoeschen, checkpoints.deleteCheckpoint)
		vizact.onbuttondown(self.checkPortButton, checkpoints.portCheckPoint, self.tracker)

		#Port Button
		vizact.onbuttondown(self.beliebigPortButton, porten.porten, self.tracker)
	
		#Shortcuts
		vizact.onkeydown(viz.KEY_CONTROL_L, mouse.enableDisableMouse, self.tracker, self.link, self.menubar)
		vizact.onkeydown("c", checkpoints.checkPoints, False)
		vizact.onkeydown("v", birdView.enableBirdEyeView)
		vizact.onkeydown("n", notes.noteView, False)


	
	#Bekomme Slider Position
	def sliderPosition(self, slider):
		return slider.get()
			
	#Setze Alphawert
	def setAlpha(self, slider):
		self.alpha = self.sliderPosition(slider)
		model.alpha(alpha)
			
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
			
	#Lösche Model		
	def deleteModel(self):
		global modelIsLoaded
		model.remove()
		modelIsLoaded = False
	"""		
	#Setze MausModus
	def setMouseMode(self):
		global mouseMode
		if (mouseMode is False):
			mouseMode = True
		else:
			mouseMode = False
	"""		
		
		
	#Zeige Menü
	def showMenu(self):
		if (mouseMode is True):
			fullscreenItem.checked = viz.window.getFullscreen()
			vizpopup.display(mymenu)

if __name__ == "__main__":
		oberflaeche = Oberflaeche()
