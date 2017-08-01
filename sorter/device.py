class Device():
    def __init__(self):
        pass

    def photographAll(self,filenameQueue):
        pass

    def returnAllToInputTray(self):
        pass

    def sort(self,sortScores):
        pass

    def getProgress(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

'''
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
'''
