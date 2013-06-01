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

import CheckpointFunktionen
import GlobalVariables

checkNotesVisible = False
noteList = []


#Setze Text an eigener Position
def openTextBox(menubar):
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True

		menubar.setVisible(viz.OFF)
	
	
		#ueberpruefe die Eingabe
		
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			if object is not input.cancel:
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
			else:
				GlobalVariables.windowOpen = False
				input.remove()
	
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
			noteList.append([text3D, round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3)])
			GlobalVariables.windowOpen = False
			
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
			CheckpointFunktionen.checkPoints(True)
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
		
		menubar.setVisible(viz.OFF)


		#ueberpruefe die Eingabe
		
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			if object is not input.cancel:
				try:
					if (type(int(data.value)) is int and int(data.value) <= len(noteList) and int(data.value )> 0): #Ist die Eingabe im gültigen bereich?
						noteList[int (data.value)-1][0].remove()
						del noteList[int (data.value)-1] #Lösche 3D Notiz
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
def port3DNote(tracker, menubar):
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		
		menubar.setVisible(viz.OFF)

		#ueberpruefe die Eingabe
		
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			if object is not input.cancel:
				try:
					if (type(int(data.value)) is int and int(data.value) <= len(noteList) and int(data.value )> 0): #Ist die Eingabe im gültigen bereich?
						text = noteList[int(data.value)-1][0]
						position = text.getPosition()

						viz.MainView.setPosition(position[0], position[1], position[2]-0.5)
						tracker.setPosition(position[0], position[1], position[2]-0.5)

						viz.MainView.setEuler(noteList[int(data.value)-1][1], noteList[int(data.value)-1][2], noteList[int(data.value)-1][3])
						tracker.setEuler( noteList[int(data.value)-1][1], noteList[int(data.value)-1][2], noteList[int(data.value)-1][3])
						
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
