import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask

#Eigene Module
import checkpoints
import notes
import mouse
import birdView


modelIsLoaded = False

viz.MainWindow.fov(60)

#Menübar
menubar = vizmenu.add()
menubar.setVisible(False)

#Bearbeiten
BearbeitenMenu = menubar.add("Bearbeiten")
buttonDateiOeffnen = BearbeitenMenu.add(viz.BUTTON_LABEL, "Datei öffnen")
buttonModelEntfernen = BearbeitenMenu.add(viz.BUTTON_LABEL, "Model entfernen")

#Ansicht DropDown
AnsichtsMenu = menubar.add("Ansicht")
checkRohre = AnsichtsMenu.add(viz.CHECKBOX, "Rohre")
checkWaende = AnsichtsMenu.add(viz.CHECKBOX, "Wände")
checkBirdEyeView = AnsichtsMenu.add(viz.CHECKBOX, "Vogelperspektive")
checkPointsView = AnsichtsMenu.add(viz.CHECKBOX, "Checkpoints")
checkPointSetzen = AnsichtsMenu.add(viz.BUTTON_LABEL, "Checkpoint setzen")
checkPointLoeschen = AnsichtsMenu.add(viz.BUTTON_LABEL, "Checkpoint löschen")
checkPportButton = AnsichtsMenu.add(viz.BUTTON_LABEL, "Zu Checkpoints porten")
noteViewButton = AnsichtsMenu.add(viz.CHECKBOX, "Notizen")
deleteNoteButton = AnsichtsMenu.add(viz.BUTTON_LABEL, "Lösche 3D Notiz")
notePortButton = AnsichtsMenu.add(viz.BUTTON_LABEL, "Zu 3D Notizen porten")



#Einfügen DropDown
EinfuegenMenu = menubar.add("Einfügen")
buttonNotizEinfuegen = EinfuegenMenu.add(viz.BUTTON_LABEL, "Notiz")

#Optionen DropDown
OptionenMenu = menubar.add("Optionen")

#Alphawert
alphaSlider = AnsichtsMenu.add(viz.SLIDER, "Alphawert")
alphaSlider.set(1.0)

#Steuerung
viz.mouse(viz.OFF)
viz.mouse.setTrap()
tracker = vizcam.addWalkNavigate(moveScale=2.0)
tracker.setPosition([0,1.8,0])
link = viz.link(tracker,viz.MainView)
viz.mouse.setVisible(False)


#Erstes Model laden
model = viz.addChild(r'C:\Users\pasca_000\Downloads\CADModellHofner.obj')
modelIsLoaded = True
model.disable(viz.CULL_FACE)
model.setPosition(0,0,60, viz.ABS_GLOBAL)
model.setEuler([0,0,0])
viz.collision(viz.ON)

#Boden laden
ground1 = viz.addChild('ground.osgb')
ground2 = viz.addChild('ground.osgb')
ground2.setPosition(0,0,50)

#Bekomme Slider Position
def sliderPosition(slider):
	return slider.get()
	
#Setze Alphawert
def setAlpha(slider):
	alpha = sliderPosition(slider)
	model.alpha(alpha)
	
#Lade neues Model
def setModel (path):
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
def deleteModel():
	global modelIsLoaded
	model.remove()
	modelIsLoaded = False


		
#Button Definition
vizact.onbuttondown(buttonDateiOeffnen, setModel, r'C:\Users\pasca_000\Downloads\CADModellHofner.obj' )
vizact.onbuttondown(buttonModelEntfernen, deleteModel)

#Note Buttons
vizact.onbuttondown(buttonNotizEinfuegen, notes.openTextBox)
vizact.onbuttondown(noteViewButton, notes.noteView)
vizact.onbuttonup(noteViewButton, notes.noteView)
vizact.onbuttondown(deleteNoteButton, notes.delete3DNote)
vizact.onbuttondown(notePortButton, notes.port3DNote, tracker)

#BirdEyeView Buttons
vizact.onbuttondown(checkBirdEyeView, birdView.enableBirdEyeView)
vizact.onbuttonup(checkBirdEyeView, birdView.enableBirdEyeView)

#Checkpoints Buttons
vizact.onbuttondown(checkPointsView, checkpoints.checkPoints)
vizact.onbuttonup(checkPointsView, checkpoints.checkPoints)
vizact.onbuttondown(checkPointSetzen, checkpoints.createCheckpoint)
vizact.onbuttondown(checkPointLoeschen, checkpoints.deleteCheckpoint)
vizact.onbuttondown(checkPportButton, checkpoints.portCheckPoint, tracker)


#Shortcuts
vizact.onkeydown(viz.KEY_CONTROL_L, mouse.enableDisableMouse, tracker, link, menubar)

#Alphawert aktualisieren
vizact.ontimer(0.1, setAlpha, alphaSlider )

viz.go()
