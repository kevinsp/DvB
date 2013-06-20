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
def enableDisableMouse(menubar):
		
	if viz.mouse.getVisible():
		viz.mouse(viz.ON)
		GlobalVariables.tracker.setEuler(GlobalVariables.euler)
		GlobalVariables.tracker.setPosition(GlobalVariables.position)
		GlobalVariables.link.enable()
		viz.mouse.setVisible(False)
		menubar.setVisible(False)
	else:
		viz.mouse(viz.OFF)
		GlobalVariables.euler = GlobalVariables.tracker.getEuler()
		GlobalVariables.position = GlobalVariables.tracker.getPosition()
		GlobalVariables.link.disable()
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
	



