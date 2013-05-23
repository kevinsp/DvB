import viz
windowOpen = False
infoWindowOpen = False
flugModus = False
position = []
euler = []

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