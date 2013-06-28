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

import GlobalVariables
import Checkpoint
import Notes

checkPointsVisible = False
myPanel = vizdlg.Panel()


def checkPoints(onViolent):
        """Checkpointliste Fenster anzeigen"""
        
	global checkPointsVisible	
	global myPanel

       # """Falls Checkboxfenster nicht sichtbar, checkpoints auslesen und ausgeben"""
	if not checkPointsVisible: 	
			
		checkPointZaehler = 1		

		#"""Berechnung der Gesamtteillisten"""
		#"""Jede Teilliste besteht aus maximal 10 Einträgen"""
		if len(GlobalVariables.checkPointsList) >= 10: 
			GlobalVariables.gesamtTeillisteCheckpoint = (len(GlobalVariables.checkPointsList)/10)+1

               # """Die Liste mit den Texten, die später auf den Buttons stehen"""
		message = [] 
		
		#"""Füge die Eintraege in "message" ein"""
		#"""Nicht mehr als 10 Einträge pro Teilliste"""
		while(checkPointZaehler <=10 and checkPointZaehler <= (len(GlobalVariables.checkPointsList))-(10*(GlobalVariables.teillisteCheckpoint-1))): 
			objekt = GlobalVariables.checkPointsList[checkPointZaehler-1+(10*(GlobalVariables.teillisteCheckpoint-1))] #:Lese Checkpoint Objekt aus der Checkpoint Liste aus
                        #"""Füge Text in die Liste ein"""
			message.append(str (checkPointZaehler+(10*(GlobalVariables.teillisteCheckpoint-1))) + ". "+ str (objekt.name)+"\n") 
			
			checkPointZaehler += 1

		#"""Schließe noteView, wenn offen, da immer nur eins von beiden offen sein darf"""
		if (GlobalVariables.infoWindowOpen is True):
			Notes.noteView(True)	

		#"""Haupt Panel des Checkpointlisten Fensters"""
		myPanel = vizdlg.Panel(theme = GlobalVariables.blackTheme, fontSize=25, align=viz.ALIGN_RIGHT_CENTER, background = False, border = False)
		
		rowCommentDelete = vizdlg.Panel(border=False,background=False,margin=0) #:Panel für den Kommentar entfernen Button
		commentDelete = rowCommentDelete.addItem(viz.addButtonLabel("x")) #:Kommentar entfernen Button
		
		row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0) #:Panel für Navigation
		zurueck = row.addItem(viz.addButtonLabel("Zurueck")) #:Button für eine Teilliste zurueck
		teillisteView = row.addItem(viz.addText(str(GlobalVariables.teillisteCheckpoint) + "/" + str(GlobalVariables.gesamtTeillisteCheckpoint)))#:Anzeige in welcher Teilliste von wie vielen Gesamtlisten man sich befindet
		naechste = row.addItem(viz.addButtonLabel("Naechste"))#:Button für eine Teilliste vorwaerts


		
		#"""Füge alle Panels in Hauptpanel ein"""
		myPanel.addItem(rowCommentDelete)
		myPanel.addItem(row)

		#"""Hauptpanel an die rechte Seite heften"""			
		viz.link(viz.RightCenter,myPanel)
		checkPointsVisible = True
		GlobalVariables.infoWindowOpen = True
		
		
		def teillisteVerringernErhoehen(wert):
                        """zirkulierendes Liste implementieren"""
                        
			if checkPointsVisible:
				#"""Falls man am Anfang ist und zurueck geht, kommt man am Ende wieder raus"""
				if GlobalVariables.teillisteCheckpoint == 1 and wert == -1: 
					GlobalVariables.teillisteCheckpoint = GlobalVariables.gesamtTeillisteCheckpoint
				#"""Falls man am Ende ist und vorwaerts geht, kommt man am Anfang wieder raus"""	
				elif GlobalVariables.teillisteCheckpoint == GlobalVariables.gesamtTeillisteCheckpoint and wert == 1:
					GlobalVariables.teillisteCheckpoint = 1
					
				else:
					GlobalVariables.teillisteCheckpoint = GlobalVariables.teillisteCheckpoint+wert

				#"""Checkpointfenster aktualisieren"""
				checkPoints(False)
				checkPoints(False)
				
		
		def deleteComment():
                        """Kommentar entfernen"""
                        
			#"""Falls ein Kommentar angezeigt wird"""
			if GlobalVariables.commentView is not None:
				#"""Entferne Kommentar"""
				GlobalVariables.commentPanel.removeItem(GlobalVariables.commentView)
				GlobalVariables.positionWhichIsActivated = -1
				GlobalVariables.commentPanel.visible(viz.OFF)
				
				#"""Checkpointfenster aktualisieren"""
				checkPoints(False)
				checkPoints(False)
			

		#"""Button Funktionsdefinition"""
		vizact.onbuttondown(zurueck,teillisteVerringernErhoehen, -1)
		vizact.onbuttondown(naechste, teillisteVerringernErhoehen, 1)
		vizact.onbuttondown(commentDelete, deleteComment)

		#"""Navigation mit Pfeiltasten darf nur einmal gesetzt werden"""
		if GlobalVariables.nurEinmalSetzen is False:
			vizact.onkeydown(viz.KEY_LEFT, teillisteVerringernErhoehen, -1)
			vizact.onkeydown(viz.KEY_RIGHT, teillisteVerringernErhoehen, 1)
			GlobalVariables.nurEinmalSetzen = True

		
		rowlist = [] #:Liste mit den rows
		checkpointButtons = []#:Liste mit den Buttons
		buttonZaehler = 0

		#"""Liste durchlaufen"""
		for a in message:
			checkpointButtons.append(viz.addButtonLabel(message[buttonZaehler]))
			#"""Falls von einem Checkpoint der Kommentar angezeigt wird, diesen Button farblich hinterlegen"""
			if GlobalVariables.positionWhichIsActivated == (buttonZaehler+(10*(GlobalVariables.teillisteCheckpoint-1))) and GlobalVariables.commentWindowOpen is True:
				buttonRow = vizdlg.Panel(theme = GlobalVariables.gewaehltTheme, layout=vizdlg.LAYOUT_HORZ_BOTTOM, margin=2)
			else:
				buttonRow = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False, background = False, margin=0)
                       # """Füge Buttons in die Liste ein""" 
			buttonRow.addItem(checkpointButtons[buttonZaehler])
			#"""Füge die Row in die Rowlist ein"""
			rowlist.append(buttonRow) 
			#"""Füge die checkpointbuttonrows ins panel ein"""
			myPanel.addItem(rowlist[buttonZaehler]) 
			buttonZaehler+=1

		if GlobalVariables.commentPanel is not None:
		#"""Panel für die Kommentare in die Mitte des Bildschirms"""
			viz.link(viz.CenterCenter, GlobalVariables.commentPanel)


		
		def makeCommentary(position):
				"""Mache den zeilenumbruch für das Kommentar"""

				#"""Kommentar des Checkpoints an Position "position" auslesen"""
				comment = str(GlobalVariables.checkPointsList[position+(10*(GlobalVariables.teillisteCheckpoint-1))].comment.strip()) 

				#"""Kommentar so formatieren, dass es nach einer bestimmten Länge am letzten Wort einen Zeilenumbruch einfügt"""
				comment = comment.split(" ")
				counter = 0
				commentGesamt = ""
				while counter < len(comment):
					commentGesamt += " "+comment[counter]
					
					letzterUmbruch = commentGesamt.rfind("\n")
					differenz = len(commentGesamt)-letzterUmbruch
					
					if differenz > 30:
						commentGesamt += "\n"
					counter+=1
				return commentGesamt


		
		def showComment(position):
                        """Zeige Kommentar an"""
                        
			#"""Falls kein Kommentar angezeigt wird, das ausgewaehlte anzeigen"""
			if GlobalVariables.commentWindowOpen is False:
				GlobalVariables.commentWindowOpen = True
				GlobalVariables.commentView = GlobalVariables.commentPanel.addItem(viz.addText(makeCommentary(position), fontSize=25))
				GlobalVariables.commentPanel.visible(True)
				GlobalVariables.positionWhichIsActivated = position
				GlobalVariables.commentPanel.visible(viz.ON)
			#"""Falls ein Kommentar bereits angezeigt wird, das alte entfernen und ein neues Kommentar anzeigen"""
			elif GlobalVariables.commentWindowOpen is True and position is not GlobalVariables.positionWhichIsActivated:
				GlobalVariables.commentPanel.removeItem(GlobalVariables.commentView)
				GlobalVariables.commentView = GlobalVariables.commentPanel.addItem(viz.addText(makeCommentary(position), fontSize=25))
				GlobalVariables.positionWhichIsActivated = position
				GlobalVariables.commentPanel.visible(viz.ON)
			#"""Angezeigtes Kommentar entfernen"""
			else:
				GlobalVariables.commentWindowOpen = False
				GlobalVariables.commentPanel.visible(False)
				GlobalVariables.commentPanel.removeItem(GlobalVariables.commentView)
			#"""Checkpointfenster aktualisieren"""
			checkPoints(False)
			checkPoints(False)
				

		#"""Erstellen der SubMenu Items"""
		showCommentary = vizpopup.Item('Zeige Kommentar')
		deleteCheckpointSub = vizpopup.Item('Loesche Checkpoint')
		porteZuCheckpoint = vizpopup.Item('Springe zu')
		mymenu = vizpopup.Menu('Main',[showCommentary, deleteCheckpointSub, porteZuCheckpoint])		

		
		def subMenu(position):
                        """Zeige subMenu für Checkpoint an der Position "position" an"""
                        
			vizpopup.onMenuItem(showCommentary, showComment, position)
			vizpopup.onMenuItem(deleteCheckpointSub, deleteCheckpointAndroid, position)
			vizpopup.onMenuItem(porteZuCheckpoint, porteCheckpointAndroid, position)
			vizpopup.display(mymenu)
			
			
		#"""belege alle Buttons mit SubMenu anzeigen Funktionen"""
		i=0
		for a in checkpointButtons:
			vizact.onbuttonup(checkpointButtons[i], subMenu, i)
			i+=1
       # """Falls Checkboxfenster sichtbar, unsichtbar machen"""
	else: 
		checkPointsVisible = False
		myPanel.visible(False)
		if (onViolent is False):
			GlobalVariables.infoWindowOpen = False
			
		

def createCheckpoint(menubar=None):
        """Checkpoint erstellen"""
        
	global checkPointsVisible
	#"""Falls noch kein Fenster offen ist"""
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		userPosition = viz.MainView.getPosition()
		userEuler = viz.MainView.getEuler()	

               # """Verstecke menubar"""
		if menubar is not None:
			menubar.setVisible(viz.OFF)

                
		def checkpointHinzufuegen(data):
                        """Ueberpruefe eingabe und fuege Checkpoint hinzu"""
                        
			object = viz.pick(0,viz.SCREEN)
			#"""Falls man auf Accept geklickt hat: ueberpruefen und erstellen"""
			if object is input.accept: 

				#"""Name des Checkpoints darf nicht laenger als 15 Zeichen sein"""
				if len(str(data.value).split("//")[0])<=15: 

						
						#"""Füge Checkpoint zur Liste auf 3 Nachkommastellen gerundet an"""
						#"""Wenn kein Kommentar eingegeben wurde"""
						if (len(str(data.value).split("//"))==1):
							checkpoint = Checkpoint.Checkpoint(round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3), str(data.value).split("//")[0],\
							round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3))

						#"""Wenn ein kommentar eingegeben wurde"""
						else:   
							checkpoint = Checkpoint.Checkpoint(round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3), str(data.value).split("//")[0],\
							round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3), str(data.value).split("//")[1])	

						#"""Neuen Checkpoint zur Liste hinzfuegen"""	
						GlobalVariables.checkPointsList.append(checkpoint)
						GlobalVariables.windowOpen = False		
						input.remove()

				#"""Falls der Checkpointname laenger als 15 Zeichen ist"""
				else:
					data.error = "Bitte den Namen nicht laenger\nals 15 Zeichen machen."
					input.box.setFocus(viz.ON)

			#"""Falls man auf Cancel geklickt hat: abbrechen und Fenster schließen"""
			elif object is input.cancel:
				GlobalVariables.windowOpen = False		
				input.remove()

			#"""Falls man ausversehen nicht auf einen der Buttons geklickt hat"""
			else:
				data.error = ""
				input.box.setFocus(viz.ON)
				

			#"""Checkpointfenster aktualisieren, falls angezeigt"""
			if (checkPointsVisible is True):
				checkPoints(False)
				checkPoints(False)

		#"""Dialogfenster fuer neuen Checkpoint erstellen"""
		input = vizdlg.InputDialog(title='Neuer Checkpoint', prompt="Eingabeformat:\n\"Name//Kommentar\"", length=1.0, validate = checkpointHinzufuegen)
		viz.link(viz.CenterCenter,input)
		input.box.overflow(viz.OVERFLOW_SHRINK)
		input.box.setLength(4)
		input.alpha(0.4)
		input.color(0,0,0)
		
		def showdialog():
			yield input.show()
			
			while True:	 
				if input.accepted:
					break
				else:
					break

		#"""Fokus auf Textfeld"""		
		input.box.setFocus(viz.ON)
		
		viztask.schedule(showdialog()) 


	

def deleteCheckpoint(menubar=None):
        """Lösche Checkpoint"""
        
	global fensterOpen
	
	#"""Falls noch kein Fenster offen ist"""
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True

		#"""Verstecke menubar"""
		if menubar is not None:
			menubar.setVisible(viz.OFF)
		
		
		def ueberpruefeEingabe(data):
                        """Ueberpruefe die Eingabe und loesche Checkpoint"""
                        
			object = viz.pick(0,viz.SCREEN)

			#"""Falls man auf Accept geklickt hat: ueberpruefen und loeschen"""
			if object is input.accept:
				try:
					#"""Ist die Eingabe ein Integer Wert und in Listenlänge?"""
					if (type(int(data.value)) is int and len(GlobalVariables.checkPointsList) >= int(data.value) and int(data.value) >0 ): 

						#"""Loesche Checkpoint"""
						del GlobalVariables.checkPointsList[int (data.value)-1]

						#"""Checkpointfenster aktualisieren, falls angezeigt"""
						if (checkPointsVisible is True):
							checkPoints(False)
							checkPoints(False)

						#"""Eingabefenster entfernen"""
						input.remove()
						GlobalVariables.windowOpen = False

					#"""Falsche Eingabe"""
					else:
						data.error = "Biite nur Zahlen im Bereich der \nverfuegbaren Checkpoints."
						input.box.setFocus(viz.ON)

				#"""Falsche Eingabe"""		
				except:
					data.error = "Biite nur Zahlen im Bereich der \nverfuegbaren Checkpoints."
					input.box.setFocus(viz.ON)

			#"""Falls man auf Cancel geklickt hat: Vorgang abbrechen"""
			elif object is input.cancel:
				GlobalVariables.windowOpen = False
				input.remove()
			#"""Falls man ausversehen nicht auf einen der Buttons geklickt hat"""
			else:
				data.error=""
				input.box.setFocus(viz.ON)
		
		#"""Dialogfenster fuer Checkpoint loeschen erstellen"""
		input = vizdlg.InputDialog(title = "Loesche Checkpoint", prompt="Checkpointnummer eingeben", length=1.0, validate = ueberpruefeEingabe)
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

		#"""Fokus auf Textfeld"""			
		input.box.setFocus(viz.ON)
		
		viztask.schedule(showdialog()) 



def portCheckPoint(menubar=None):
        """Zu Checkpoints porten"""

	#"""Falls noch kein Fenster offen ist"""
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True

		#"""Verstecke menubar"""
		if menubar is not None:
			menubar.setVisible(False)

		
		def porteCheckpoint(checkPointNummer):
                        #"""Springe zu eingegeben Checkpoint"""
                        
			#"""Lese Checkpoint aus Liste aus"""
			point = GlobalVariables.checkPointsList[int(checkPointNummer)-1]
				
			#"""Setze Position"""
			viz.MainView.setPosition(point.posX, point.posZ, point.posY)
			GlobalVariables.tracker.setPosition(point.posX, point.posZ, point.posY)
				
			#"""Setze Winkel"""
			viz.MainView.setEuler(point.eulerX,point.eulerZ, point.eulerY)
			GlobalVariables.tracker.setEuler(point.eulerX, point.eulerZ, point.eulerY)

			#"""Uebergebe neue Position/Winkel an Globale Variablen"""
			GlobalVariables.euler = GlobalVariables.tracker.getEuler()
			GlobalVariables.position = GlobalVariables.tracker.getPosition()

			GlobalVariables.windowOpen = False	
			
		
		def ueberpruefeEingabe(data):
                        """Ueberpruefe die Eingabe"""
                        
			object = viz.pick(0,viz.SCREEN)
			#"""Falls man auf Accept geklickt hat: ueberpruefen und springen"""
			if object is input.accept:
				try:
                                       #"""Ist die Eingabe ein Integer Wert und in Listenlänge?"""
                                       #"""Ist die Eingabe in Listenlänge?"""
					if (type(int(data.value)) is int and len(GlobalVariables.checkPointsList) >= int(data.value) and int(data.value) >0 ): 
                                                 #"""Springe zu Checkpoint"""
						porteCheckpoint(data.value)

						#"""Entferne Eingabefenster"""
						input.remove()
						GlobalVariables.windowOpen = False

                                        #"""Falsche Eingabe"""
					else:
						data.error = "Biite nur Zahlen im Bereich der \nverfuegbaren Checkpoints."
						input.box.setFocus(viz.ON)
                                #"""Falsche Eingabe"""
				except:
					data.error = "Biite nur Zahlen im Bereich der \nverfuegbaren Checkpoints."
					input.box.setFocus(viz.ON)
			#"""Falls man auf Cancel geklickt hat: Vorgang abbrechen	"""
			elif object is input.cancel:
				GlobalVariables.windowOpen = False
				input.remove()
				
			#"""Falls man ausversehen nicht auf einen der Buttons geklickt hat"""	
			else:
				data.error=""
				input.box.setFocus(viz.ON)
			
		#"""Dialogfenster fuer zu Checkpoint springen erstellen"""
		input = vizdlg.InputDialog(title='Springe zu Checkpoint', prompt="Checkpointnummer eingeben", length=1.0, validate = ueberpruefeEingabe)
		viz.link(viz.CenterCenter,input)
		input.alpha(0.4)
		input.color(0,0,0)
			
		def showdialog():
			yield input.show()
			while True:
				if input.accepted:
					break
				else:
					break
		#"""Fokus auf Textfeld"""		
		input.box.setFocus(viz.ON)
		
		viztask.schedule(showdialog()) 
				



def getCheckpointsAndroid():
        """Gebe Liste mit Checkpoint zurueck"""
        
	return GlobalVariables.checkPointsList



def createCheckpointAndroid(name="", comment=""):
        """Erstelle neuen Checkpoint"""
        
	userPosition = viz.MainView.getPosition() 
	userEuler = viz.MainView.getEuler()	
	
	#"""Fuege Checkpoint zur Liste auf 3 Nachkommastellen gerundet an"""
	checkpoint = Checkpoint.Checkpoint(round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3), str(name),\
	round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3), str(comment))

	#"""Fuege Checkpoint in Liste ein"""
	GlobalVariables.checkPointsList.append(checkpoint)

	#"""Checkpointfenster aktualisieren, falls angezeigt"""
	if (checkPointsVisible is True):
		checkPoints(False)
		checkPoints(False)


def deleteCheckpointAndroid(checkpointNummer):
        """Loesche Checkpoint"""

       # """Ist die Eingabe in Listenlaenge?"""
        if (len(GlobalVariables.checkPointsList) > int(checkpointNummer) and int(checkpointNummer) >=0 ):
			#"""Loesche Checkpoint"""
			del GlobalVariables.checkPointsList[int (checkpointNummer)]
		
			#"""Checkpointfenster aktualisieren, falls angezeigt"""
			if (checkPointsVisible is True):
				checkPoints(False)
				checkPoints(False)


        		
def porteCheckpointAndroid(checkpointNummer):
        """Zu Checkpoint porten"""
        
	#"""Ist die Eingabe in Listenlaenge?"""
	if (len(GlobalVariables.checkPointsList) > int(checkpointNummer) and int(checkpointNummer) >=0 ): 
		#"""Lese Checkpoint aus Liste aus"""
		point = GlobalVariables.checkPointsList[int(checkpointNummer)]
		
		#"""Setze Position"""
		viz.MainView.setPosition(point.posX, point.posZ, point.posY)
		GlobalVariables.tracker.setPosition(point.posX, point.posZ, point.posY)
			
		#"""Setze Winkel"""
		viz.MainView.setEuler(point.eulerX,point.eulerZ, point.eulerY)
		GlobalVariables.tracker.setEuler(point.eulerX, point.eulerZ, point.eulerY)

		#"""Uebergebe neue Position/Winkel an Globale Variablen"""
		GlobalVariables.euler = GlobalVariables.tracker.getEuler()
		GlobalVariables.position = GlobalVariables.tracker.getPosition()

		
