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

        self.progress = "Waiting for next job."

        self.stateFlag = Event()

        self.device     = Device()
        self.recognizer = Recognizer()

        self.sortJobThread = None

    def start(sortParameters):
        if self.finished and not self.stopped:
            self.finished = False

            self.sortJobThread = SortJobThread(self.stateFlag,self.paused,self.cancelled,self.stopped,self.finished,self.progress,self.device,self.recognizer,sortParameters)
            self.sortJobThread.start()

            self.startDate  = datetime.datetime.now()
            self.pausedTime = self.startDate - self.startDate
        else:
            raise ValueError("Can't start next job before previous job finished, or device cleaned up and reset.")

    def pause():
        if not self.stopped and not self.finished:
            if not self.paused:
                self.paused = True
                self.stateFlag.set()

                self.pauseDate = datetime.datetime.now()
            else:
                raise ValueError("Cannot pause a paused job.")
        else:
            raise ValueError("Cannot pause a stopped or finished job.")

    def resume():
        if not self.stopped and not self.finished:
            if self.paused:
                self.paused = False
                self.stateFlag.set()

                self.pausedTime += datetime.datetime.now() - self.pauseDate
            else:
                raise ValueError("Cannot resume a running job.")
        else:
            raise ValueError("Cannot resume a stopped or finished job.")

    def getUpdate():
        if not self.stopped:
            update = {}
            update["progress"]       = self.progress
            update["operatingState"] = self.getOperatingState()
            update["timeStats"]      = self.getTimeStats()

            return update
        else:
            raise ValueError("Cannot get execution update from a stopped job.")

    def getOperatingState():
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

    def getTimeStats():
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

    def cancel():
        if not self.stopped and not self.finished:
            self.cancelled = True
            self.stateFlag.set()
        else:
            raise ValueError("Cannot cancel a stopped or finished job.")

    def stop():
        if not self.finished:
            self.paused    = False
            self.cancelled = False
            self.stopped   = True
            self.stateFlag.set()
            self.sortJobThread.join()
        else:
            raise ValueError("Cannot stop finished job.")

#TODO: this needs to be rewritten next
class SortJobThread(Thread):
    def __init__(self,stateFlag,paused,cancelled,stopped,finished,device,recognizer,sortParameters):
        self.stateFlag      = stateFlag
        self.paused         = paused
        self.cancelled      = cancelled
        self.stopped        = stopped
        self.finished       = finished
        self.device         = device
        self.recognizer     = recognizer
        self.sortParameters = sortParameters

    def run(): #jobs must be LIFO
        sleepTime = 0.01

        trays = {}
        tray["main"] = queue.Queue()
        tray["A"]    = queue.Queue()
        tray["B"]    = queue.Queue()

        photographyInstructions = queue.Queue()
        cardPhotoFilenames      = queue.Queue()
        identifiedCards         = queue.Queue()

        #startTime =

        photographyInstructions.put("PHOTO")

        photographyThread        = Thread(target=Operation.photographAll, args=[cardPhotoFilenames])
        recognitionComputeThread = Thread(target=Recognition.recognizeImages, args=[cardPhotoFilenames,identifiedCards])

        while True:
            #first check if there have been any new commands picked up from Flask
            if jobs.qsize()!=1:
                newJob = jobs.get()
                if newJob.type()=="pause": #allow the recognition thread to continue processing during pause
                    photographyThread.pause = True
                    updateChild.set()
                elif newJob.type()=="resume":
                    if photographyThread.pause:
                        photographyThread.pause = False
                        updateChild.set()
                elif newJob.type()=="cancel": #returns cards to the input bin
                    photographyThread.undo = True
                    updateChild.set()
                elif newJob.type()=="emergency stop": #does not return cards to the input bin
                    photographyThread.stop        = True
                    recognitionComputeThread.stop = True

                    updateChild.set()

                    photographyThread.join()
                    recognitionComputeThread.join()

                    return
            elif not photographyInstructions.is_alive():
                break
            else:
                time.sleep(sleepTime)

        #confirm to ourselves that both threads are finished
        #TODO: add logging so we know whether these joins get completed
        photographyThread.join()
        recognitionComputeThread.join()

        #generate a sort ordering from the identified cards
        sortScores = Ordering.generateSortScores(list(identifiedCards))

        #open a new physical sort thread using that sort ordering
        physicalSortThread = Thread(target=Operation.sortCards, args=[sortScores])
        while True:
            if jobs.qsize()!=1:
                newJob = jobs.get()
                if newJob.type()=="pause": #allow the recognition thread to continue processing during pause
                    physicalSortThread.pause = True
                    updateChild.set()
                elif newJob.type()=="resume":
                    if physicalSortThread.pause:
                        physicalSortThread.pause = False
                        updateChild.set()
                elif newJob.type()=="cancel": #returns cards to the input bin
                    if physicalSortThread.undo:
                        physicalSortThread.undo = True
                        updateChild.set()
                elif newJob.type()=="emergency stop": #does not return cards to the input bin
                    physicalSortThread.stop = True
                    updateChild.set()

                    physicalSortThread.join()

                    return
            elif not physicalSortThread.is_alive():
                break
            else:
                time.sleep(sleepTime)

        return

class WorkerThread(Thread):
    pauseTime = 0.05

    def __init__(self):
        Thread.__init__(self,updateTrigger)
        self.pausing  = False #'pause' temporarily pauses the execution loop
        self.previouslyPaused = False
        self.undoing  = False #'undo' entails stopping the thread once the work has been 'undone' (i.e. physical sorting)
        self.stopping = False #'stop' entails stopping the thread immediately

        self.updateTrigger = updateTrigger

#handle the photography of all cards in the input tray, and the return of all cards from the sorting tray back to the input tray
#handle the 'pause', 'undo' and 'stop' interrupts
class PhotographyThread(WorkerThread):
    def __init__(self,updateFromParent,sortingDevice,cardPhotoFilenames):
        super().__init__(self,updateTrigger)
        self.sortingDevice           = sortingDevice
        self.cardPhotoFilenames      = cardPhotoFilenames
        self.returnToInputTrayThread = None
        self.photographCardsThread   = self.sortingDevice.startPhotographCardsThread(updateFromChild,cardPhotoFilenames)

        self.childUpdate = threading.Event()

    def run(self,cardPhotoFilenames): #cardPhotoFilenames is a producer queue
        while True:
            if self.stopping and updateFromParent.is_set():
                self.stop()
                return

            if self.pausing and updateFromParent.is_set():
                self.pause()

            if not self.pausing and self.previouslyPaused and updateFromParent.is_set():
                self.resume()

            if self.undoing and updateFromParent.is_set():
                self.undo()

            updateFromParent.clear()

            if self.photographCardsThread!=None:
                if not self.photographCardsThread.is_alive():
                    self.photographCardsThread=None
                    self.returnToInputTrayThread = self.sortingDevice.startReturnToInputTrayThread(childUpdate)
            elif self.returnToInputTrayThread!=None:
                if not self.returnToInputTrayThread.is_alive():
                    return

            time.sleep(super.pauseTime)

    def resume(self):
        if self.photographCardsThread!=None:
            returnToInputTrayThread.pausing = False
        elif self.returnToInputTrayThread!=None:
            returnToInputTrayThread.pausing = False

        self.childUpdate.set()

        self.previouslyPaused = False

    def pause(self):
        if self.photographCardsThread!=None:
            returnToInputTrayThread.pausing = True
        elif self.returnToInputTrayThread!=None:
            returnToInputTrayThread.pausing = True

        self.childUpdate.set()

        self.previouslyPaused = True

    def undo(self):
        if photographCardsThread!=None: #check if 'undo' has already been called
            self.photographCardsThread.stop()
            if not self.photographCardsThread.is_alive():
                self.photographCardsThread = None

            if returnToInputTrayThread==None:
                self.returnToInputTrayThread = self.sortingDevice.startReturnToInputTrayThread(childUpdate)

    def stop(self):
        if self.photographCardsThread!=None:
            self.photographCardsThread.stopping = True
        elif self.returnToInputTrayThread!=None:
            self.returnToInputTrayThread.stopping = True

        self.childUpdate.set()

        if self.photographCardsThread!=None:
            self.photographCardsThread.join()
        elif self.returnToInputTrayThread!=None:
            self.returnToInputTrayThread.join()

#class RecognitionComputeThread(WorkerThread):

#class PhotographCardsThread(WorkerThread):

#class ReturnToInputTrayThread(WorkerThread):
