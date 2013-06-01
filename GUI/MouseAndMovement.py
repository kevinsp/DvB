import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizact

import GlobalVariables





#aktiviere/deaktiviere Mauszeiger
def enableDisableMouse(tracker, link, menubar):
		
	if viz.mouse.getVisible():
		viz.mouse(viz.ON)
		tracker.setEuler(GlobalVariables.euler)
		if (GlobalVariables.flugModus is False):
			tracker.setPosition(GlobalVariables.position[0], 1.82, GlobalVariables.position[2])
		else:
			tracker.setPosition(GlobalVariables.position)
		link.enable()
		viz.mouse.setVisible(False)
		menubar.setVisible(False)
	else:
		viz.mouse(viz.OFF)
		GlobalVariables.euler = tracker.getEuler()
		GlobalVariables.position = tracker.getPosition()
		link.disable()
		viz.mouse.setVisible(True)
		menubar.setVisible(True)
	
# Bewege in der Höhe
def moveUpAndDown(tracker, direction):
	def nachOben():
		tracker.setPosition(viz.MainView.getPosition()[0], viz.MainView.getPosition()[1]+0.2,  viz.MainView.getPosition()[2])
	def nachUnten():
		tracker.setPosition(viz.MainView.getPosition()[0], viz.MainView.getPosition()[1]-0.1,  viz.MainView.getPosition()[2])

	funktion1 = None
	funktion2 = None
	
	if GlobalVariables.variable is True and GlobalVariables.flugModus is False:
		print "test"
		vizact.removeEvent(funktion1)
		vizact.removeEvent(funktion2)
		
	if (GlobalVariables.flugModus is True):
		funktion1 = vizact.whilekeydown(viz.KEY_SHIFT_L, nachOben)
		funktion2 = vizact.whilekeydown(viz.KEY_ALT_L, nachUnten)

		if (direction is viz.KEY_SHIFT_L):
			funktion1
			GlobalVariables.variable = True
			GlobalVariables.position = tracker.getPosition()
			
		elif direction is viz.KEY_ALT_L:
			funktion2
			GlobalVariables.variable = True
			GlobalVariables.position = tracker.getPosition()

	print str(GlobalVariables.variable) +"  "+ str(GlobalVariables.flugModus)


