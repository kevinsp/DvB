import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizact

import Checkpoints
import GlobalVariables

checkNotesVisible = False
noteList = []


#Setze Text an eigener Position
def openTextBox(menubar):
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Setze 3D Text")
		infoBox.bgcolor(GlobalVariables.vizInfoBackgroundColor)
		infoBox.bordercolor(GlobalVariables.vizInfoBorderColor)
		infoBox.titlebgcolor(GlobalVariables.vizInfoTitleBackgroundColor)

		textBox = infoBox.add(viz.TEXTBOX, "Text:")
		bestaetigeButton = infoBox.add(viz.BUTTON_LABEL, "Ok")	
		vizact.ontimer2(0.1, 0, textBox.setFocus, viz.ON)
		menubar.setVisible(viz.OFF)
		
		
		#Text schreiben und Box + Button löschen
		def writeText():
			text = textBox.get()
			infoBox.remove()
			def removeNotePanel():
				notePanel.remove()
				okButton.remove()
				GlobalVariables.windowOpen = False
				
			if (text.strip() is not ""):
				userPosition = viz.MainView.getPosition()
				userEuler = viz.MainView.getEuler()
				text3D = viz.addText3D(text, pos = [userPosition[0]-0.2, userPosition[1], userPosition[2] + 0.2])
				text3D.setScale(0.2, 0.2, 0.2)
				text3D.color(viz.RED)
				noteList.append([text3D, round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3)])
				GlobalVariables.windowOpen = False
			else:
				notePanel = vizinfo.InfoPanel("Bitte nur Notizen mit Text eingeben.",align=viz.ALIGN_CENTER,fontSize=15,icon=False,key=None)
				notePanel.visible(True)
				#Erschaffe Bestätigungsbutton
				okButton = viz.addButtonLabel("Ok")
				okButton.setPosition(0.5,0.425)
				okButton.setScale(1,1)
				vizact.onbuttondown(okButton,removeNotePanel)
				

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
			message += str (checkNotesZaehler) + ". " + str (a[0].getMessage()) + "\n"
			checkNotesZaehler += 1
		if (GlobalVariables.infoWindowOpen is True):
			Checkpoints.checkPoints(True)
		checkNotesPanel = vizinfo.InfoPanel("Notizen:\n" + message,align=viz.ALIGN_RIGHT_CENTER,fontSize=15,icon=False,key=None)
		checkNotesVisible = True
		checkNotesPanel.visible(True)
		GlobalVariables.infoWindowOpen = True
		
	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkNotesVisible = False
		checkNotesPanel.visible(False)
		if (onViolent is False):
			GlobalVariables.infoWindowOpen = False
		
#Lösche 3D Notiz
def delete3DNote(menubar):
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Lösche 3D Text")
		infoBox.bgcolor(GlobalVariables.vizInfoBackgroundColor)
		infoBox.bordercolor(GlobalVariables.vizInfoBorderColor)
		infoBox.titlebgcolor(GlobalVariables.vizInfoTitleBackgroundColor)

		textBox = infoBox.add(viz.TEXTBOX, "3D Text Nr:")
		bestaetigeButton = infoBox.add(viz.BUTTON_LABEL, "Löschen")		
		vizact.ontimer2(0.1, 0, textBox.setFocus, viz.ON)
		menubar.setVisible(viz.OFF)

		#Checkpoint löschen und Box + Button löschen
		def delete3DNote1():

			noteNummer = textBox.get()
			infoBox.remove()
			
			def removeNotePanel():
				notePanel.remove()
				okButton.remove()
				GlobalVariables.windowOpen = False
				
					
			try:
				if (int(noteNummer)>0):
					noteList[int (noteNummer)-1].remove()
					del noteList[int (noteNummer)-1] #Lösche 3D Notiz
					GlobalVariables.windowOpen = False
				else:
					raise
			except:
				notePanel = vizinfo.InfoPanel("Bitte nur Nummern im Bereich\nder verfuegbaren 3D Notizen eingeben.",align=viz.ALIGN_CENTER,fontSize=15,icon=False,key=None)
				notePanel.visible(True)
				#Erschaffe Bestätigungsbutton
				okButton = viz.addButtonLabel("Ok")
				okButton.setPosition(0.5,0.425)
				okButton.setScale(1,1)
				vizact.onbuttondown(okButton,removeNotePanel)
		vizact.onbuttondown(bestaetigeButton, delete3DNote1)	
	else:
		pass
		
#Zu 3D Notizen porten
def port3DNote(tracker, menubar):
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		#Erschaffe VizInfo Box
		infoBox = vizinfo.add("")
		infoBox.scale(0.8,1)
		infoBox.translate(0.65,0.6)
		infoBox.title("Zu 3D Text porten")
		infoBox.bgcolor(GlobalVariables.vizInfoBackgroundColor)
		infoBox.bordercolor(GlobalVariables.vizInfoBorderColor)
		infoBox.titlebgcolor(GlobalVariables.vizInfoTitleBackgroundColor)

		noteBox = infoBox.add(viz.TEXTBOX, "Text Nr:")
		portButton1 = infoBox.add(viz.BUTTON_LABEL, "Porten")	
		vizact.ontimer2(0.1, 0, noteBox.setFocus, viz.ON)
		menubar.setVisible(viz.OFF)

		def porten():
			#Position abfragen und textbox + button entfernen
			noteNummer = noteBox.get()
			infoBox.remove()
			
			def removeNotePanel():
				notePanel.remove()
				okButton.remove()
				GlobalVariables.windowOpen = False
			
			try:
				if (int(noteNummer)>0): #Prüfe eingabe und porte
					text = noteList[int(noteNummer)-1]
					position = text[0].getPosition()
		
					viz.MainView.setPosition(position[0], position[1], position[2]-0.5)
					tracker.setPosition(position[0], position[1], position[2]-0.5)
					
					viz.MainView.setEuler(text[1], text[2], text[3])
					tracker.setEuler(text[1], text[2], text[3])
					GlobalVariables.euler = [text[1], text[2], text[3]]
					
					GlobalVariables.position = tracker.getPosition()
					GlobalVariables.windowOpen = False

				else:
					raise
			except:
				notePanel = vizinfo.InfoPanel("Bitte nur Nummern im Bereich\nder verfuegbaren 3D Notizen eingeben.",align=viz.ALIGN_CENTER,fontSize=15,icon=False,key=None)
				notePanel.visible(True)
				#Erschaffe Bestätigungsbutton
				okButton = viz.addButtonLabel("Ok")
				okButton.setPosition(0.5,0.425)
				okButton.setScale(1,1)
				vizact.onbuttondown(okButton,removeNotePanel)
				
		vizact.onbuttondown(portButton1, porten)
	else:
		pass

