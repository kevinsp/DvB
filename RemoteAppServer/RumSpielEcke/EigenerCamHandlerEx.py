import viz
import vizact

viz.setMultiSample(4)
viz.fov(60)
viz.go()

import vizinfo
info = vizinfo.add( 'The view is controlled by custom camera handler class.\nControls:\n--Left / Right mouse buttons: move up/down.\n--Mouse wheel: pan left / right.\n--W / S keys: forward / back' )

#Initialize world
viz.clearcolor( viz.GRAY )
ground = viz.addChild( 'ground.osgb' )

#Create custom camera handler
class MyCameraHandler( viz.CameraHandler ):

    def _camMouseDown( self, e ):
        if e.button == viz.MOUSEBUTTON_LEFT:
            #move view down
            e.view.move( [0, -1, 0] )
        elif e.button == viz.MOUSEBUTTON_RIGHT:
            #move view up
            e.view.move( [0, 1, 0] )

    def _camMouseWheel( self, e ):
        if e.dir > 0:
            #wheel rolled forward
            e.view.move( [1, 0, 0] )
        else:
            #wheel rolled backwards
            e.view.move( [-1, 0, 0] )

    def _camUpdate( self, e ):
        #Check keyboard movement
        if viz.iskeydown ('w' ):
            #move forward the amout of time in seconds sence the last call to _camUpdate
            e.view.move( [0, 0, e.elapsed * 10] )
        elif viz.iskeydown ('s' ):
            #move backward the amout of time in seconds sence the last call to _camUpdate
            e.view.move( [0, 0, -e.elapsed * 10] )
        elif viz.iskeydown ('a' ):
            #move backward the amout of time in seconds sence the last call to _camUpdate
            e.view.move( [ -e.elapsed * 10, 0, 0] )

#Set camera handler
viz.cam.setHandler( MyCameraHandler() )

#Remove camera handler on spacebar (will revert to built-in camera handler)
vizact.onkeydown( ' ', viz.cam.setHandler, None )