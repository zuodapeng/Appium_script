import unittest
import util

class CameraTest(unittest.TestCase):
    def setUp(self):
        util.launchApp(self, 'com.intel.camera22', '.Camera')

    def tearDown(self):
        util.tearDown(self)

    def testChangeToBackCamera(self):
        util.setCameraMode(self, '1')