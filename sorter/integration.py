#I suspect that it's safe to use threading here, and processes in the intensive parts of recognition.py
#you shouldn't stack more jobs if there are already two, unless the job you're stacking is an update job, which may be the third job in the stack
import time
from threading import Thread,Event

from sorter.device      import Device
from sorter.recognition import Recognizer

class SortJob:
    def __init__(self):
        self.paused    = False
        self.cancelled = False
        self.stopped   = False
        self.finished  = True

        self.startDate  = None
        self.pauseDate  = None
        self.pausedTime = None

        self.progress = "Waiting for new job."

        self.stateFlag    = Event()
        self.responseFlag = Event()

        self.device     = Device()
        self.recognizer = Recognizer()

        self.sortJobThread = None

    def start(sortParameters):
        if self.finished and not self.stopped:
            self.finished = False

            self.sortJobThread = SortJobThread(self.stateFlag,self.responseFlag,self.paused,self.cancelled,self.stopped,self.finished,self.progress,self.device,self.recognizer,sortParameters)
            self.sortJobThread.start()

            self.startDate  = datetime.datetime.now()
            self.pausedTime = self.startDate - self.startDate
        else:
            raise ValueError("Can't start next job before previous job finished, or device cleaned up and reset.")

    def pause(self):
        if not self.stopped and not self.finished:
            if not self.paused:
                self.paused = True
                self.notifyChildOfStateChange()

                self.pauseDate = datetime.datetime.now()
            else:
                raise ValueError("Cannot pause a paused job.")
        else:
            raise ValueError("Cannot pause a stopped or finished job.")

    def resume(self):
        if not self.stopped and not self.finished:
            if self.paused:
                self.paused = False
                self.notifyChildOfStateChange()

                self.pausedTime += datetime.datetime.now() - self.pauseDate
            else:
                raise ValueError("Cannot resume a running job.")
        else:
            raise ValueError("Cannot resume a stopped or finished job.")

    def getUpdate(self):
        if not self.stopped:
            update = {}
            update["progress"]       = self.progress
            update["operatingState"] = self.getOperatingState()
            update["timeStats"]      = self.getTimeStats()

            return update
        else:
            raise ValueError("Cannot get execution update from a stopped job.")

    def getOperatingState(self):
        runStates = []
        if not self.stopped and not self.finished:
            if self.paused:
                runStates.append("Paused")
            else:
                runStates.append("Running")

            if self.cancelled:
                runStates.append("Cancelled")

        if self.stopped:
            runStates.append("Stopped")
        elif self.finished:
            runStates.append("Finished")

        return runStates

    def getTimeStats(self):
        timeStats = {}
        timeStats["startDate"]       = self.startDate
        timeStats["expectedEndDate"] = self.expectedEndDate()

        timeStats["elapsedTime"]           = datetime.datetime.now() - self.startDate
        timeStats["expectedRemainingTime"] = timeStats["expectedEndDate"] - datetime.datetime.now()
        timeStats["runningTime"]           = timeStats["elapsedTime"] - self.pausedTime
        timeStats["pausedTime"]            = self.pausedTime

        return timeStats

    def inProgress():
        return not self.stopped and not self.finished

    def cancel(self):
        if not self.stopped and not self.finished:
            self.cancelled = True
            self.notifyChildOfStateChange()
        else:
            raise ValueError("Cannot cancel a stopped or finished job.")

    def stop(self):
        if not self.finished:
            self.paused    = False
            self.cancelled = False
            self.stopped   = True
            self.notifyChildOfStateChange()
            self.sortJobThread.join()
        else:
            raise ValueError("Cannot stop finished job.")

    #reduce likelihood of race conditions
    def notifyChildOfStateChange(self):
        self.stateFlag.set()
        self.responseFlag.wait()
        self.responseFlag.clear()

#TODO: this needs to be rewritten next
class SortJobThread(Thread):
    def __init__(self,stateFlag,responseFlag,paused,cancelled,stopped,finished,progress,device,recognizer,sortParameters):
        self.stateFlag      = stateFlag
        self.responseFlag   = responseFlag

        self.paused         = paused
        self.cancelled      = cancelled
        self.stopped        = stopped
        self.finished       = finished
        self.device         = device
        self.recognizer     = recognizer
        self.sortParameters = sortParameters

        self.previouslyPaused    = False
        self.previouslyCancelled = False

        self.progress = progress

        self.sleepTime = 20.0

        self.device     = device
        self.recognizer = recognizer

        self.photographyQueue = Queue.queue()
        self.recognitionQueue = Queue.queue()

    def run(self):
        device.photographAll(self.photographyQueue)
        recognizer.recognizeAll(self.photographyQueue,self.recognitionQueue)

        while True:
            if device.finished and self.photographyQueue.empty():
                recognizer.stop()
                break

            self.notFinishedLoopBody()

        sortScores = Ordering.generateSortScores(self.sortParameters,list(self.recognitionQueue))
        device.sort(sortScores)

        while True:
            if device.finished:
                break

            self.notFinishedLoopBody()

    def onStateChange(self):
        stateFlag.clear()

        if self.paused and not self.previouslyPaused:
            self.previouslyPaused = True
            device.pause()
        elif not self.paused and self.previouslyPaused:
            self.previouslyPaused = False
            device.resume()

        if self.cancelled and not self.previouslyCancelled:
            self.previouslyCancelled = True
            device.returnAllToInputTray()
        elif self.stopped:
            device.stop()
            recognizer.stop()
            self.progress = 'Job stopped.'
            return

        responseFlag.set()

    def notFinishedLoopBody(self):
        if stateFlag.is_set():
            self.onStateChange()

        self.progress = device.getProgress() + '\n' + recognizer.getProgress()

        sleep(self.sleepTime/1000.0)
