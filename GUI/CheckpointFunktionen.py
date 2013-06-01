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

import GlobalVariables
import Checkpoint
import Notes

checkPointsVisible = False


#Checkpointliste Fenster
def checkPoints(onViolent):
	global checkPointsVisible
	global checkPointsPanel
	
	
	if not checkPointsVisible: 	#Falls Checkboxfenster nicht 
		message = ""			# sichtbar, checkpoints auslesen und ausgeben
		checkPointZaehler = 1
		for a in GlobalVariables.checkPointsList: #Checkpoints zusammenschreiben
			message += str (checkPointZaehler) + ". "+ str (a.name)+"\n    "+ str (a.posX) +" "+ str (a.posZ) +" "+ str (a.posY)  + "\n"
			checkPointZaehler += 1
		if (GlobalVariables.infoWindowOpen is True):
			Notes.noteView(True)	#Schließe noteView, wenn offen
		
		checkPointsPanel = vizinfo.InfoPanel("Checkpoints:\n" + message,align=viz.ALIGN_RIGHT_CENTER,fontSize=15,icon=False,key=None)
		checkPointsVisible = True
		checkPointsPanel.visible(True)
		GlobalVariables.infoWindowOpen = True

	else: #Falls Checkboxfenster sichtbar, unsichtbar machen
		checkPointsVisible = False
		checkPointsPanel.visible(False)
		if (onViolent is False):
			GlobalVariables.infoWindowOpen = False
			
		

#Checkpoint erstellen/speichern
def createCheckpoint(menubar):
	
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		userPosition = viz.MainView.getPosition() #Frage User Position
		userEuler = viz.MainView.getEuler()
		menubar.setVisible(viz.OFF)

		def checkpointHinzufuegen(data):
			object = viz.pick(0,viz.SCREEN)
			if object is not input.cancel:
				#Füge Checkpoint zur Liste auf 3 Nachkommastellen gerundet an	
				checkpoint = Checkpoint.Checkpoint(round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3), str (data.value),\
				round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3))
				GlobalVariables.checkPointsList.append(checkpoint)
				#GlobalVariables.checkPointsList.append([round(userPosition[0],3), round(userPosition[1],3), round(userPosition[2],3), str (data.value), \
				#round(userEuler[0], 3), round(userEuler[1], 3), round(userEuler[2], 3)])
			
			GlobalVariables.windowOpen = False		
			input.remove()
			if (checkPointsVisible is True):
				checkPoints(False)
				checkPoints(False)
			


		#vizdialog
		input = vizdlg.InputDialog(title='Kommentar zum Checkpoint', length=1.0, validate = checkpointHinzufuegen)
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
		pass
	
#Lösche Checkpoint
def deleteCheckpoint(menubar):
	global fensterOpen	
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		menubar.setVisible(viz.OFF)
		
		#ueberpruefe die Eingabe
		
		def ueberpruefeEingabe(data):
			object = viz.pick(0,viz.SCREEN)
			if object is not input.cancel:
				try:
					if (type(int(data.value)) is int and len(GlobalVariables.checkPointsList) >= int(data.value) and int(data.value) >0 ): #Ist die Eingabe in Listenlänge?
						deleteCheckpoint1(data.value)
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
		input = vizdlg.InputDialog(title = "Loesche Checkpoint", length=1.0, validate = ueberpruefeEingabe)
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

		
		#Checkpoint löschen
		def deleteCheckpoint1(checkpointnummer):
			del GlobalVariables.checkPointsList[int (checkpointnummer)-1] #Lösche Checkpoint
		
	else:
		pass

#Zu Checkpoints porten
def portCheckPoint(tracker, menubar):
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		menubar.setVisible(False)
		
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
		
		def porteCheckpoint(checkPointNummer):
			point = GlobalVariables.checkPointsList[int(checkPointNummer)-1]
			
			#Setze Position
			viz.MainView.setPosition(point.posX, point.posZ, point.posY)
			tracker.setPosition(point.posX, point.posZ, point.posY)
			
			#Setze Winkel
			viz.MainView.setEuler(point.eulerX,point.eulerZ, point.eulerY)
			tracker.setEuler(point.eulerX, point.eulerZ, point.eulerY)
			
			GlobalVariables.euler = tracker.getEuler()
			GlobalVariables.position = tracker.getPosition()
			GlobalVariables.windowOpen = False
		