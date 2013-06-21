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
	GlobalVariables.direction = direction

	def bewege():
		if GlobalVariables.flugModus is True and GlobalVariables.direction is viz.KEY_SHIFT_L:			
			GlobalVariables.tracker.setPosition(GlobalVariables.tracker.getPosition()[0], GlobalVariables.tracker.getPosition()[1]+GlobalVariables.flySpeed,  GlobalVariables.tracker.getPosition()[2])
			GlobalVariables.position = GlobalVariables.tracker.getPosition()
		elif GlobalVariables.flugModus is True and GlobalVariables.direction is viz.KEY_ALT_L:
			GlobalVariables.tracker.setPosition(GlobalVariables.tracker.getPosition()[0],GlobalVariables.tracker.getPosition()[1]-GlobalVariables.flySpeed,  GlobalVariables.tracker.getPosition()[2])
			GlobalVariables.position = GlobalVariables.tracker.getPosition()

	if GlobalVariables.flugEinmalGesetzt is False:
		vizact.whilekeydown(viz.KEY_SHIFT_L, bewege)
		vizact.whilekeydown(viz.KEY_ALT_L, bewege)
		GlobalVariables.flugEinmalGesetzt = True
	



