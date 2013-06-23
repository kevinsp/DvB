import viz
import viztracker
import vizinput
import vizshape
import vizproximity
import vizinfo
# Enable full screen anti-aliasing (FSAA) to smooth edges
viz.setMultiSample(1)


#Kommentar entfernen fuer 3D-Labor
"""
# connect to tracker
vrpn7 = viz.add('vrpn7.dle')
hostname = '141.82.50.174'

# connect eye tracker
pptEyes = vrpn7.addTracker('PPT0@'+hostname,0)
link = viz.link(pptEyes, viz.Mainview)
"""


# Display
viz.setOption('viz.fullscreen',1)
viz.fov(40.0,1.333)
#viz.setOption('viz.stereo',viz.QUAD_BUFFER)

viz.mouse.setVisible(True)

# increase the Field of View
viz.MainWindow.fov(60)

viz.go()


# ADD CAD-Modell
cad = viz.addChild(r'C:\VIZARD\Buero.osgt')
#cad = viz.addChild(r'C:\Users\Informatik\Desktop\RRBBB\RRBBB.wrl')

cad.disable(viz.CULL_FACE)
#setPosition X Y Z
cad.setPosition(0,0,60,viz.ABS_GLOBAL)
#setEuler Y X Z
cad.setEuler( [0, 0, 0] )


# collision control
viz.collision(viz.OFF)




# ADD Ground
ground1 = viz.addChild('ground.osgb')
ground2 = viz.addChild('ground.osgb')
ground2.setPosition(0,0,60)
ground3 = viz.addChild('ground.osgb')
ground3.setPosition(0,0,50)


#OPTIMIERUNGEN

# ADD world axis with X, Y, Z labels
world_axes = vizshape.addAxes()
X = viz.addText3D('X',pos=[1.1,0,0],color=viz.RED,scale=[0.3,0.3,0.3],parent=world_axes)
Y = viz.addText3D('Y',pos=[0,1.1,0],color=viz.GREEN,scale=[0.3,0.3,0.3],align=viz.ALIGN_CENTER_BASE,parent=world_axes)
Z = viz.addText3D('Z',pos=[0,0,1.1],color=viz.BLUE,scale=[0.3,0.3,0.3],align=viz.ALIGN_CENTER_BASE,parent=world_axes)

# start position
viz.MainView.setPosition(6,1,6)
viz.MainView.setEuler(0,0,0)

# ADD lighting
licht = viz.addLight()
licht.enable()
licht.setEuler(45,45,0)
licht.intensity(2.5)


# Proximity Stuff

# Target
target = vizproximity.Target(viz.MainView)

#Sensor
shape = (1,1,1)
source = [0.3,0.3,0.3]
#Sensor Objekt..


pflanze = viz.addChild('plant.osgb')


pflanze.setPosition(0.3,0.3,0.3)
sensor = vizproximity.Sensor(vizproximity.Sphere(4.0),source=viz.Matrix.translate(source))

desc = pflanze.getNodeNames()

#desc = cad.getNodeNames()

#Proximity Manager
manager = vizproximity.Manager()
manager.addTarget(target)
manager.addSensor(sensor)

info = vizinfo.add(r'C:\VIZARD\Buero_test.osgt')
info.visible(False)
# Register callbacks for proximity sensors
def EnterProximity(e):
	info.message(str(desc))
	print(str(desc))
	info.visible(True)
	info.translate([.8, .8])
	print(cad.getNodeNames()[5].split("."))


def ExitProximity(e):
	info.visible(False)

manager.onEnter(None, EnterProximity)
manager.onExit(None, ExitProximity)

