import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizact

import globalVariables
import notes

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
		if (globalVariables.infoWindowOpen is True):
			notes.noteView(True)	
			
		checkPointsPanel = vizinfo.InfoPanel("Checkpoints:\n" + message,align=viz.ALIGN_RIGHT_CENTER,fontSize=15,icon=False,key=None)
		checkPointsVisible = True
		checkPointsPanel.visible(True)
		globalVariables.infoWindowOpen = True

	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkPointsVisible = False
		checkPointsPanel.visible(False)
		if (onViolent is False):
			globalVariables.infoWindowOpen = False
			
		

#Checkpoint erstellen/speichern
def createCheckpoint():
	
	
	if (globalVariables.windowOpen is False):
		globalVariables.windowOpen = True
		userPosition = viz.MainView.getPosition() #Frage User Position
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Checkpoint anlegen")

		textBox = infoBox.add(viz.TEXTBOX, "Kommentar:")
		bestaetigeButton = infoBox.add(viz.BUTTON_LABEL, "ok")	

		

		def checkpointHinzufuegen():
			#Füge Checkpoint zur Liste auf 3 Nachkommastellen gerundet an	
			checkPointsList.append([round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3), textBox.get()])
			infoBox.remove()
			globalVariables.windowOpen = False
		
		vizact.onbuttondown(bestaetigeButton, checkpointHinzufuegen)	
	else:
		pass
	
#Lösche Checkpoint
def deleteCheckpoint():
	global fensterOpen	
	if (globalVariables.windowOpen is False):
		globalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Checkpoint löschen")

		textBox = infoBox.add(viz.TEXTBOX, "Checkpoint Nr:")
		bestaetigeButton = infoBox.add(viz.BUTTON_LABEL, "ok")	
			
		#Checkpoint löschen und Box + Button löschen
		def deleteCheckpoint1():

			checkpointnummer = textBox.get()
			infoBox.remove()
			globalVariables.windowOpen = False
			
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
				okButton.setPosition(0.5,0.40)
				okButton.setScale(1,1)
				vizact.onbuttondown(okButton,removeCheckPointsPanel)
			
		vizact.onbuttondown(bestaetigeButton, deleteCheckpoint1)	
	else:
		pass

#Zu Checkpoints porten
def portCheckPoint(tracker):
	if (globalVariables.windowOpen is False):
		globalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Zu Checkpoint porten")

		portBox = infoBox.add(viz.TEXTBOX, "Checkpoint Nr:")
		portButton1 = infoBox.add(viz.BUTTON_LABEL, "Porten")	
		

		
		def porten():
			#Position abfragen und infobox entfernen
			checkPointNummer = portBox.get()
			infoBox.remove()
			
			def removeCheckPointsPanel():
				checkPointsPanel.remove()
				okButton.remove()
				globalVariables.windowOpen = False
				
			try:
				if (int(checkPointNummer)>0): #Prüfe eingabe und porte
					position = checkPointsList[int(checkPointNummer)-1]
					viz.MainView.setPosition(position[0], position[1], position[2])
					tracker.setPosition(position[0], position[1], position[2])
				else:
					raise
			except:

				checkPointsPanel = vizinfo.InfoPanel("Bitte nur Nummern im Bereich\nder verfügbaren Checkpoints eingeben.",align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
				checkPointsPanel.visible(True)
				#Erschaffe Bestätigungsbutton
				okButton = viz.addButtonLabel("Ok")
				okButton.setPosition(0.5,0.40)
				okButton.setScale(1,1)
				vizact.onbuttondown(okButton,removeCheckPointsPanel)
				
		vizact.onbuttondown(portButton1, porten)
