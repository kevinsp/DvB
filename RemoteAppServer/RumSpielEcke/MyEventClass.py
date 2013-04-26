__author__ = 'MrLapTop'
import viz

class MyEventClass(viz.EventClass):
    def __init__(self):
        #IMPORTANT: We need to initialize base class
        viz.EventClass.__init__(self)

        #Register callback with our event class
        self.callback(INC_JASON_EVENT,self.onJasonEvent)
        self.callback(viz.UPDATE_EVENT,self.printEvent)

    def onJasonEvent(self,e):
        if e.blub:
            viz.MainView.move([0,0,1])

    def printEvent(self,e):
        print e.__dict__


def losGehts():

    while(True):

        viz.waitFrame(200)
        viz.logNotice("Bin in Schleife")
        pre = viz.Event(blub="ME")
        viz.postEvent(INC_JASON_EVENT,pre)

if __name__ == "__main__":
    #INC_JASON_EVENT = viz.getEventID("INC_JASON_EVENT")
    #viz.go()
    #court = viz.addChild('piazza.osgb')
    myEventClass = viz.Event()
    print myEventClass
    #viz.director(losGehts)
