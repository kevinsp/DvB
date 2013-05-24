import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizact
import vizdlg

import GlobalVariables
import Notes

checkPointsVisible = False
checkPointsList = []
	

#Checkpointliste Fenster
def checkPoints(onViolent):
	global checkPointsVisible
	global checkPointsPanel
	
	
	if not checkPointsVisible: 	#Falls Checkboxfenster nicht 
		message = ""			# sichtbar, checkpoints auslesen und ausgeben
		checkPointZaehler = 1
		for a in checkPointsList: #Checkpoints zusammenschreiben
			message += str (checkPointZaehler) + ". "+ str (a[3])+"\n    "+ str (a[0]) +" "+ str (a[1]) +" "+ str (a[2])  + "\n"
			checkPointZaehler += 1
		if (GlobalVariables.infoWindowOpen is True):
			Notes.noteView(True)	
			
		checkPointsPanel = vizinfo.InfoPanel("Checkpoints:\n" + message,align=viz.ALIGN_RIGHT_CENTER,fontSize=15,icon=False,key=None)
		checkPointsVisible = True
		checkPointsPanel.visible(True)
		GlobalVariables.infoWindowOpen = True

	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkPointsVisible = False
		checkPointsPanel.visible(False)
		if (onViolent is False):
			GlobalVariables.infoWindowOpen = False
			
		

#Checkpoint erstellen/speichern
def createCheckpoint(menubar):
	
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		userPosition = viz.MainView.getPosition() #Frage User Position
		userEuler = viz.MainView.getEuler()
		"""
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Checkpoint anlegen")
		infoBox.bgcolor(GlobalVariables.vizInfoBackgroundColor)
		infoBox.bordercolor(GlobalVariables.vizInfoBorderColor)
		infoBox.titlebgcolor(GlobalVariables.vizInfoTitleBackgroundColor)
		"""

		"""
		textBox = infoBox.add(viz.TEXTBOX, "Kommentar:")
		abbrechenButton = infoBox.add(viz.BUTTON_LABEL, "Abbrechen")
		
		bestaetigeButton = infoBox.add(viz.BUTTON_LABEL, "Ok")		
		vizact.ontimer2(0.1, 0, textBox.setFocus, viz.ON)
		"""
		
		menubar.setVisible(viz.OFF)

		def checkpointHinzufuegen(text):
			#Füge Checkpoint zur Liste auf 3 Nachkommastellen gerundet an	
			checkPointsList.append([round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3), str (text), \
			round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3)])
			#infoBox.remove()
			
			return True
		
#######################		
		input = vizdlg.InputDialog(prompt='Kommentar zum Checkpoint', length=1.0)
		viz.link(viz.CenterCenter,input)
		input.alpha(0.4)
		input.color(0,0,0)
		
		def showdialog():
			yield input.show()
				   
			if input.accepted:
				checkpointHinzufuegen(input.value)
			else:
				pass
			  
			GlobalVariables.windowOpen = False
		   
		viztask.schedule(showdialog()) 
		
##############		
		#vizact.onbuttondown(bestaetigeButton, checkpointHinzufuegen)	
	else:
		pass
	
#Lösche Checkpoint
def deleteCheckpoint(menubar):
	global fensterOpen	
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Checkpoint loeschen")
		infoBox.bgcolor(GlobalVariables.vizInfoBackgroundColor)
		infoBox.bordercolor(GlobalVariables.vizInfoBorderColor)
		infoBox.titlebgcolor(GlobalVariables.vizInfoTitleBackgroundColor)
		
		textBox = infoBox.add(viz.TEXTBOX, "Checkpoint Nr:")
		bestaetigeButton = infoBox.add(viz.BUTTON_LABEL, "Ok")	
		vizact.ontimer2(0.1, 0, textBox.setFocus, viz.ON)
		menubar.setVisible(viz.OFF)
		#Checkpoint löschen und Box + Button löschen
		def deleteCheckpoint1():

			checkpointnummer = textBox.get()
			infoBox.remove()
			GlobalVariables.windowOpen = False
			
			def removeCheckPointsPanel():
				checkPointsPanel.remove()
				okButton.remove()
		
			try:
				if (int(checkpointnummer)>0):
					del checkPointsList[int (checkpointnummer)-1] #Lösche Checkpoint
				else:
					raise
			except:
				checkPointsPanel = vizinfo.InfoPanel("Bitte nur Nummern im Bereich\nder verfügbaren Checkpoints eingeben.",align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
				checkPointsPanel.visible(True)
				#Erschaffe Bestätigungsbutton
				okButton = viz.addButtonLabel("Ok")
				okButton.setPosition(0.5,0.425)
				okButton.setScale(1,1)
				vizact.onbuttondown(okButton,removeCheckPointsPanel)
			
		vizact.onbuttondown(bestaetigeButton, deleteCheckpoint1)	
	else:
		pass

#Zu Checkpoints porten
def portCheckPoint(tracker, menubar):
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Zu Checkpoint porten")
		infoBox.bgcolor(GlobalVariables.vizInfoBackgroundColor)
		infoBox.bordercolor(GlobalVariables.vizInfoBorderColor)
		infoBox.titlebgcolor(GlobalVariables.vizInfoTitleBackgroundColor)

		portBox = infoBox.add(viz.TEXTBOX, "Checkpoint Nr:")
		portButton1 = infoBox.add(viz.BUTTON_LABEL, "Porten")	
		vizact.ontimer2(0.1, 0, portBox.setFocus, viz.ON)
		menubar.setVisible(viz.OFF)
		
		def porten():
			#Position abfragen und infobox entfernen
			checkPointNummer = portBox.get()
			infoBox.remove()
			
			def removeCheckPointsPanel():
				checkPointsPanel.remove()
				okButton.remove()
				GlobalVariables.windowOpen = False
				
				
			try:
				if (int(checkPointNummer)>0): #Prüfe eingabe und porte
					point = checkPointsList[int(checkPointNummer)-1]
					
					viz.MainView.setPosition(point[0], point[1], point[2])
					tracker.setPosition(point[0], point[1], point[2])
					
					viz.MainView.setEuler(point[4], point[5], point[6])
					tracker.setEuler(point[4], point[5], point[6])
					GlobalVariables.euler = [point[4], point[5], point[6]]
					
					GlobalVariables.position = tracker.getPosition()
					GlobalVariables.windowOpen = False

				else:
					raise
			except:

				checkPointsPanel = vizinfo.InfoPanel("Bitte nur Nummern im Bereich\nder verfügbaren Checkpoints eingeben.",align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
				checkPointsPanel.visible(True)
				#Erschaffe Bestätigungsbutton
				okButton = viz.addButtonLabel("Ok")
				okButton.setPosition(0.5,0.425)
				okButton.setScale(1,1)
				vizact.onbuttondown(okButton,removeCheckPointsPanel)
				
		vizact.onbuttondown(portButton1, porten)
