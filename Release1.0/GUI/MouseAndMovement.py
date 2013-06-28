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





def enableDisableMouse(menubar):
        """aktiviere/deaktiviere Mauszeiger"""

	#"""Falls die Maus sichtbar ist, mache unsichtbar und aktiviere die Steuerung der Kamera durch die Maus	"""
	if viz.mouse.getVisible():
		viz.mouse(viz.ON)
		GlobalVariables.tracker.setEuler(GlobalVariables.euler)
		GlobalVariables.tracker.setPosition(GlobalVariables.position)
		GlobalVariables.link.enable()
		viz.mouse.setVisible(False)
		#"""Verstecke menubar"""
		menubar.setVisible(False)
		
	#"""Falls die Maus unsichtbar ist, mache sichtbar und deaktiviere die Steuerung der Kamera durch die Maus"""
	else:
		viz.mouse(viz.OFF)
		GlobalVariables.euler = GlobalVariables.tracker.getEuler()
		GlobalVariables.position = GlobalVariables.tracker.getPosition()
		GlobalVariables.link.disable()
		viz.mouse.setVisible(True)
		#"""Zeige menubar"""
		menubar.setVisible(True)
	

def moveUpAndDown(direction):
        """Fliege hoch oder runter"""
        
	GlobalVariables.direction = direction
	
	def bewege():
                
                #"""Hoch fliegen bei aktiven Flugmodus und linker Shift Taste"""
		if GlobalVariables.flugModus is True and GlobalVariables.direction is viz.KEY_SHIFT_L:			
			GlobalVariables.tracker.setPosition(GlobalVariables.tracker.getPosition()[0], GlobalVariables.tracker.getPosition()[1]+GlobalVariables.flySpeed,  GlobalVariables.tracker.getPosition()[2])
			GlobalVariables.position = GlobalVariables.tracker.getPosition()

		#"""Runter fliegen bei aktiven Flugmodus und linker ALT Taste"""
		elif GlobalVariables.flugModus is True and GlobalVariables.direction is viz.KEY_ALT_L:
			GlobalVariables.tracker.setPosition(GlobalVariables.tracker.getPosition()[0],GlobalVariables.tracker.getPosition()[1]-GlobalVariables.flySpeed,  GlobalVariables.tracker.getPosition()[2])
			GlobalVariables.position = GlobalVariables.tracker.getPosition()

       # """Setze die Shortcuts zur Bewegung einmalig"""
	if GlobalVariables.flugEinmalGesetzt is False:
		vizact.whilekeydown(viz.KEY_SHIFT_L, bewege)
		vizact.whilekeydown(viz.KEY_ALT_L, bewege)
		GlobalVariables.flugEinmalGesetzt = True
	





def speedUp():
        """erhoehe bewegugnsgeschwindigkeit"""
        
	#"""Falls die maximale Geschwindigkeit noch nicht erreicht wurde"""
	if(GlobalVariables.moveSpeed<40):
		GlobalVariables.moveSpeed += 0.2
		position = viz.MainView.getPosition()
		euler = viz.MainView.getEuler()
		
		#"""Loesche alten Tracker und initialisiere neuen mit erhoehter Geschwindigkeit"""
		GlobalVariables.tracker.remove()
		GlobalVariables.tracker = vizcam.addWalkNavigate(moveScale=GlobalVariables.moveSpeed)
		GlobalVariables.link = viz.link(GlobalVariables.tracker, viz.MainView)
		GlobalVariables.tracker.setPosition(position)
		GlobalVariables.tracker.setEuler(euler)
		viz.postEvent(viz.getEventID("VIEW_CHANGED_EVENT"), GlobalVariables.tracker)		
	#"""Zeige User die neue Geschwindigkeit"""
	GlobalVariables.midTextScreen.message("Geschwindigkeit: " + str(GlobalVariables.moveSpeed))
	vizact.ontimer2(1, 0, GlobalVariables.midTextScreen.message, "")
		
			

def speedDown():
        """verringere bewegeungsgeschwindigkeit"""
        
        #"""Falls die minimale Geschwindigkeit noch nicht erreicht wurde"""
	if(GlobalVariables.moveSpeed>0.4):
		GlobalVariables.moveSpeed -=0.2
		position = viz.MainView.getPosition()
		euler = viz.MainView.getEuler()
			
		#"""Loesche alten Tracker und initialisiere neuen mit erhoehter Geschwindigkeit"""
		GlobalVariables.tracker.remove()
		GlobalVariables.tracker = vizcam.addWalkNavigate(moveScale=GlobalVariables.moveSpeed)
		GlobalVariables.link = viz.link(GlobalVariables.tracker, viz.MainView)
		GlobalVariables.tracker.setPosition(position)
		GlobalVariables.tracker.setEuler(euler)
		viz.postEvent(viz.getEventID("VIEW_CHANGED_EVENT"), GlobalVariables.tracker)	
	#"""Zeige User die neue Geschwindigkeit"""
	GlobalVariables.midTextScreen.message("Geschwindigkeit: " + str(GlobalVariables.moveSpeed))
	vizact.ontimer2(1, 0, GlobalVariables.midTextScreen.message, "")
		
		

def flySpeedUp():
        """erhoehe Fluggeschwindigkeit"""
        
       # """Falls die maximale Fluggeschwindigkeit noch nicht erreicht wurde"""
	if GlobalVariables.flySpeed <10:
		GlobalVariables.flySpeed +=0.05
		
	#"""Zeige User die neue Geschwindigkeit"""
	GlobalVariables.midTextScreen.message("Fluggeschwindigkeit: " + str(GlobalVariables.flySpeed))
	vizact.ontimer2(1, 0, GlobalVariables.midTextScreen.message, "")
	

def flySpeedDown():
        """verringere Fluggeschwindigkeit"""
        
        #"""Falls die minimale Fluggeschwindigkeit noch nicht erreicht wurde"""
	if GlobalVariables.flySpeed>0.1:
		GlobalVariables.flySpeed -=0.05
	#"""Zeige User die neue Geschwindigkeit"""
	GlobalVariables.midTextScreen.message("Fluggeschwindigkeit: " + str(GlobalVariables.flySpeed))
	vizact.ontimer2(1, 0, GlobalVariables.midTextScreen.message, "")
	
	
			

def flugModusOnOff():
        """FlugmodusOnOFF"""
        
	#"""Falls Flugmodus bereits aktiv ist, deaktiviere"""
	if (GlobalVariables.flugModus is True):
		GlobalVariables.flugModus = False
		viz.collision(viz.ON)
			
		GlobalVariables.position = viz.MainView.getPosition() """evtl noch entfernen"""

        #"""Zeige Flugmodusangabe auf dem Bildschirm"""
		GlobalVariables.midTextScreen.message("Flugmodus: OFF")
		vizact.ontimer2(1, 0, GlobalVariables.midTextScreen.message, "")

	#"""Falls Flugmodus inaktiv ist, aktiviere"""
	else:
		GlobalVariables.flugModus = True
		viz.collision(viz.OFF)
		#"""Zeige Flugmodusangabe auf dem Bildschirm"""
		GlobalVariables.midTextScreen.message("Flugmodus: ON")
		vizact.ontimer2(1, 0, GlobalVariables.midTextScreen.message, "")
	
	
