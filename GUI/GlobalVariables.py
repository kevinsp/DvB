import viz
import vizdlg

windowOpen = False
infoWindowOpen = False
flugModus = False
showPosi = False
showIP = False
position = []
euler = []
checkPointsList = []
noteList = []
teillisteCheckpoint = 1 #Nr der Teilliste, welche gerade angezeigt wird (checkpoints)
gesamtTeillisteCheckpoint = 1 #Nr der maximalen Teillisten in checkpoints
teillisteNote = 1 #Nr der Teilliste, welche gerade angezeigt wird (Note)
gesamtTeillisteNote = 1 #Nr der maximalen Teillisten in Notes
commentWindowOpen = False #Ist das Kommentar Fenster offen (checkpoints)
moveSpeed = 2.0 #Bewegungsgeschwindigkeit
tracker = 0 #tracker
link = 0 #link
flySpeed = 0.2 #fluggeschwindigkeit
serverIsRunning = False #Läuft der Server?
nurEinmalSetzen = False
positionWhichIsActivated = -1 #position, welcher kommentar gerade angezeigt wird
commentPanel = vizdlg.Panel(fontSize=13, align=viz.ALIGN_CENTER_CENTER, background=False, border=False) #Panel des Kommentars
commentView = None				#Das Kommentar

###Proximity Variablen###
variable1 = False
variable2 = False
variable3 = False
variable4 = False
variable5 = False
variable6 = False
###					 ###






vizInfoBackgroundColor = [0,0,0,0.4]
vizInfoBorderColor = [0,0,0,1]
vizInfoTitleBackgroundColor = [0,0,0,0.7]

#anzeige von checkpoints/Note Theme
blackTheme = viz.getTheme()
blackTheme.borderColor = (0.1,0.1,0.1,.2)
blackTheme.backColor = (0.4,0.4,0.4,.2)
blackTheme.lightBackColor = (0.6,0.6,0.6,.2)
blackTheme.darkBackColor = (0.2,0.2,0.2,.2)
blackTheme.highBackColor = (0.2,0.2,0.2,.2)

#angewähltesLabel Theme
gewaehltTheme = viz.getTheme()
gewaehltTheme.borderColor = (0,0,0,1)
gewaehltTheme.backColor = (0,0,0,1)
gewaehltTheme.lightBackColor = (0,0,0,1)
gewaehltTheme.darkBackColor = (0,0,0,1)
gewaehltTheme.highBackColor = (0,0,0,1)



#Menuetheme
darkTheme = viz.getTheme()			###   R, G, B, Alpha
darkTheme.borderColor = (0,0,0,1) #Farbe der Borders
darkTheme.backColor = (0,0,0,0.4) #Hintergrund MenüButtons
darkTheme.lightBackColor = (0,0,0,0.4) #Farbe, Hintergrund Dropdown Menü
darkTheme.darkBackColor = (0,0,0,0.75) #Farbe, Hintergrund der Progressbar
darkTheme.highBackColor = (0,0,0,0.4) #Farbe, Hintergrund, wenn man über den menübuttons ist
darkTheme.highTextColor = (0,0,0,1) #Farbe, Text, wenn man mit der Maus darüber ist
darkTheme.textColor = (1,1,1,1) #Farbe, Text 
