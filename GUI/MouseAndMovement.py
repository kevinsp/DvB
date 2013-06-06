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
def moveUpAndDown(direction):

	def nachOben():
		if GlobalVariables.flugModus is True:			
			GlobalVariables.tracker.setPosition(viz.MainView.getPosition()[0], viz.MainView.getPosition()[1]+GlobalVariables.flySpeed,  viz.MainView.getPosition()[2])
			GlobalVariables.position = GlobalVariables.tracker.getPosition()

	def nachUnten():
		if GlobalVariables.flugModus is True:
			GlobalVariables.tracker.setPosition(viz.MainView.getPosition()[0], viz.MainView.getPosition()[1]-GlobalVariables.flySpeed,  viz.MainView.getPosition()[2])
			GlobalVariables.position = GlobalVariables.tracker.getPosition()

	vizact.whilekeydown(viz.KEY_SHIFT_L, nachOben)
	vizact.whilekeydown(viz.KEY_ALT_L, nachUnten)
	



