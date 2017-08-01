import unittest
from sorter import app
from flask.ext.api import status
import json

class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.cardSorterServer.test_client()
        self.startPayload = json.dumps({"A": "B"})
        self.contentType  = 'application/json'
        #TODO: once mocks for Device and Recognizer are available, feed them to SortJob instead of mocking SortJob
        #maybe even dependency-inject by replacing app.sortJob with SortJob(MockDevice(),MockRecognizer())
        app.sortJob = MockSortJob()

    def testStartPositive(self):
        response = self.app.post('/job/start', data=self.startPayload, content_type=self.contentType)
        self.assertTrue(status.is_success(response.status_code), msg='Response Code=' + str(response.status_code))

    def testPausePositive(self):
        self.app.post('/job/start', data=self.startPayload, content_type=self.contentType)
        response = self.app.post('/job/pause')
        self.assertTrue(status.is_success(response.status_code), msg='Response Code=' + str(response.status_code))

    def testResumePositive(self):
        self.app.post('/job/start', data=self.startPayload, content_type=self.contentType)
        self.app.post('/job/pause')
        response = self.app.post('/job/resume')
        self.assertTrue(status.is_success(response.status_code), msg='Response Code=' + str(response.status_code))

    def testUpdatePositive(self):
        self.app.post('/job/start', data=self.startPayload, content_type=self.contentType)
        response = self.app.get('/job/update')
        self.assertTrue(status.is_success(response.status_code), msg='Response Code=' + str(response.status_code))

    def testStopPositive(self):
        self.app.post('/job/start', data=self.startPayload, content_type=self.contentType)
        response = self.app.delete('/job/stop')
        self.assertTrue(status.is_success(response.status_code), msg='Response Code=' + str(response.status_code))

    def testCancelPositive(self):
        self.app.post('/job/start', data=self.startPayload, content_type=self.contentType)
        response = self.app.delete('/job/cancel')
        self.assertTrue(status.is_success(response.status_code), msg='Response Code=' + str(response.status_code))

    def testStartTwice(self):
        self.app.post('/job/start', data=self.startPayload, content_type=self.contentType)
        response = self.app.post('job/start')
        self.assertFalse(status.is_success(response.status_code), msg='Response Code=' + str(response.status_code))

    def testPausePausedJob(self):
        self.app.post('/job/start', data=self.startPayload, content_type=self.contentType)
        self.app.post('/job/pause')
        response = self.app.post('/job/pause')
        self.assertFalse(status.is_success(response.status_code), msg='Response Code=' + str(response.status_code))

    def testResumeRunningJob(self):
        self.app.post('/job/start', data=self.startPayload, content_type=self.contentType)
        response = self.app.post('/job/resume')
        self.assertFalse(status.is_success(response.status_code), msg='Response Code=' + str(response.status_code))

    def testRequestBeforeStart(self):
        responses    = []
        requestTypes = []
        for requestType in ['pause','resume','update','stop','cancel']:
            responses.append(self.app.post('/job/' + requestType))
            requestTypes.append(requestType)

        for i in range(len(responses)):
            self.assertFalse(status.is_success(responses[i].status_code), msg='Request=' + requestTypes[i] + ', Response Code=' + str(responses[i].status_code))

    def testRequestAfterStop(self):
        self.app.post('/job/start', data=self.startPayload, content_type=self.contentType)
        self.app.delete('/job/stop')

        responses    = []
        requestTypes = []
        for requestType in ['pause','resume','update','stop','cancel']:
            responses.append(self.app.post('/job/' + requestType))
            requestTypes.append(requestType)

        for i in range(len(responses)):
            self.assertFalse(status.is_success(responses[i].status_code), msg='Request=' + requestTypes[i] + ', Response Code=' + str(responses[i].status_code))

    def testInvalidRequest(self):
        response = self.app.post('/job/starf')
        self.assertFalse(status.is_success(response.status_code), msg='Response Code=' + str(response.status_code))

    def tearDown(self):
        app.sortJob.stop()

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

if __name__ == "__main__":
    unittest.main()
