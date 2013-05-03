import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizact

checkPointsVisible = False
checkPointsList = []	

#Checkpointliste Fenster
def checkPoints():
	global checkPointsVisible
	global checkPointsPanel
	
	if not checkPointsVisible: #Falls Checkboxfenster nicht 
		message = ""	# sichtbar, checkpoints auslesen und ausgeben
		checkPointZaehler = 1
		for a in checkPointsList: #Checkpoints zusammenschreiben
			message += str (checkPointZaehler) + ". " + str (a) + "\n"
			checkPointZaehler += 1
		checkPointsPanel = vizinfo.InfoPanel("Checkpoints:\n" + message,align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
		checkPointsVisible = True
		checkPointsPanel.visible(True)
	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkPointsVisible = False
		checkPointsPanel.visible(False)

#Checkpoint erstellen/speichern
def createCheckpoint():
	userPosition = viz.MainView.getPosition() #Frage User Position
	#Füge Checkpoint zur Liste auf 3 Nachkommastellen gerundet an
	checkPointsList.append([round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3)])
		
#Lösche Checkpoint
def deleteCheckpoint():
	#Erschaffe Textbox
	textBox = viz.addTextbox()
	textBox.setPosition(0.5,0.5)
	textBox.overflow(viz.OVERFLOW_GROW)
	
	#Erschaffe Bestätigungsbutton
	bestaetigeButton = viz.addButtonLabel("Löschen")
	bestaetigeButton.setPosition(0.5,0.45)
	bestaetigeButton.setScale(1,1)
	
	#Checkpoint löschen und Box + Button löschen
	def deleteCheckpoint1():

		checkpointnummer = textBox.get()
		bestaetigeButton.remove()
		textBox.remove()
		
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

#Zu Checkpoints porten
def portCheckPoint(tracker):
	#Erschaffe Textbox
	portBox = viz.addTextbox()
	portBox.setPosition(0.5,0.5)
	portBox.overflow(viz.OVERFLOW_GROW)
	
	#Erschaffe Bestätigungsbutton
	portButton1 = viz.addButtonLabel("Porten")
	portButton1.setPosition(0.5,0.45)
	portButton1.setScale(1,1)
	
	def porten():
		#Position abfragen und textbox + button entfernen
		checkPointNummer = portBox.get()
		portButton1.remove()
		portBox.remove()
		
		def removeCheckPointsPanel():
			checkPointsPanel.remove()
			okButton.remove()
			
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
