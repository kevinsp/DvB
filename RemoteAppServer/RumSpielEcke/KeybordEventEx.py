__author__ = 'MrLapTop'

import viz

viz.go()

import vizinfo
vizinfo.add('This script demonstrates how to use keyboard callbacks.\nWhen a key is pressed, its value will be printed out.\nAlso the screen will toggle between black and white.')

color = 0
# This function is triggered whenever a keyboard button
# is pressed and gets passed the key that was pressed
# into the argument whichKey.
def mykeyboard(whichKey):
    print 'The following key was pressed: ', whichKey
    global color
    color = color ^ 1

    if whichKey == viz.KEY_F1:
        print 'Fkey 1 pressed'
    elif whichKey == viz.KEY_F2:
        print 'Fkey 2 pressed'
    elif whichKey == viz.KEY_F3:
        print 'Fkey 2 pressed'
    elif whichKey == viz.KEY_F4:
        print 'Fkey 2 pressed'
    elif whichKey == viz.KEY_UP:
        print 'Up arrow pressed'
    elif whichKey == viz.KEY_DOWN:
        print 'Down arrow pressed'
    elif whichKey == viz.KEY_LEFT:
        print 'Left arrow pressed'
    elif whichKey == viz.KEY_RIGHT:
        print 'Right arrow pressed'
    elif whichKey == viz.KEY_ESCAPE:
        print '==================================================='
        print '==================================================='
        print '==================================================='
        print '==================================================='
        print '==================================================='
        print '==================================================='
        print '==================================================='
        print '==================================================='
        print '==================================================='


    viz.clearcolor(color, color, color)

viz.callback(viz.KEYDOWN_EVENT, mykeyboard)