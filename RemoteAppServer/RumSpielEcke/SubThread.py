__author__ = 'Rolle'

import viz
import threading


class SubThread():

    def __init__(self):
        #threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.data = []
        self.shouldIRun = True

    def run(self):
        while True:
            with self.lock:
                if self.shouldIRun:
                    for d in self.data:
                        print d
                    viz.waitTime(1)
                    #print "Hallo"
                else:
                    print "Stopped"
                    return
            viz.waitTime(1)


    def changeData(self,data):
        with self.lock:
            self.data = data



    def stop(self):
        with self.lock:
            self.shouldIRun = False
        return

