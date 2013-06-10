import viz

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
commentWindowOpenNr = -1 #Nr des offenen Kommentar Fensters
moveSpeed = 2.0 #Bewegungsgeschwindigkeit
tracker = 0 #tracker
flySpeed = 0.2 #fluggeschwindigkeit

vizInfoBackgroundColor = [0,0,0,0.4]
vizInfoBorderColor = [0,0,0,1]
vizInfoTitleBackgroundColor = [0,0,0,0.7]



darkTheme = viz.getTheme()			###   R, G, B, Alpha
darkTheme.borderColor = (0,0,0,1) #Farbe der Borders
darkTheme.backColor = (0,0,0,0.4) #Hintergrund MenüButtons
darkTheme.lightBackColor = (0,0,0,0.4) #Farbe, Hintergrund Dropdown Menü
darkTheme.darkBackColor = (0,0,0,0.75) #Farbe, Hintergrund der Progressbar
darkTheme.highBackColor = (0,0,0,0.4) #Farbe, Hintergrund, wenn man über den menübuttons ist
darkTheme.highTextColor = (0,0,0,1) #Farbe, Text, wenn man mit der Maus darüber ist
darkTheme.textColor = (1,1,1,1) #Farbe, Text 
