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

#Vogelperspektive
def enableBirdEyeView():
	global birdEyeViewIsActivated
	global BirdEyeWindow
	
	if not (birdEyeViewIsActivated):
		BirdEyeWindow = viz.addWindow()
		BirdEyeWindow.fov(60)
		BirdEyeView = viz.addView()
		BirdEyeWindow.setView(BirdEyeView)
		link = viz.link( viz.MainView, BirdEyeView)
		link.preEuler([0,90,0]) #winkel der cam
		link.postTrans([0,30,0]) #höhe der view
		birdEyeViewIsActivated = True
	else:
		BirdEyeWindow.remove()
		birdEyeViewIsActivated = False