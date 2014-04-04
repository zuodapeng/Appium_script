import unittest
import commands
import time
from selenium import webdriver

CAMERA_ID = 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'
Geolocation_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_geo_location_key'
Exposure_STATE= 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_exposure_key'
Scene_STATE = 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_scenemode_key'

DCIM_PATH = '/mnt/sdcard/DCIM'
CAMERA_FOLDER = '100ANDRO'

class CameraTest(unittest.TestCase):
    """docstring for CameraTest"""
    def setUp(self):
        desired_caps = {
            'device': 'android',
            'browserName': '',
            'version': '4.4',
            'app-package': 'com.intel.camera22',
            'app-activity': '.Camera'
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def _checkCamera(self):
        cameraID = commands.getoutput('adb shell ' + CAMERA_ID)
        print(cameraID)
        current = cameraID.find('0')
        print(current)
        if current == -1:
            element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
            self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
            self.driver.find_element_by_name('Front and back camera switch').click()

    def _switchToPerfectShot(self):
        self.driver.find_element_by_name('Show switch camera mode list').click()
        time.sleep(1)
        assert self.driver.find_element_by_id('com.intel.camera22:id/mode_wave_perfectshot')

        self.driver.find_element_by_id('com.intel.camera22:id/mode_wave_perfectshot').click()
        time.sleep(3)
        assert self.driver.find_element_by_name('Shutter button')

    def _setGeo(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[0].click()
        setGeo = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status == 'on':
            setGeo[4].click()
        elif status == 'off':
            setGeo[3].click()
        state = commands.getoutput('adb shell ' + Geolocation_STATE)
        assert state.find(status) != -1, 'set geolocation failed'

    def _setScenesStatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[1].click()
        setScenes = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')

        if status == 'barcode':
            setScenes[3].click()
        elif status == 'night-portrait':
            setScenes[4].click()
        elif status == 'portrait':
            setScenes[5].click()
        elif status == 'landscape':
            setScenes[6].click()
        elif status == 'night':
            setScenes[7].click()
        elif status == 'sports':
            setScenes[8].click()
        elif status == 'auto':
            setScenes[9].click()

        state = commands.getoutput('adb shell ' + Scene_STATE)
        assert state.find(status) != -1, 'set scenes failed'

    def _setExposureStatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[2].click()
        setExposure = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='6':
            setExposure[7].click()
        elif status =='3':
            setExposure[6].click()
        elif status =='0':
            setExposure[5].click()
        elif status =='-3':
            setExposure[4].click()
        elif status =='-6':
            setExposure[3].click()
        state = commands.getoutput('adb shell ' + Exposure_STATE)
        assert state.find(status) != -1, 'set Exposure failed'

    def _captureAndCheck(self):
        
        #Get the number of photo in sdcard
        result = commands.getoutput('adb shell ls ' + DCIM_PATH)
        if result.find(CAMERA_FOLDER) == -1:
            print("no 100ANDRO folder.")
            beforeNo = '0'
        #Get the number of photo in sdcard
        else:
            beforeNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep BST | wc -l')
        time.sleep(2)
        self.driver.find_element_by_name('Shutter button').click()
        time.sleep(10)
        afterNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep BST | wc -l')
        assert int(afterNo) == int(beforeNo) + 9, 'take picture fail!'

    def testCapturepictureWithGeoLocationOn(self):
        """
        Summary:testCapturepictureWithGeoLocationOn: capture PerfectShot picture in geolocation on mode
        Steps:  1.Launch perfect shot activity
                2.Check geo-tag ,set to ON
                3.Touch shutter button to capture picture
                4.Exit activity
        """ 
        self._checkCamera()
        self._switchToPerfectShot()
        self._setGeo('on')
        self._captureAndCheck()
        self._setGeo('off')

    def testCapturepictureWithGeoLocationOff(self):
        """
        Summary:testCapturepictureWithGeoLocationOff: capture PerfectShot picture in geolocation off mode
        Steps:  1.Launch perfect shot activity
                2.Check geo-tag ,set to Off
                3.Touch shutter button to capture  picture
                4.Exit activity
        """ 
        self._checkCamera()
        self._switchToPerfectShot()
        self._setGeo('off')
        self._captureAndCheck()

    def testCapturePictureWithScenesBarcode(self):
        """
        Summary:testCapturePictureWithScenesBarcode: Capture image with Scene mode Barcode
        Steps:  1.Launch perfect shot activity
        2.Set Scene mode Barcode
        3.Touch shutter button to capture picture
        4.Exit  activity 
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setScenesStatus('barcode')
        self._captureAndCheck()
        self._setScenesStatus('auto')

    def testCapturePictureWithScenesNightPortrait(self):
        """
        Summary:testCapturePictureWithScenes NightPortrait: Capture image with Scene modeNightPortrait
        Steps:  1.Launch perfect shot activity
        2.Set Scene mode Night-portrait
        3.Touch shutter button to capture picture
        4.Exit  activity 
        """ 
        self._checkCamera()
        self._switchToPerfectShot()
        self._setScenesStatus('night-portrait')
        self._captureAndCheck()
        self._setScenesStatus('auto')

    def testCapturePictureWithScenesPortrait(self):
        """
        Summary:testCapturePictureWithScenesSport: Take picture with set scenes to portrait
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to portrait
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setScenesStatus('portrait')
        self._captureAndCheck()
        self._setScenesStatus('auto')

    def testCapturePictureWithScenesLandscape(self):
        """
        Summary:testCapturePictureWithScenesLandscape: Take picture with set scenes to landscape
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to landscape
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setScenesStatus('landscape')
        self._captureAndCheck()
        self._setScenesStatus('auto')

    def testCapturePictureWithScenesNight(self):
        """
        Summary:testCapturePictureWithScenesNight: Take picture with set scenes to night
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to night
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setScenesStatus('night')
        self._captureAndCheck()
        self._setScenesStatus('auto')

    def testCapturePictureWithScenesSport(self):
        """
        Summary:testCapturePictureWithScenesSport: Take picture with set scenes to Sports
        Steps:  1Launch perfect shot activity
                2.Check scence mode ,set mode to Sports
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setScenesStatus('sports')
        self._captureAndCheck()
        self._setScenesStatus('auto')

    def testCapturePictureWithScenesAuto(self):
        """
        Summary:testCapturePictureWithScenesAuto: Take picture with set scenes to auto
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to auto
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setScenesStatus('auto')
        self._captureAndCheck()

    def testCaptureWithExposureSubtractTwo(self):
        """
        Summary:testCaptureWithExposureSubtractTwo: Take PerfectShot piture with exposure -2
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to -2
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setExposureStatus('-6')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureSubtractOne(self):
        """
        Summary:testCaptureWithExposureSubtractOne: Take PerfectShot piture with exposure -1
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to -1
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setExposureStatus('-3')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureZero(self):
        """
        Summary:testCaptureWithExposureZero: Take PerfectShot piture with exposure 0
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to 0
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setExposureStatus('0')
        self._captureAndCheck()

    def testCaptureWithExposureAddOne(self):
        """
        Summary:testCaptureWithExposureAddOne: Take PerfectShot piture with exposure +1
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to +1
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setExposureStatus('3')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureAddTwo(self):
        """
        Summary:testCapturePictureWithExposureAddOne: Take PerfectShot piture with exposure +2
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to +2
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPerfectShot()
        self._setExposureStatus('6')
        self._captureAndCheck()
        self._setExposureStatus('0')


