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
        #Falls noch kein Eingabefenster offen
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True

                #verstecke menubar
		menubar.setVisible(viz.OFF)
	
	
		#ueberpruefe die Eingabe und erstelle 3D Text
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			#Falls auf Accept geklickt wurde: ueberpruefe und erstelle
			if object is input.accept:
				#Ist eine Eingabe vorhanden und nicht laenger als 15 Zeichen?
				if (data.value.strip() is not "" and len(str(data.value).strip())<=15):
									
					writeText(data.value) #Funktion fuer Text schreiben

					#Noteliste akutalisieren falls sichtbar
					if (checkNotesVisible is True):
						noteView(False)
						noteView(False)

					#Eingabefenster wieder beenden	
					input.remove()
					GlobalVariables.windowOpen = False

				#Falls keiner oder zu lange Text
				else:
					data.error = "Bitte nur Text eingeben mit\nmaximal 15 Zeichen."
					input.box.setFocus(viz.ON)

			#Falls auf Cancel geklickt wurde: Vorgang abbrechen
			elif object is input.cancel:
				GlobalVariables.windowOpen = False
				input.remove()
			#Falls aus Vesehen auf kein Button geklickt wurde
			else:
				data.error=""
				input.box.setFocus(viz.ON)
	
		#Eingabefenster fuer Texteingabe erstellen
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

		#Fokus auf Textfeld			
		input.box.setFocus(viz.ON)
		
		viztask.schedule(showdialog()) 
		
		
		
		#Text schreiben 
		def writeText(text):
			#Frage User Position und Winkel ab
			userPosition = viz.MainView.getPosition()
			userEuler = viz.MainView.getEuler()
			#Erstelle 3D Text
			text3D = viz.addText3D(text.strip(), pos = [userPosition[0]-0.2, userPosition[1], userPosition[2] + 0.2])
			text3D.setScale(0.2, 0.2, 0.2)
			text3D.color(viz.RED)

			#Fuege 3D Text in Liste ein
			GlobalVariables.noteList.append(Note.Note(userPosition[0]-0.2, userPosition[1], userPosition[2] + 0.2, text3D.getMessage(), \
											round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3)))
			GlobalVariables.noteListObjects.append(text3D)
			GlobalVariables.windowOpen = False
	
#Notizen anzeigen
def noteView(onViolent):
	global checkNotesVisible
	global myPanel
	
	
	if not checkNotesVisible: #Falls Checkboxfenster nicht sichtbar, notes auslesen und ausgeben

		message = []	#Die Liste mit den Texten, die später angezeigt wird
		checkNotesZaehler = 1
		
		#Berechnung der Gesamtteillisten
		if len(GlobalVariables.noteList) >= 10:
			GlobalVariables.gesamtTeillisteNote = (len(GlobalVariables.noteList)/10)+1

		#Füge die Eintraege in "message" ein
		while(checkNotesZaehler <=10 and checkNotesZaehler <= (len(GlobalVariables.noteList))-(10*(GlobalVariables.teillisteNote-1))):
			objekt = GlobalVariables.noteList[checkNotesZaehler-1+(10*(GlobalVariables.teillisteNote-1))]
			message.append(str (checkNotesZaehler+(10*(GlobalVariables.teillisteNote-1))) + ". "+ str (objekt.name) +"\n")
			checkNotesZaehler += 1

		#Schließe checkpoints, wenn offen, da immer nur eins von beiden offen sein darf
		if (GlobalVariables.infoWindowOpen is True):
			CheckpointFunktionen.checkPoints(True)
			
		#Haupt Panel des Checkpointlisten Fensters
		myPanel = vizdlg.Panel(theme = GlobalVariables.blackTheme, fontSize=25, align=viz.ALIGN_RIGHT_CENTER, background=False, border=False)
		
		row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0) # Panel für Navigation
		zurueck = row.addItem(viz.addButtonLabel("Zurueck")) #Button für eine Teilliste zurueck
		teillisteView = row.addItem(viz.addText(str(GlobalVariables.teillisteNote) + "/" + str(GlobalVariables.gesamtTeillisteNote))) #Anzeige in welcher Teilliste von wie vielen Gesamtlisten man sich befindet
		naechste = row.addItem(viz.addButtonLabel("Naechste")) #Button für eine Teilliste vorwaerts

                #Füge Panel in Hauptpanel ein
		myPanel.addItem(row)
		
		#Hauptpanel an die rechte Seite heften
		viz.link(viz.RightCenter, myPanel)
		checkNotesVisible = True
		GlobalVariables.infoWindowOpen = True
		
		#zirkulierendes "Liste"
		def teillisteVerringernErhoehen(wert):
                        #Falls man am Anfang ist und zurueck geht, kommt man am Ende wieder raus
			if GlobalVariables.teillisteNote == 1 and wert == -1:
				GlobalVariables.teillisteNote = GlobalVariables.gesamtTeillisteNote
                        #Falls man am Ende ist und vorwaerts geht, kommt man am Anfang wieder raus
			elif GlobalVariables.teillisteNote == GlobalVariables.gesamtTeillisteNote and wert == 1:
				GlobalVariables.teillisteNote = 1
			else:

				GlobalVariables.teillisteNote = GlobalVariables.teillisteNote+wert
			#NoteView aktualisieren	
			noteView(False)
			noteView(False)

		#Button Funktionsdefinition
		vizact.onbuttondown(zurueck,teillisteVerringernErhoehen, -1)
		vizact.onbuttondown(naechste, teillisteVerringernErhoehen, 1)
	
                #Navigation mit Pfeiltasten darf nur einmal gesetzt werden
		if GlobalVariables.nurEinmalSetzen is False:
			vizact.onkeydown(viz.KEY_LEFT, teillisteVerringernErhoehen, -1)
			vizact.onkeydown(viz.KEY_RIGHT, teillisteVerringernErhoehen, 1)
			GlobalVariables.nurEinmalSetzen = True
	
	

		rowlist = [] #Liste mit den rows
		noteButtons = [] #Liste mit den Buttons
		buttonZaehler = 0

		#Liste Durchlaufen
		for a in message:
			noteButtons.append(viz.addButtonLabel(message[buttonZaehler]))

			#Erstelle Panel fuer den jeweiligen noteButon
			buttonRow = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False, background = False, margin=0)

			buttonRow.addItem(noteButtons[buttonZaehler])#Füge Buttons in die Liste ein
			rowlist.append(buttonRow) #Füge die Row in die Rowlist ein
			myPanel.addItem(rowlist[buttonZaehler])  #Füge die noteRows ins panel ein
			buttonZaehler+=1


		#Erstellen der SubMenu Items
		deleteNoteSub = vizpopup.Item('Loesche Note')
		porteZuNote = vizpopup.Item('Springe zu')
		mymenu = vizpopup.Menu('Main',[deleteNoteSub, porteZuNote])		




		#Zeige subMenu für Note an der Position "position" an
		def subMenu(position):		
			vizpopup.onMenuItem(deleteNoteSub, delete3DNote, position=position)
			vizpopup.onMenuItem(porteZuNote, port3DNote, position=position)
			vizpopup.display(mymenu)
			
			
		#Belege alle Buttons mit submenu anzeigen Funktionen
		i=0
		for a in noteButtons:
			vizact.onbuttonup(noteButtons[i], subMenu, i)
			i+=1

	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkNotesVisible = False
		myPanel.visible(False)
		if (onViolent is False):
			GlobalVariables.infoWindowOpen = False

#Lösche 3D Notiz
def delete3DNote(menubar=None, position = None):
        
        #Falls noch kein Eingabefenster offen
	if (GlobalVariables.windowOpen is False):
                
                #Verstecke menubar
		if menubar is not None:
			menubar.setVisible(viz.OFF)
			
		#ueberpruefe die Eingabe und loesche Note
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)

			#Falls man auf Accept geklickt hat: ueberpruefen und loeschen
			if object is input.accept:
				try:
                                        #Ist die Eingabe ein Integer Wert und in Listenlänge?
					if (type(int(data.value)) is int and int(data.value) <= len(GlobalVariables.noteList) and int(data.value )> 0): #Ist die Eingabe im gültigen bereich?

						GlobalVariables.noteListObjects[int (data.value)-1].remove() #Entferne Notiz aus der Umgebung
						del GlobalVariables.noteList[int (data.value)-1] #Lösche 3D Notiz aus der Liste
						GlobalVariables.windowOpen = False
						
                                                #Eingabefenster entfernen
						input.remove()
						GlobalVariables.windowOpen = False

                                        #Falsche Eingabe
					else:
						data.error = "Bitte nur eine gueltige\nNummer eingeben."
						input.box.setFocus(viz.ON)

                                #Falsche Eingabe
				except:
					data.error = "Bitte nur eine gueltige\nNummer eingeben."
					input.box.setFocus(viz.ON)
			#Falls man auf Cancel geklickt hat: Vorgang abbrechen	
			elif object is input.cancel:
				GlobalVariables.windowOpen = False
				input.remove()

			#Falls man ausversehen nicht auf einen der Buttons geklickt hat
			else:
				data.error=""
				input.box.setFocus(viz.ON)

		#Falls keine Position mit uebergeben wurde, d.h. Funktionsaufruf nicht ueber SubMenu		
		if position is None:
			GlobalVariables.windowOpen = True
			
			#Dialogfenster fuer 3D Note loeschen erstellen
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
			#Fokus auf Textfeld			
                        input.box.setFocus(viz.ON)
                        
			viztask.schedule(showdialog())
			
		#Falls Funktionsaufruf ueber SubMenu	
		else:
                        #Ist die Eingabe im gültigen bereich?
			if (int(position) < len(GlobalVariables.noteList) and int(position)>= 0): 
				print GlobalVariables.noteListObjects
				print int(position)
				GlobalVariables.noteListObjects[int (position)].remove() #Loesche 3D Notiz aus Umgebung
				del GlobalVariables.noteListObjects[int (position)]
				del GlobalVariables.noteList[int (position)] #Loesche 3D Notiz aus Liste

                #NoteView Fenster aktualisieren, falls angezeigt
		if (checkNotesVisible is True):
			noteView(False)
			noteView(False)

		
#Zu 3D Notizen porten
def port3DNote(menubar=None, position=None):
        
	if (GlobalVariables.windowOpen is False):
		#Verstecke Menubar
		if menubar is not None:
			menubar.setVisible(viz.OFF)

		#Ueberpruefe die Eingabe
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			#Falls man auf Accept geklickt hat: ueberpruefen und springen
			if object is input.accept:
				try:
                                        #Ist die Eingabe ein Integer Wert und in Listenlänge?
					if (type(int(data.value)) is int and int(data.value) <= len(GlobalVariables.noteList) and int(data.value )> 0): #Ist die Eingabe im gültigen bereich?
						text = GlobalVariables.noteList[int(data.value)-1] #Lese Note aus Liste aus

                                                #Setze Position
						viz.MainView.setPosition(text.posX, text.posZ, text.posY-0.5)
						GlobalVariables.tracker.setPosition(text.posX, text.posZ, text.posY-0.5)

                                                #Setze Winkel
						viz.MainView.setEuler(text.eulerX, text.eulerZ, text.eulerY)
						GlobalVariables.tracker.setEuler(text.eulerX, text.eulerZ, text.eulerY)

                                        	#Uebergebe neue Position/Winkel an Globale Variablen						
						GlobalVariables.euler = GlobalVariables.tracker.getEuler()
						GlobalVariables.position = GlobalVariables.tracker.getPosition()

						GlobalVariables.windowOpen = False
						input.remove()
					#Falsche Eingabe	
					else:
						data.error = "Bitte nur eine gueltige\nNummer eingeben."
						input.box.setFocus(viz.ON)
				#Falsche Eingabe
				except:
					data.error = "Bitte nur eine gueltige\nNummer eingeben."
					input.box.setFocus(viz.ON)
			#Falls man auf Cancel geklickt hat: Vorgang abbrechen			
			elif object is input.cancel:
				GlobalVariables.windowOpen = False
				input.remove()
			#Falls man ausversehen nicht auf einen der Buttons geklickt hat	
			else:
				data.error=""
				input.box.setFocus(viz.ON)
                #Falls keine Position mit uebergeben wurde, d.h. Funktionsaufruf nicht ueber SubMenu	
		if position is None:
			GlobalVariables.windowOpen = True
			#Dialogfenster fuer zu 3D Note springen erstellen
			input = vizdlg.InputDialog(title = "SPringe zu Notiz", prompt="Notiznummer eingeben", length=1.0, validate = ueberpruefeEingabe)
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
			#Fokus auf Textfeld	
			input.box.setFocus(viz.ON)
			viztask.schedule(showdialog())
			
		else:
                        #Ist die Eingabe in Listenlaenge?
			if (int(position) < len(GlobalVariables.noteList) and int(position)>= 0):
				text = GlobalVariables.noteList[int(position)] #Lese Note aus Liste aus

                                #Setze Position
				viz.MainView.setPosition(text.posX, text.posZ, text.posY-0.5)
				GlobalVariables.tracker.setPosition(text.posX, text.posZ, text.posY-0.5)

                                #Setze Winkel
				viz.MainView.setEuler(text.eulerX, text.eulerZ, text.eulerY)
				GlobalVariables.tracker.setEuler(text.eulerX, text.eulerZ, text.eulerY)

				#Uebergebe neue Position/Winkel an Globale Variablen		
				GlobalVariables.euler = GlobalVariables.tracker.getEuler()
				GlobalVariables.position = GlobalVariables.tracker.getPosition()
