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



#Checkpointliste Fenster
def checkPoints(onViolent):
	global checkPointsVisible	
	global myPanel


	if not checkPointsVisible: 	#Falls Checkboxfenster nicht 
								# sichtbar, checkpoints auslesen und ausgeben
		checkPointZaehler = 1		
		checkpointsPanelList = []#Liste für die icons zum kommentar aufplopen nebend er checkpointliste

		#Berechnung der Gesamtteillisten
		if len(GlobalVariables.checkPointsList) >= 10:
			GlobalVariables.gesamtTeillisteCheckpoint = (len(GlobalVariables.checkPointsList)/10)+1
	
		message = []
	
		while(checkPointZaehler <=10 and checkPointZaehler <= (len(GlobalVariables.checkPointsList))-(10*(GlobalVariables.teillisteCheckpoint-1))):
			objekt = GlobalVariables.checkPointsList[checkPointZaehler-1+(10*(GlobalVariables.teillisteCheckpoint-1))]
			message.append(str (checkPointZaehler+(10*(GlobalVariables.teillisteCheckpoint-1))) + ". "+ str (objekt.name)+"\n    "+ str (objekt.posX) +" "+ str (objekt.posZ) +" "+ str (objekt.posY)  + "\n")
			checkPointZaehler += 1

		
		if (GlobalVariables.infoWindowOpen is True):
			Notes.noteView(True)	#Schließe noteView, wenn offen

		myPanel = vizdlg.Panel(theme = GlobalVariables.blackTheme, fontSize=13, align=viz.ALIGN_RIGHT_CENTER, background=False, border=False)
		
		#PanelButtons
		rowCommentDelete = vizdlg.Panel(border=False,background=False,margin=0)
		commentDelete = rowCommentDelete.addItem(viz.addButtonLabel("x"))
		
		row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0)
		zurueck = row.addItem(viz.addButtonLabel("Zurueck"))
		teillisteView = row.addItem(viz.addText(str(GlobalVariables.teillisteCheckpoint) + "/" + str(GlobalVariables.gesamtTeillisteCheckpoint)))
		naechste = row.addItem(viz.addButtonLabel("Naechste"))

		#zirkulierendes "Liste"
		def teillisteVerringernErhoehen(wert):
			if checkPointsVisible: 
				if GlobalVariables.teillisteCheckpoint == 1 and wert == -1:
					GlobalVariables.teillisteCheckpoint = GlobalVariables.gesamtTeillisteCheckpoint
					GlobalVariables.positionWhichIsActivated = -1
				elif GlobalVariables.teillisteCheckpoint == GlobalVariables.gesamtTeillisteCheckpoint and wert == 1:
					GlobalVariables.teillisteCheckpoint = 1
					GlobalVariables.positionWhichIsActivated = -1

				else:
					GlobalVariables.teillisteCheckpoint = GlobalVariables.teillisteCheckpoint+wert
					GlobalVariables.positionWhichIsActivated = -1

				checkPoints(False)
				checkPoints(False)
		#Kommentar wegmachen
		def deleteComment():
			if GlobalVariables.commentView is not None:
				GlobalVariables.commentPanel.removeItem(GlobalVariables.commentView)
				
			

		#Button action
		vizact.onbuttondown(zurueck,teillisteVerringernErhoehen, -1)
		vizact.onbuttondown(naechste, teillisteVerringernErhoehen, 1)
		vizact.onbuttondown(commentDelete, deleteComment)
		
		if GlobalVariables.nurEinmalSetzen is False:
			vizact.onkeydown(viz.KEY_LEFT, teillisteVerringernErhoehen, -1)
			vizact.onkeydown(viz.KEY_RIGHT, teillisteVerringernErhoehen, 1)
			GlobalVariables.nurEinmalSetzen = True
		
		#Add row to myPanel
		myPanel.addItem(rowCommentDelete)
		myPanel.addItem(row)
		

		rowlist = [] #liste mit den rows
		checkpointButtons = []	#liste mit den buttons
		buttonZaehler = 0
		for a in message:
			checkpointButtons.append(viz.addButtonLabel(message[buttonZaehler]))
			if GlobalVariables.positionWhichIsActivated == buttonZaehler:
				buttonRow = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False, margin=0)
				
			else:
				buttonRow = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False, background = False, margin=0)

			buttonRow.addItem(checkpointButtons[buttonZaehler])
			rowlist.append(buttonRow)
			myPanel.addItem(rowlist[buttonZaehler]) #füge die checkpointbuttonrows ins panel ein
			buttonZaehler+=1

		#Panel für die Kommentare
		
		viz.link(viz.CenterCenter, GlobalVariables.commentPanel)


		#Mache den zeilenumbruch für das Kommentar
		def makeCommentary(position):
				comment = str(GlobalVariables.checkPointsList[position+(10*(GlobalVariables.teillisteCheckpoint-1))].comment)
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


		#Zeige Kommentar an
		def showComment(position):
			
			if GlobalVariables.commentWindowOpen is False:
				GlobalVariables.commentWindowOpen = True
				GlobalVariables.commentView = GlobalVariables.commentPanel.addItem(viz.addText(makeCommentary(position)))
				print GlobalVariables.commentPanel.getItems()
				GlobalVariables.commentPanel.visible(True)
				GlobalVariables.positionWhichIsActivated = position
				
			elif GlobalVariables.commentWindowOpen is True and position is not GlobalVariables.positionWhichIsActivated:
				print GlobalVariables.commentPanel.getItems()
				GlobalVariables.commentPanel.removeItem(GlobalVariables.commentView)
				GlobalVariables.commentView = GlobalVariables.commentPanel.addItem(viz.addText(makeCommentary(position)))
				GlobalVariables.positionWhichIsActivated = position
			else:
				GlobalVariables.commentWindowOpen = False
				GlobalVariables.commentPanel.visible(False)
			checkPoints(False)
			checkPoints(False)
				

		showCommentary = vizpopup.Item('Zeige Kommentar')
		porteZuCheckpoint = vizpopup.Item('Springe zu')
		mymenu = vizpopup.Menu('Main',[showCommentary, porteZuCheckpoint])		

		#Zeige subMenu an
		def subMenu(position):		
			vizpopup.onMenuItem(showCommentary, showComment, position)
			vizpopup.onMenuItem(porteZuCheckpoint, portCheckPoint, checkPointNummer=position)
			vizpopup.display(mymenu)
			
			
		#belege die ganzen Buttons mit comment anzeigen funktionen
		i=0
		for a in checkpointButtons:
			vizact.onbuttonup(checkpointButtons[i], subMenu, i)
			i+=1
			
		viz.link(viz.RightCenter,myPanel)
		checkPointsVisible = True
		GlobalVariables.infoWindowOpen = True

	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkPointsVisible = False
		myPanel.visible(False)
		if (onViolent is False):
			GlobalVariables.infoWindowOpen = False
			
		

#Checkpoint erstellen/speichern
def createCheckpoint(menubar=None):
	global checkPointsVisible
	
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		userPosition = viz.MainView.getPosition() #Frage User Position
		userEuler = viz.MainView.getEuler()			#Frage User Kamerawinkel
		if menubar is not None:
			menubar.setVisible(viz.OFF)

		def checkpointHinzufuegen(data):
			object = viz.pick(0,viz.SCREEN)
			
			if object is input.accept:
				if len(str(data.value).split("//")[0])<=15:
					#Füge Checkpoint zur Liste auf 3 Nachkommastellen gerundet an

						if (len(str(data.value).split("//"))==1):#wenn kein kommentar eingegeben wurde
							checkpoint = Checkpoint.Checkpoint(round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3), str(data.value).split("//")[0],\
							round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3))
						else:#wenn ein kommentar eingegeben wurde
							checkpoint = Checkpoint.Checkpoint(round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3), str(data.value).split("//")[0],\
							round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3), str(data.value).split("//")[1])	
							
						GlobalVariables.checkPointsList.append(checkpoint)
						GlobalVariables.windowOpen = False		
						input.remove()
				else:
					data.error = "Bitte den Namen nicht laenger\nals 15 Zeichen machen."
					
				
			elif object is input.cancel:
				GlobalVariables.windowOpen = False		
				input.remove()
			
			else:
				vizact.ontimer2(0.1, 0, input.box.setFocus, viz.ON)
						
			#akutalisiere die Liste, wenn sie angezeigt wird
			if (checkPointsVisible is True):
				checkPoints(False)
				checkPoints(False)
			


		#vizdialog
		input = vizdlg.InputDialog(title='Neuer Checkpoint', prompt="Eingabeformat:\n\"Name//Kommentar\"",length=1.0, validate = checkpointHinzufuegen)
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
					
		vizact.ontimer2(0.1, 0, input.box.setFocus, viz.ON) #Fokus auf Textfeld
		viztask.schedule(showdialog()) 

	else:
		pass
	
#Lösche Checkpoint
def deleteCheckpoint(menubar=None, position=None):
	global fensterOpen	
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		if menubar is not None:
			menubar.setVisible(viz.OFF)
		
		#ueberpruefe die Eingabe
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			if object is not input.cancel:
				try:
					if (type(int(data.value)) is int and len(GlobalVariables.checkPointsList) >= int(data.value) and int(data.value) >0 ): #Ist die Eingabe in Listenlänge?
						del GlobalVariables.checkPointsList[int (data.value)-1] #Lösche Checkpoint
						if (checkPointsVisible is True):
							checkPoints(False)
							checkPoints(False)
						input.remove()
						GlobalVariables.windowOpen = False

					else:
						data.error = "Biite nur Zahlen im Bereich der \nverfuegbaren Checkpoints."
						input.box.setFocus(viz.ON)
				except:
					data.error = "Biite nur Zahlen im Bereich der \nverfuegbaren Checkpoints."
					input.box.setFocus(viz.ON)
			else:
				GlobalVariables.windowOpen = False
				input.remove()
		
		#vizdialog
		input = vizdlg.InputDialog(title = "Loesche Checkpoint", prompt="\"Checkpointnummer\"", length=1.0, validate = ueberpruefeEingabe)
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

#Zu Checkpoints porten
def portCheckPoint(menubar=None, checkPointNummer = None):
	
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		if menubar is not None:
			menubar.setVisible(False)
			
		def porteCheckpoint(checkPointNummer):
				point = GlobalVariables.checkPointsList[int(checkPointNummer)-1]
				
				#Setze Position
				viz.MainView.setPosition(point.posX, point.posZ, point.posY)
				GlobalVariables.tracker.setPosition(point.posX, point.posZ, point.posY)
				
				#Setze Winkel
				viz.MainView.setEuler(point.eulerX,point.eulerZ, point.eulerY)
				GlobalVariables.tracker.setEuler(point.eulerX, point.eulerZ, point.eulerY)
				
				GlobalVariables.euler = GlobalVariables.tracker.getEuler()
				GlobalVariables.position = GlobalVariables.tracker.getPosition()
				GlobalVariables.windowOpen = False	
			
		
		if checkPointNummer is None:
			#ueberpruefe die Eingabe
			
			def ueberpruefeEingabe(data):
				object = viz.pick(0,viz.SCREEN)
				if object is not input.cancel:
					try:
						if (type(int(data.value)) is int and len(GlobalVariables.checkPointsList) >= int(data.value) and int(data.value) >0 ): #Ist die Eingabe in Listenlänge?
							porteCheckpoint(data.value)
							input.remove()
							GlobalVariables.windowOpen = False

						else:
							data.error = "Biite nur Zahlen im Bereich der \nverfuegbaren Checkpoints."
							input.box.setFocus(viz.ON)
					except:
						data.error = "Biite nur Zahlen im Bereich der \nverfuegbaren Checkpoints."
						input.box.setFocus(viz.ON)
				else:
					GlobalVariables.windowOpen = False
					input.remove()	
			
			#vizdialog
			input = vizdlg.InputDialog(title='Porte zu Checkpoint', length=1.0, validate = ueberpruefeEingabe)
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
			vizact.ontimer2(0.1, 0, input.box.setFocus, viz.ON)
			viztask.schedule(showdialog()) 
			
			
		else:
			porteCheckpoint(checkPointNummer)

#######		Android Funktionen 		#########

def getCheckpointsAndroid():
	return GlobalVariables.checkPointsList



def createCheckpointAndroid(name="", comment=""):
	userPosition = viz.MainView.getPosition() #Frage User Position
	userEuler = viz.MainView.getEuler()			#Frage User Kamerawinkel
	#Füge Checkpoint zur Liste auf 3 Nachkommastellen gerundet an	
	checkpoint = Checkpoint.Checkpoint(round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3), str(name),\
	round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3), str(comment))
	GlobalVariables.checkPointsList.append(checkpoint)
	checkPoints(False)
	checkPoints(False)
	
def deleteCheckpointAndroid(checkpointNummer):
	try:
		if (len(GlobalVariables.checkPointsList) >= int(checkpointNummer) and int(checkpointNummer) >0 ): #Ist die Eingabe in Listenlänge?
			del GlobalVariables.checkPointsList[int (checkpointNummer)-1] #Lösche Checkpoint
			print "test"
			checkPoints(False)
			checkPoints(False)
		else:
			return False
	except:
		return False
		
def porteCheckpointAndroid(checkpointNummer):

		#if (type(int(checkpointNummer)) is int and len(GlobalVariables.checkPointsList) >= int(checkpointNummer) and int(checkpointNummer) >0 ): #Ist die Eingabe in Listenlänge?
			point = GlobalVariables.checkPointsList[int(checkpointNummer)-1]
			
			#Setze Position
			viz.MainView.setPosition(point.posX, point.posZ, point.posY)
			GlobalVariables.tracker.setPosition(point.posX, point.posZ, point.posY)
			
			#Setze Winkel
			viz.MainView.setEuler(point.eulerX,point.eulerZ, point.eulerY)
			GlobalVariables.tracker.setEuler(point.eulerX, point.eulerZ, point.eulerY)
			
			GlobalVariables.euler = GlobalVariables.tracker.getEuler()
			GlobalVariables.position = GlobalVariables.tracker.getPosition()

		