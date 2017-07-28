#I suspect that it's safe to use threading here, and processes in the intensive parts of recognition.py
#you shouldn't stack more jobs if there are already two, unless the job you're stacking is an update job, which may be the third job in the stack

class Operation:
    def runJob(jobs,updateOutput): #jobs must be LIFO
        trays = {}
        tray["main"] = queue.Queue()
        tray["A"]    = queue.Queue()
        tray["B"]    = queue.Queue()

        photographyInstructions = queue.Queue()
        cardPhotoFilenames      = queue.Queue()
        identifiedCards         = queue.Queue()

        photographyInstructions.put("PHOTO")

        photographyThread        = Thread(target=Operation.photographAll, args=[photographyInstructions,updateOutput])
        recognitionComputeThread = Thread(target=Recognition.recognizeImages, args=[cardPhotoFilenames,identifiedCards])

        while True:
            #first check if there have been any new commands picked up from Flask
            if jobs.qsize()!=1:
                newJob = jobs.get()
                if newJob.type()=="pause":
                    #pause both threads
                elif newJob.type()=="cancel":
                    #kill both threads and empty the sorting trays

                    returnAllCardsThread = Thread(target=Operation.returnAllToInputTray, args=[trays])
                    trays["A"].join()
                    trays["B"].join()

                    return
                elif newJob.type()=="resume":
                    #unpause both threads
            elif photographyInstructions.empty():
                #kill both threads
                #generate sort ordering
                #open a new thread with that sort ordering
            else:
