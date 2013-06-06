﻿import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizact
import vizdlg

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
				if (data.value.strip() is not "" ): #Ist eine Eingabe vorhanden?
					writeText(data.value)
					if (checkNotesVisible is True):
						noteView(False)
						noteView(False)
					input.remove()
					GlobalVariables.windowOpen = False

				else:
					data.error = "Bitte nur Text eingeben."
					input.box.setFocus(viz.ON)
			
			elif object is input.cancel:
				GlobalVariables.windowOpen = False
				input.remove()
			else:
				vizact.ontimer2(0.1, 0, input.box.setFocus, viz.ON)
	
		#vizdialog
		input = vizdlg.InputDialog(title = "Schreibe Text", length=1.0, validate = ueberpruefeEingabe)
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
		
		
		
		#Text schreiben und Box + Button löschen
		def writeText(text):
			userPosition = viz.MainView.getPosition()
			userEuler = viz.MainView.getEuler()
			text3D = viz.addText3D(text.strip(), pos = [userPosition[0]-0.2, userPosition[1], userPosition[2] + 0.2])
			text3D.setScale(0.2, 0.2, 0.2)
			text3D.color(viz.RED)
			GlobalVariables.noteList.append([text3D, round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3)])
			GlobalVariables.windowOpen = False
			
	else:
		pass
	
#Notizen anzeigen
def noteView(onViolent):
	global checkNotesVisible
	global myPanel
	
	
	if not checkNotesVisible: #Falls Checkboxfenster nicht 
		message = ""	# sichtbar, notes auslesen und ausgeben
		checkNotesZaehler = 1
		
		#Berechnung der Gesamtteillisten
		if len(GlobalVariables.noteList) >= 10:
			GlobalVariables.gesamtTeillisteNote = (len(GlobalVariables.noteList)/10)+1

		while(checkNotesZaehler <=10 and checkNotesZaehler <= (len(GlobalVariables.noteList))-(10*(GlobalVariables.teillisteNote-1))):
			objekt = GlobalVariables.noteList[checkNotesZaehler-1+(10*(GlobalVariables.teillisteNote-1))]
			message += str (checkNotesZaehler+(10*(GlobalVariables.teillisteNote-1))) + ". "+ str (objekt[0].getMessage()) +"\n"
			checkNotesZaehler += 1

		
		if (GlobalVariables.infoWindowOpen is True):
			CheckpointFunktionen.checkPoints(True)

		blackTheme = viz.getTheme()
		blackTheme.borderColor = (0.1,0.1,0.1,.2)
		blackTheme.backColor = (0.4,0.4,0.4,.2)
		blackTheme.lightBackColor = (0.6,0.6,0.6,.2)
		blackTheme.darkBackColor = (0.2,0.2,0.2,.2)
		blackTheme.highBackColor = (0.2,0.2,0.2,.2)

			
		myPanel = vizdlg.Panel(theme = blackTheme, fontSize=13, align=viz.ALIGN_CENTER_TOP, background=False, border=False)
		
		#PanelButtons
		row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0)
		zurueck = row.addItem(viz.addButtonLabel("Zurueck"))
		teillisteView = row.addItem(viz.addText(str(GlobalVariables.teillisteNote) + "/" + str(GlobalVariables.gesamtTeillisteNote)))
		naechste = row.addItem(viz.addButtonLabel("Naechste"))

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
	
		#Add row to myPanel
		myPanel.addItem(row)

		#Add a subgroup containing slider/textbox
		group = vizdlg.Panel(theme=blackTheme, background=False, border=False)


		#Add row for slider to subgroup
		row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0)
		row.addItem(viz.addText(message))
		group.addItem(row)


		myPanel.addItem(group)
		viz.link(viz.RightCenter)
		
		checkNotesVisible = True
		GlobalVariables.infoWindowOpen = True

	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkNotesVisible = False
		myPanel.visible(False)
		if (onViolent is False):
			GlobalVariables.infoWindowOpen = False

#Lösche 3D Notiz
def delete3DNote(menubar):
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		
		menubar.setVisible(viz.OFF)


		#ueberpruefe die Eingabe
		
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			if object is not input.cancel:
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
			else:
				GlobalVariables.windowOpen = False
				input.remove()
	
		#vizdialog
		input = vizdlg.InputDialog(title = "Loesche Notiz", length=1.0, validate = ueberpruefeEingabe)
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
		pass
		
#Zu 3D Notizen porten
def port3DNote(menubar):
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		
		menubar.setVisible(viz.OFF)

		#ueberpruefe die Eingabe
		
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			if object is not input.cancel:
				try:
					if (type(int(data.value)) is int and int(data.value) <= len(GlobalVariables.noteList) and int(data.value )> 0): #Ist die Eingabe im gültigen bereich?
						text = GlobalVariables.noteList[int(data.value)-1][0]
						position = text.getPosition()

						viz.MainView.setPosition(position[0], position[1], position[2]-0.5)
						GlobalVariables.tracker.setPosition(position[0], position[1], position[2]-0.5)

						viz.MainView.setEuler(GlobalVariables.noteList[int(data.value)-1][1], GlobalVariables.noteList[int(data.value)-1][2], GlobalVariables.noteList[int(data.value)-1][3])
						GlobalVariables.tracker.setEuler( GlobalVariables.noteList[int(data.value)-1][1], GlobalVariables.noteList[int(data.value)-1][2], GlobalVariables.noteList[int(data.value)-1][3])
						
						GlobalVariables.euler = tracker.getEuler()
						GlobalVariables.position = tracker.getPosition()
						GlobalVariables.windowOpen = False
						input.remove()
					else:
						data.error = "Bitte nur eine gueltige\nNummer eingeben."
						input.box.setFocus(viz.ON)
				except:
					data.error = "Bitte nur eine gueltige\nNummer eingeben."
					input.box.setFocus(viz.ON)
			else:
				GlobalVariables.windowOpen = False
				input.remove()
	
		#vizdialog
		input = vizdlg.InputDialog(title = "Porte zu Notiz", length=1.0, validate = ueberpruefeEingabe)
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
		pass
