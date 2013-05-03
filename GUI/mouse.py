import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizact




#aktiviere/deaktiviere Mauszeiger
def enableDisableMouse(tracker, link, menubar):
	global euler
	global position
	if viz.mouse.getVisible():
		tracker.setEuler(euler)
		tracker.setPosition(position)
		link.enable()
		viz.mouse.setVisible(False)
		menubar.setVisible(False)
	else:
		euler = tracker.getEuler()
		position = tracker.getPosition()
		link.disable()
		viz.mouse.setVisible(True)
		menubar.setVisible(True)
	