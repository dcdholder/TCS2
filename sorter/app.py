from flask import Flask, request
from flask_restful import Api, Resource

import json

cardSorterServer = Flask(__name__)

sortJob = None

class JobResource(Resource):
    def post(self,action):
        global sortJob
        if action=="start":
            if sortJob==None or not sortJob.inProgress():
                startRequestBody = request.get_json()
                try:
                    #sortJob = integration.SortJob(startRequestBody)
                    sortJob = MockSortJob(startRequestBody)
                    return 'Sort job started.', 201
                except Exception as e:
                    return str(e), 400
            else:
                return 'Cannot start job; job already in progress.', 409

        elif action=="pause" or action=="resume":
            if sortJob==None or not sortJob.inProgress():
                return 'No existing sort job to act on.', 404
            else:
                if action=="pause":
                    if sortJob.paused:
                        return 'Sort job already paused.', 403
                    else:
                        sortJob.pause()
                        return 'Sort job paused.', 204
                elif action=="resume":
                    if sortJob.paused:
                        sortJob.resume()
                        return 'Sort job resumed.', 204
                    else:
                        return 'Sort job not paused.', 403
        else:
            return 'Invalid post URI: possible options are \'start\', \'pause\' or \'resume\'.', 400

    def get(self,action):
        global sortJob
        if action=="update":
            if sortJob==None or not sortJob.inProgress():
                return 'No existing sort job to act on.', 404
            else:
                updateDict = sortJob.getUpdate()
                return json.dumps(updateDict), 200
        else:
            return 'Invalid get URI: must be \'update\'.', 400

    def delete(self,action):
        global sortJob
        if action=="stop" or action=="cancel":
            if sortJob==None or not sortJob.inProgress():
                return 'No existing sort job to act on.', 404
            else:
                if action=="stop":
                    sortJob.stop()
                    sortJob = None
                    return 'Sort job stopped.', 204
                elif action=="cancel":
                    if sortJob.cancelled:
                        return 'Sort job already cancelled.', 403
                    else:
                        sortJob.cancel()
                        return 'Sort job cancelled.', 204
        else:
            return 'Invalid delete URI: must be \'stop\' or \'cancel\'.', 400

class MockSortJob:
    def __init__(self,sortParameters):
        self.paused    = False
        self.cancelled = False
        self.stopped   = False

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
        return not self.stopped

cardSorterServerApi = Api(cardSorterServer)
cardSorterServerApi.add_resource(JobResource, '/job/<action>')

if __name__ =='__main__':
    cardSorterServer.run(debug=True)
