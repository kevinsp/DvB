import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizpopup
import vizact
import vizdlg

import GlobalVariables


def porten(menubar):
        """Springe zu selbst definierter Position"""
        
	"""Falls noch kein Eingabefenster offen"""
	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True

		"""Verstecke menubar"""
		menubar.setVisible(False)
		
		
		def ueberpruefeEingabe(data):
                        """ueberpruefe die Eingabe und springe"""
                        
			object = viz.pick(0,viz.SCREEN)
			"""Falls man auf Accept geklickt hat: ueberpruefen und springen"""
			if object is input.accept:
				coordinates = data.value.split()
				try:
                                       """Ist die Eingabe ein Float Wert und in Listenlänge?"""
					if (type(float(coordinates[0])) is float and type(float(coordinates[1])) is float and type(float(coordinates[2])) is float): 
						"""setze Position"""
						viz.MainView.setPosition(float(coordinates[0]), float(coordinates[1]), float(coordinates[2]))
						GlobalVariables.tracker.setPosition(float(coordinates[0]), float(coordinates[1]), float(coordinates[2]))

						"""Uebergebe neue Position an Globale Variable"""
						GlobalVariables.position = tracker.getPosition()

                                                """Entferne Eingabefenster"""
						input.remove()
						GlobalVariables.windowOpen = False

                                        """Falsche Eingabe"""
					else:
						data.error = "Biite nur Zahlen eingeben."
						input.box.setFocus(viz.ON)
                                """Falsche Eingabe"""
				except:
					data.error = "Biite nur Zahlen eingeben."
					input.box.setFocus(viz.ON)
			"""Falls man auf Cancel geklickt hat: Vorgang abbrechen	"""
			elif object is input.cancel:
				GlobalVariables.windowOpen = False
				input.remove()
				
			"""Falls man ausversehen nicht auf einen der Buttons geklickt hat"""	
			else:
				data.error=""
				input.box.setFocus(viz.ON)
				
		"""Dialogfenster fuer zu selbst definieren Position springen erstellen"""
		input = vizdlg.InputDialog(title='Springe zu', prompt = "Die Koordinaten hintereinander eingeben\n \"10.0  5.0  7.5\" (X Z Y)", length=1.0, validate = ueberpruefeEingabe)
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
		"""Fokus auf Textfeld"""	
		input.box.setFocus(viz.ON)
		viztask.schedule(showdialog()) 
		
