from threading import Thread

class MockSortJob:
    def __init__(self):
        self.paused    = False
        self.cancelled = False
        self.stopped   = False
        self.finished  = True

    def start(self,sortParameters):
        self.finished = False
        self.paused   = False
        self.stopped  = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def getUpdate(self):
        return {"status": "OK"}

    def stop(self):
        self.stopped = True

    def cancel(self):
        self.cancelled = True

    def inProgress(self):
        return not self.stopped and not self.finished

class MockDevice():
    NUM_FAKE_CARDS       = 10
    TOTAL_OPERATION_TIME = 0.1

    def __init__(self):
        self.paused   = False
        self.stopped  = False
        self.finished = True

        self.progress = None

        self.runningThread = None

    def photographAll(self,filenameQueue):
        self.finished      = False
        self.runningThread = MockDevicePhotographThread(self.paused,self.stopped,self.finished,self.progress,filenameQueue)
        self.runningThread.start()

    def returnAllToInputTray(self):
        self.runningThread = MockDeviceSleeperThread()
        self.runningThread.start()

    def sort(self,sortScores):
        self.runningThread = MockDeviceSleeperThread()
        self.runningThread.start()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.paused  = False
        self.stopped = True

class MockDeviceSleeperThread(Thread):
    def __init__(self,finished):
        self.finished = finished

    def run(self):
        self.finished = False
        sleep(Device.TOTAL_OPERATION_TIME)
        self.finished = True

class MockDevicePhotographThread(Thread):
    def __init__(self,paused,stopped,progress,filenameQueue):
        self.paused   = paused
        self.stopped  = stopped
        self.finished = finished

        self.progress = progress

        self.filenameQueue = filenameQueue

    def run(self):
        self.finished = False

        cardCount = 0
        while self.cardCount<MockDevice.NUM_FAKE_CARDS:
            sleep(MockDevice.TOTAL_OPERATION_TIME) / MockDevice.NUM_FAKE_CARDS
            if not self.paused and not self.stopped:
                cardCount+=1
                filenameQueue.put("fake_" + cardCount + ".png")
                self.progress = 'Imaging card ' + cardCount
            elif self.stopped:
                return

        self.finished = True

class MockRecognizer():
    def __init__(self):
        self.paused   = False
        self.stopped  = False
        self.finished = True

        self.progress = None

        self.mockRecognizerRecognitionThread = None

    def recognizeAll(filenameQueue,recognitionQueue):
        self.mockRecognizerRecognitionThread = MockRecognizerRecognitionThread(self.paused,self.stopped,self.finished,self.progress,self.filenameQueue,self.recognitionQueue)
        self.mockRecognizerRecognitionThread.start()

    def pause():
        self.paused = True

    def resume():
        self.paused = False

    def stop():
        self.paused  = False
        self.stopped = True

class MockRecognizerRecognitionThread(Thread):
    def __init__(self,paused,stopped,finished,progress,filenameQueue,recognitionQueue):
        self.paused   = paused
        self.stopped  = stopped
        self.finished = finished

        self.progress = progress

        self.cardCount        = cardCount
        self.recognitionQueue = recognitionQueue

    def run(self):
        cardsRecognized = 0
        while True:
            sleep(MockRecognizer.TIME_PER_CARD)
            if not self.paused and not self.stopped:
                if not filenameQueue.empty()
                    filenameQueue.get()
                    recognitionQueue.put(Card.CardFromNameAndSet("Island","Amonkhet"))
                    cardsRecognized+=1
                    cardCount = filenameQueue.qsize()+cardsRecognized
                    self.progress = 'Recognizing card ' + cardsRecognized + '/' + cardCount
                elif self.stopped:
                    return
