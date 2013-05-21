import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizpopup
import vizact

import GlobalVariables

def porten(tracker, menubar):
	
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		
		infoBox.title("Zu beliebige Position porten")

		posiXBox = infoBox.add(viz.TEXTBOX, "X-Koordinate:")
		posiYBox = infoBox.add(viz.TEXTBOX, "Y-Koordinate:")
		posiZBox = infoBox.add(viz.TEXTBOX, "Z-Koordinate:")
		portButton1 = infoBox.add(viz.BUTTON_LABEL, "Porten")	
		
		menubar.setVisible(viz.OFF)
		
	


		#man braucht kein doppelklick mehr um den focus
		#der textboxen zu ändern
		def updateFocus():
			print "test"
			object = viz.pick(0,viz.SCREEN)

			if object == posiXBox:
				posiXBox.setFocus(viz.ON)
			elif object == posiYBox:
				posiYBox.setFocus(viz.ON)
			elif object == posiZBox:
				posiZBox.setFocus(viz.ON)
				

		vizact.onbuttonup(posiXBox,updateFocus)
		vizact.onbuttonup(posiYBox,updateFocus)
		vizact.onbuttonup(posiZBox,updateFocus)
		vizact.ontimer2(0.1, 0, posiXBox.setFocus, viz.ON)
		
		def porten2():
			#Position abfragen und infobox
			posiX = posiXBox.get()
			posiY = posiYBox.get()
			posiZ = posiZBox.get()
			infoBox.remove()
			
			

			def removePortPanel():
				checkPointsPanel.remove()
				okButton.remove()
				GlobalVariables.windowOpen = False
				
			try:
				###Kolissionserkennung einbauen###
				viz.MainView.setPosition(float(posiX), float(posiZ), float(posiY))
				tracker.setPosition(float(posiX), float(posiZ), float(posiY))
				GlobalVariables.position = tracker.getPosition()
				GlobalVariables.windowOpen = False
			except:
				#####Noch überarbeiten###
				checkPointsPanel = vizinfo.InfoPanel("Fehler",align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
				checkPointsPanel.visible(True)
				#Erschaffe Bestätigungsbutton
				okButton = viz.addButtonLabel("Ok")
				okButton.setPosition(0.5,0.40)
				okButton.setScale(1,1)
				vizact.onbuttondown(okButton,removePortPanel)
		vizact.onbuttondown(portButton1, porten2)
	else:
		pass
				
		
