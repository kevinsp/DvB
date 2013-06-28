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

	#"""Falls Vogelperspektive nicht aktiviert ist"""
	if not (birdEyeViewIsActivated):
               # """Fenster für die Vogelperspektive erstellen"""
		BirdEyeWindow = viz.addWindow() 
		BirdEyeWindow.fov(60)

		#"""Eine neue View erstellen"""
		BirdEyeView = viz.addView()
		#"""View in das Fenster einfügen"""
		BirdEyeWindow.setView(BirdEyeView)
		#"""Die View mit der MainView verknüpfen"""
		link = viz.link( viz.MainView, BirdEyeView)
		#"""Winkel, sodass Perspektive von oben"""
		link.preEuler([0,90,0])
		#"""Höhe der View"""
		link.postTrans([0,30,0]) 
		
		birdEyeViewIsActivated = True
	else:
                 #"""Entferne Vogelperspektive"""
		BirdEyeWindow.remove()
		birdEyeViewIsActivated = False
