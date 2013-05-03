import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizact


checkNotesVisible = False
noteList = []


#Setze Text an eigener Position
def openTextBox():
	#Erschaffe Textbox
	textBox = viz.addTextbox()
	textBox.setPosition(0.5,0.5)
	textBox.overflow(viz.OVERFLOW_GROW)
	
	#Erschaffe Bestätigungsbutton
	bestaetigeButton = viz.addButtonLabel("OK")
	bestaetigeButton.setPosition(0.5,0.45)
	bestaetigeButton.setScale(1,1)
	
	#Text schreiben und Box + Button löschen
	def writeText():
		text = textBox.get()
		userPosition = viz.MainView.getPosition()
		text3D = viz.addText3D(text, pos = [userPosition[0]-0.2, userPosition[1], userPosition[2] + 0.2])
		text3D.setScale(0.2, 0.2, 0.2)
		text3D.color(viz.RED)
		textBox.remove()
		bestaetigeButton.remove()
		noteList.append(text3D)
	vizact.onbuttondown(bestaetigeButton, writeText)	
	
#Notizen anzeigen
def noteView():
	global checkNotesVisible
	global checkNotesPanel

	if not checkNotesVisible: #Falls Checkboxfenster nicht 
		message = ""	# sichtbar, checkpoints auslesen und ausgeben
		checkNotesZaehler = 1
		for a in noteList: #Checkpoints zusammenschreiben
			message += str (checkNotesZaehler) + ". " + str (a.getMessage()) + "\n"
			checkNotesZaehler += 1
		checkNotesPanel = vizinfo.InfoPanel("Notizen:\n" + message,align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
		checkNotesVisible = True
		checkNotesPanel.visible(True)
	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkNotesVisible = False
		checkNotesPanel.visible(False)
		
#Lösche 3D Notiz
def delete3DNote():
	#Erschaffe Textbox
	textBox = viz.addTextbox()
	textBox.setPosition(0.5,0.5)
	textBox.overflow(viz.OVERFLOW_GROW)
	
	#Erschaffe Bestätigungsbutton
	bestaetigeButton = viz.addButtonLabel("Löschen")
	bestaetigeButton.setPosition(0.5,0.45)
	bestaetigeButton.setScale(1,1)
	
	#Checkpoint löschen und Box + Button löschen
	def delete3DNote1():

		noteNummer = textBox.get()
		bestaetigeButton.remove()
		textBox.remove()
		
		def removeNotePanel():
			notePanel.remove()
			okButton.remove()
				
		try:
			if (int(noteNummer)>0):
				noteList[int (noteNummer)-1].remove()
				del noteList[int (noteNummer)-1] #Lösche 3D Notiz
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

#Zu 3D Notizen porten
def port3DNote(tracker):
	#Erschaffe Textbox
	noteBox = viz.addTextbox()
	noteBox.setPosition(0.5,0.5)
	noteBox.overflow(viz.OVERFLOW_GROW)
	
	#Erschaffe Bestätigungsbutton
	portButton1 = viz.addButtonLabel("Porten")
	portButton1.setPosition(0.5,0.45)
	portButton1.setScale(1,1)
	
	def porten():
		#Position abfragen und textbox + button entfernen
		noteNummer = noteBox.get()
		portButton1.remove()
		noteBox.remove()
		
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

