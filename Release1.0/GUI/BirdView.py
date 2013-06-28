import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask

birdEyeViewIsActivated = False
birdEyeWindow = None


def enableBirdEyeView():
        """Vogelperspektive aktivieren/deaktivieren"""
        
	global birdEyeViewIsActivated
	global BirdEyeWindow
	
	if not (birdEyeViewIsActivated): """Falls Vogelperspektive nicht aktiviert ist"""
		BirdEyeWindow = viz.addWindow() """Fenster für die Vogelperspektive erstellen"""
		BirdEyeWindow.fov(60)
		
		BirdEyeView = viz.addView() """Eine neue View erstellen"""
		BirdEyeWindow.setView(BirdEyeView) """View in das Fenster einfügen"""
		link = viz.link( viz.MainView, BirdEyeView) """Die View mit der MainView verknüpfen"""
		link.preEuler([0,90,0]) """Winkel, sodass Perspektive von oben"""
		link.postTrans([0,30,0]) """Höhe der View"""
		
		birdEyeViewIsActivated = True
	else:
		BirdEyeWindow.remove() """Entferne Vogelperspektive"""
		birdEyeViewIsActivated = False
