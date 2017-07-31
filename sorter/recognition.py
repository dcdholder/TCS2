try:
    import Image
except:
    from PIL import Image

import thread
import pytesseract

#keep working on recognition until it can run through the entire Kaladar set with 100% accuracy
#shit like 'Woodweaver's Puzzleknot' is gonna keep me up at night
class Recognition:
    NUM_CORES = 4

    def recognizeAllCards():
        pass

    def splitImageIntoFields():
        pass

    @staticmethod
    def ocrJobs(imageFilenames):
        ocrJobQueue     = queue.Queue()
        ocrResultsQueue = queue.Queue()

        for i in range(len(imageFilenames)):
            ocrJobQueue.put([i,imageFilenames]) #attach original index to input and output

        ocrJobThreads = []
        for i in range(NUM_CORES):
            ocrJobThread = threading.Thread(target=Recognition.threadOcrJobs, args=(ocrJobQueue,ocrResultsQueue))
            ocrJobThreads.append(ocrJobThread)
            ocrJobThread.start()

        ocrJobQueue.join()

        ocrResults = [0] * len(imageFilenames)
        for i in ocrResultsQueue.qsize():
            indexAndOcrResult                = ocrResultsQueue.get()
            ocrResults[indexAndOcrResult[0]] = indexAndOcrResult[1]

        return ocrResults

    @staticmethod
    def threadOcrJobs(ocrJobQueue,ocrResultsQueue):
        while True:
            indexAndFilename = ocrJobQueue.get()
            if indexAndFilename==None:
                break
            ocrResult = Recognition.ocrJob(indexAndFilename[1])
            ocrResultsQueue.put([indexAndFilename[0],ocrResult])
            ocrJobQueue.task_done()

    @staticmethod
    def ocrJob(imageFilename):
        tesseractConfig =

        return pytesseract.image_to_string(Image.open(imageFilename), lang='en', config=tesseractConfig)
