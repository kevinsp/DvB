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
import vizpopup

import Note
import CheckpointFunktionen
import GlobalVariables

checkNotesVisible = False
myPanel = vizdlg.Panel()


#Setze Text an eigener Position
def openTextBox(menubar):
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True

		menubar.setVisible(viz.OFF)
	
	
		#ueberpruefe die Eingabe
		
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			if object is input.accept:
				if (data.value.strip() is not "" and len(str(data.value).strip())<=15): #Ist eine Eingabe vorhanden und nciht zu lange?
					writeText(data.value)
					if (checkNotesVisible is True):
						noteView(False)
						noteView(False)
					input.remove()
					GlobalVariables.windowOpen = False

				else:
					data.error = "Bitte nur Text eingeben mit\nmaximal 15 Zeichen."
					input.box.setFocus(viz.ON)
			
			elif object is input.cancel:
				GlobalVariables.windowOpen = False
				input.remove()
			else:
				data.error=""
				input.box.setFocus(viz.ON)
	
		#vizdialog
		input = vizdlg.InputDialog(title = "Schreibe Text", length=1.0, validate = ueberpruefeEingabe)
		viz.link(viz.CenterCenter,input)
		input.box.overflow(viz.OVERFLOW_CROP)
		input.box.setLength(1.35)
		input.alpha(0.4)	
		input.color(0,0,0)
		
		def showdialog():
			while True:
				yield input.show()
					 
				if input.accepted:
					break
				else:
					break
				
		vizact.ontimer2(0.1, 0, input.box.setFocus, viz.ON)
		viztask.schedule(showdialog()) 
		
		
		
		#Text schreiben 
		def writeText(text):
			userPosition = viz.MainView.getPosition()
			userEuler = viz.MainView.getEuler()
			text3D = viz.addText3D(text.strip(), pos = [userPosition[0]-0.2, userPosition[1], userPosition[2] + 0.2])
			text3D.setScale(0.2, 0.2, 0.2)
			text3D.color(viz.RED)
			
			GlobalVariables.noteList.append([text3D, Note.Note(userPosition[0]-0.2, userPosition[1], userPosition[2] + 0.2, text3D.getMessage(), \
											round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3))])
			GlobalVariables.windowOpen = False
			
	else:
		pass
	
#Notizen anzeigen
def noteView(onViolent):
	global checkNotesVisible
	global myPanel
	
	
	if not checkNotesVisible: #Falls Checkboxfenster nicht 
		message = []	# sichtbar, notes auslesen und ausgeben
		checkNotesZaehler = 1
		
		#Berechnung der Gesamtteillisten
		if len(GlobalVariables.noteList) >= 10:
			GlobalVariables.gesamtTeillisteNote = (len(GlobalVariables.noteList)/10)+1
		
		while(checkNotesZaehler <=10 and checkNotesZaehler <= (len(GlobalVariables.noteList))-(10*(GlobalVariables.teillisteNote-1))):
			objekt = GlobalVariables.noteList[checkNotesZaehler-1+(10*(GlobalVariables.teillisteNote-1))][1]
			message.append(str (checkNotesZaehler+(10*(GlobalVariables.teillisteNote-1))) + ". "+ str (objekt.name) +"\n")
			checkNotesZaehler += 1

		
		if (GlobalVariables.infoWindowOpen is True):
			CheckpointFunktionen.checkPoints(True)
			
		myPanel = vizdlg.Panel(theme = GlobalVariables.blackTheme, fontSize=17, align=viz.ALIGN_RIGHT_CENTER, background=False, border=False)
		
		#PanelButtons
		row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0)
		zurueck = row.addItem(viz.addButtonLabel("Zurueck"))
		teillisteView = row.addItem(viz.addText(str(GlobalVariables.teillisteNote) + "/" + str(GlobalVariables.gesamtTeillisteNote)))
		naechste = row.addItem(viz.addButtonLabel("Naechste"))
		myPanel.addItem(row)

		#zirkulierendes "Liste"
		def teillisteVerringernErhoehen(wert):
			if GlobalVariables.teillisteNote == 1 and wert == -1:
				GlobalVariables.teillisteNote = GlobalVariables.gesamtTeillisteNote
			elif GlobalVariables.teillisteNote == GlobalVariables.gesamtTeillisteNote and wert == 1:
				GlobalVariables.teillisteNote = 1
			else:
				GlobalVariables.teillisteNote = GlobalVariables.teillisteNote+wert
			noteView(False)
			noteView(False)

		#Button action
		vizact.onbuttondown(zurueck,teillisteVerringernErhoehen, -1)
		vizact.onbuttondown(naechste, teillisteVerringernErhoehen, 1)
	
		if GlobalVariables.nurEinmalSetzen is False:
			vizact.onkeydown(viz.KEY_LEFT, teillisteVerringernErhoehen, -1)
			vizact.onkeydown(viz.KEY_RIGHT, teillisteVerringernErhoehen, 1)
			GlobalVariables.nurEinmalSetzen = True
	
	
		#Add row to myPanel

		rowlist = [] #liste mit den rows
		noteButtons = []	#liste mit den buttons
		buttonZaehler = 0
		for a in message:
			noteButtons.append(viz.addButtonLabel(message[buttonZaehler]))
			buttonRow = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False, background = False, margin=0)
			buttonRow.addItem(noteButtons[buttonZaehler])
			rowlist.append(buttonRow)
			myPanel.addItem(rowlist[buttonZaehler]) #füge die notebuttonrows ins panel ein
			buttonZaehler+=1


		#####
		deleteNoteSub = vizpopup.Item('Loesche Note')
		porteZuNote = vizpopup.Item('Springe zu')
		mymenu = vizpopup.Menu('Main',[deleteNoteSub, porteZuNote])		




		#Zeige subMenu an
		def subMenu(position):		
			vizpopup.onMenuItem(deleteNoteSub, delete3DNote, position=position)
			vizpopup.onMenuItem(porteZuNote, port3DNote, position=position)
			vizpopup.display(mymenu)
			
			
		#belege die ganzen Buttons mit submenu anzeigen funktionen
		i=0
		for a in noteButtons:
			vizact.onbuttonup(noteButtons[i], subMenu, i)
			i+=1


		#myPanel.addItem(row)
		viz.link(viz.RightCenter, myPanel)
		
		checkNotesVisible = True
		GlobalVariables.infoWindowOpen = True

	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkNotesVisible = False
		myPanel.visible(False)
		if (onViolent is False):
			GlobalVariables.infoWindowOpen = False

#Lösche 3D Notiz
def delete3DNote(menubar=None, position = None):
	if (GlobalVariables.windowOpen is False):
		if menubar is not None:
			menubar.setVisible(viz.OFF)
		#ueberpruefe die Eingabe
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			if object is input.accept:
				try:
					if (type(int(data.value)) is int and int(data.value) <= len(GlobalVariables.noteList) and int(data.value )> 0): #Ist die Eingabe im gültigen bereich?
						GlobalVariables.noteList[int (data.value)-1][0].remove()
						del GlobalVariables.noteList[int (data.value)-1] #Lösche 3D Notiz
						GlobalVariables.windowOpen = False
						if (checkNotesVisible is True):
							noteView(False)
							noteView(False)
						input.remove()
						GlobalVariables.windowOpen = False

					else:
						data.error = "Bitte nur eine gueltige\nNummer eingeben."
						input.box.setFocus(viz.ON)
				except:
					data.error = "Bitte nur eine gueltige\nNummer eingeben."
					input.box.setFocus(viz.ON)
			elif object is input.cancel:
				GlobalVariables.windowOpen = False
				input.remove()
			else:
				data.error=""
				input.box.setFocus(viz.ON)
		if position is None:
			GlobalVariables.windowOpen = True
			#vizdialog
			input = vizdlg.InputDialog(title = "Loesche Notiz", prompt="Notiznummer eingeben",  length=1.0, validate = ueberpruefeEingabe)
			viz.link(viz.CenterCenter,input)
			input.alpha(0.4)	
			input.color(0,0,0)
			
			def showdialog():
				while True:
					yield input.show()
						 
					if input.accepted:
						break
					else:
						break
					
			vizact.ontimer2(0.1, 0, input.box.setFocus, viz.ON)
			viztask.schedule(showdialog()) 
		else:
			if (int(position) < len(GlobalVariables.noteList) and int(position)>= 0): #Ist die Eingabe im gültigen bereich?
				GlobalVariables.noteList[int (position)][0].remove()
				del GlobalVariables.noteList[int (position)] #Lösche 3D Notiz
				if (checkNotesVisible is True):
					noteView(False)
					noteView(False)
	else:
		pass
		
#Zu 3D Notizen porten
def port3DNote(menubar=None, position=None):
	if (GlobalVariables.windowOpen is False):
		
		if menubar is not None:
			menubar.setVisible(viz.OFF)

		#ueberpruefe die Eingabe
		
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			if object is input.accept:
				try:
					if (type(int(data.value)) is int and int(data.value) <= len(GlobalVariables.noteList) and int(data.value )> 0): #Ist die Eingabe im gültigen bereich?
						text = GlobalVariables.noteList[int(data.value)-1][1]

						viz.MainView.setPosition(text.posX, text.posZ, text.posY-0.5)
						GlobalVariables.tracker.setPosition(text.posX, text.posZ, text.posY-0.5)

						viz.MainView.setEuler(text.eulerX, text.eulerZ, text.eulerY)
						GlobalVariables.tracker.setEuler(text.eulerX, text.eulerZ, text.eulerY)
						
						GlobalVariables.euler = GlobalVariables.tracker.getEuler()
						GlobalVariables.position = GlobalVariables.tracker.getPosition()
						GlobalVariables.windowOpen = False
						input.remove()
						
					else:
						data.error = "Bitte nur eine gueltige\nNummer eingeben."
						input.box.setFocus(viz.ON)
				except:
					data.error = "Bitte nur eine gueltige\nNummer eingeben."
					input.box.setFocus(viz.ON)
			elif object is input.cancel:
				GlobalVariables.windowOpen = False
				input.remove()
			else:
				data.error=""
				input.box.setFocus(viz.ON)
		if position is None:
			GlobalVariables.windowOpen = True
			#vizdialog
			input = vizdlg.InputDialog(title = "Porte zu Notiz", prompt="Notiznummer eingeben", length=1.0, validate = ueberpruefeEingabe)
			viz.link(viz.CenterCenter,input)
			input.alpha(0.4)	
			input.color(0,0,0)
			
			def showdialog():
				while True:
					yield input.show()
						 
					if input.accepted:
						break
					else:
						break
			input.box.setFocus(viz.ON)
			viztask.schedule(showdialog()) 
		else:
			if (int(position) < len(GlobalVariables.noteList) and int(position)>= 0): #Ist die Eingabe im gültigen bereich?
				text = GlobalVariables.noteList[int(position)][1]

				viz.MainView.setPosition(text.posX, text.posZ, text.posY-0.5)
				GlobalVariables.tracker.setPosition(text.posX, text.posZ, text.posY-0.5)

				viz.MainView.setEuler(text.eulerX, text.eulerZ, text.eulerY)
				GlobalVariables.tracker.setEuler(text.eulerX, text.eulerZ, text.eulerY)
						
				GlobalVariables.euler = GlobalVariables.tracker.getEuler()
				GlobalVariables.position = GlobalVariables.tracker.getPosition()
	else:
		pass
