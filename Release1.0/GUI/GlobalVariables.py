import viz
import vizdlg



"""Menuetheme"""
darkTheme = viz.getTheme()	#: R, G, B, Alpha   1 != Transparent
darkTheme.borderColor = (0,0,0,1) #: Farbe der Borders
darkTheme.backColor = (0,0,0,0.4) #: Hintergrund MenüButtons
darkTheme.lightBackColor = (0,0,0,0.4) #: Farbe, Hintergrund Dropdown Menü
darkTheme.darkBackColor = (0,0,0,0.75) #: Farbe, Hintergrund der Progressbar"""
darkTheme.highBackColor = (0,0,0,0.4) #: Farbe, Hintergrund, wenn man über den menübuttons ist
darkTheme.highTextColor = (0,0,0,1) #: Farbe, Text, wenn man mit der Maus darüber ist
darkTheme.textColor = (1,1,1,1) #: Farbe, Text

"""checkpoints/Note Theme"""
blackTheme = viz.getTheme()
blackTheme.borderColor = (1,1,1,1)
blackTheme.backColor = (0,0,0,1)#: Hintergrund des Panels
blackTheme.lightBackColor = (0,0,0,1) #: Hintergrund der Buttons auf dem Panel
blackTheme.textColor = (1,1,1,1)

"""Theme des Kommentar Panels"""
commentTheme = viz.getTheme()
commentTheme.borderColor = (1,1,1,1)
commentTheme.lightBackColor = (0,0,0,0.1) #: Hintergrund
commentTheme.textColor = (1,1,1,1)


"""angewähltesLabel Theme"""
gewaehltTheme = viz.getTheme()
gewaehltTheme.borderColor = (1,1,1,1)
gewaehltTheme.backColor = (1,1,1,1)
gewaehltTheme.lightBackColor = (1,1,1,1)



windowOpen = False #: Ist ein Eingabefenster offen?
infoWindowOpen = False #: Ist ein Infofenster offen?
flugModus = False #: Flugmodus aktiv?
showPosi = False #: Zeige Position
showIP = False #: Zeige IP
position = []#: Aktuelle Position im Mausmodus
euler = []  #: Aktueller Winkel im Mausmodus
checkPointsList = []    #: Liste mit Checkpoints
noteList = []   #: Liste mit 3D Notes
noteListObjects = [] #: Liste mit den in Wizard befindlichen 3D Notes
teillisteCheckpoint = 1 #: Nr der Teilliste, welche gerade angezeigt wird (checkpoints)
gesamtTeillisteCheckpoint = 1 #: Nr der maximalen Teillisten in checkpoints
teillisteNote = 1 #: Nr der Teilliste, welche gerade angezeigt wird (Note)
gesamtTeillisteNote = 1 #: Nr der maximalen Teillisten in Notes"""
commentWindowOpen = False #: Ist das Kommentar Fenster offen (checkpoints)"""
moveSpeed = 2.0 #: Bewegungsgeschwindigkeit"""
tracker = None
link = None 
flySpeed = 0.2 #: fluggeschwindigkeit"""
serverIsRunning = False #: Läuft der Server?"""
nurEinmalSetzen = False #: Nur einmal setzen bei Listennavigation mit Pfeiltasten"""
positionWhichIsActivated = -1 #: Position, welcher Kommentar gerade angezeigt wird"""
commentPanel = vizdlg.Panel(theme = commentTheme, fontSize=30, align=viz.ALIGN_CENTER_CENTER) #: Panel des Kommentars"""
commentView = None	#: Das Kommentar vom ausgewaehlten Checkpoint"""
flugEinmalGesetzt = False  #: Nur einmal setzen bei Naviagation im Flugmodus"""
direction = None 	#: Richtung beim Fliegen"""


"""Anzeige in der Mitte des Bildschirms"""
midTextScreen = viz.addText("", viz.SCREEN)
midTextScreen.setScale(0.4,0.4,0)
midTextScreen.alignment(viz.ALIGN_CENTER_CENTER)
midTextScreen.setPosition([0.5,0.5,0])
midTextScreen.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
midTextScreen.setBackdropColor([0,0,0])


"""Proximity Variablen"""
variable1 = False
variable2 = False
variable3 = False
variable4 = False
variable5 = False
variable6 = False






vizInfoBackgroundColor = [0,0,0,0.4]
vizInfoBorderColor = [0,0,0,1]
vizInfoTitleBackgroundColor = [0,0,0,0.7]

