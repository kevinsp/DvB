import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizact

import checkpoints
import globalVariables

checkNotesVisible = False
noteList = []


#Setze Text an eigener Position
def openTextBox():
	if (globalVariables.windowOpen is False):
		globalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Setze 3D Text")

		textBox = infoBox.add(viz.TEXTBOX, "Text:")
		bestaetigeButton = infoBox.add(viz.BUTTON_LABEL, "Ok")	
		
		
		
		#Text schreiben und Box + Button löschen
		def writeText():
			text = textBox.get()
			userPosition = viz.MainView.getPosition()
			text3D = viz.addText3D(text, pos = [userPosition[0]-0.2, userPosition[1], userPosition[2] + 0.2])
			text3D.setScale(0.2, 0.2, 0.2)
			text3D.color(viz.RED)
			infoBox.remove()
			noteList.append(text3D)
			globalVariables.windowOpen = False
		vizact.onbuttondown(bestaetigeButton, writeText)	
	else:
		pass
	
#Notizen anzeigen
def noteView(onViolent):
	global checkNotesVisible
	global checkNotesPanel
	
	if not checkNotesVisible: #Falls Checkboxfenster nicht 
		message = ""	# sichtbar, notes auslesen und ausgeben
		checkNotesZaehler = 1
		for a in noteList: #Notes zusammenschreiben
			message += str (checkNotesZaehler) + ". " + str (a.getMessage()) + "\n"
			checkNotesZaehler += 1
		if (globalVariables.infoWindowOpen is True):
			checkpoints.checkPoints(True)
		checkNotesPanel = vizinfo.InfoPanel("Notizen:\n" + message,align=viz.ALIGN_RIGHT_CENTER,fontSize=15,icon=False,key=None)
		checkNotesVisible = True
		checkNotesPanel.visible(True)
		globalVariables.infoWindowOpen = True
		
	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkNotesVisible = False
		checkNotesPanel.visible(False)
		if (onViolent is False):
			globalVariables.infoWindowOpen = False
		
#Lösche 3D Notiz
def delete3DNote():
	if (globalVariables.windowOpen is False):
		globalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Lösche 3D Text")

		textBox = infoBox.add(viz.TEXTBOX, "3D Text Nr:")
		bestaetigeButton = infoBox.add(viz.BUTTON_LABEL, "Löschen")		
		
		
		#Checkpoint löschen und Box + Button löschen
		def delete3DNote1():

			noteNummer = textBox.get()
			infoBox.remove()
			
			def removeNotePanel():
				notePanel.remove()
				okButton.remove()
				globalVariables.windowOpen = False
				
					
			try:
				if (int(noteNummer)>0):
					noteList[int (noteNummer)-1].remove()
					del noteList[int (noteNummer)-1] #Lösche 3D Notiz
					globalVariables.windowOpen = False
				else:
					raise
			except:
				notePanel = vizinfo.InfoPanel("Bitte nur Nummern im Bereich\nder verfügbaren 3D Notizen eingeben.",align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
				notePanel.visible(True)
				#Erschaffe Bestätigungsbutton
				okButton = viz.addButtonLabel("Ok")
				okButton.setPosition(0.5,0.40)
				okButton.setScale(1,1)
				vizact.onbuttondown(okButton,removeNotePanel)
		vizact.onbuttondown(bestaetigeButton, delete3DNote1)	
	else:
		pass
		
#Zu 3D Notizen porten
def port3DNote(tracker):
	if (globalVariables.windowOpen is False):
		globalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Zu 3D Text porten")

		noteBox = infoBox.add(viz.TEXTBOX, "Text Nr:")
		portButton1 = infoBox.add(viz.BUTTON_LABEL, "Porten")	
		
		def porten():
			#Position abfragen und textbox + button entfernen
			noteNummer = noteBox.get()
			infoBox.remove()
			
			def removeNotePanel():
				notePanel.remove()
				okButton.remove()
			
			try:
				if (int(noteNummer)>0): #Prüfe eingabe und porte
					position = noteList[int(noteNummer)-1].getPosition()
					viz.MainView.setPosition(position[0], position[1], position[2]-0.5)
					tracker.setPosition(position[0], position[1], position[2]-0.5)
				else:
					raise
			except:
				notePanel = vizinfo.InfoPanel("Bitte nur Nummern im Bereich\nder verfügbaren 3D Notizen eingeben.",align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
				notePanel.visible(True)
				#Erschaffe Bestätigungsbutton
				okButton = viz.addButtonLabel("Ok")
				okButton.setPosition(0.5,0.40)
				okButton.setScale(1,1)
				vizact.onbuttondown(okButton,removeNotePanel)
				
		vizact.onbuttondown(portButton1, porten)
	else:
		pass

