import unittest
import commands
import time
from selenium import webdriver

CAMERA_ID = 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'
Geolocation_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_geo_location_key'
PictureSize_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_picture_size_key'
Scene_STATE = 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_scenemode_key'
Exposure_STATE= 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_exposure_key'
WhiteBalance_STATE='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_whitebalance_key'
ISO_STATE='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_iso_key'
Flash_STATE= 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_flashmode_key'

DCIM_PATH = '/mnt/sdcard/DCIM'
CAMERA_FOLDER = '100ANDRO'

class CameraTest(unittest.TestCase):
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

    def _checkCamera(self, status):
        time.sleep(2)
        cameraID = commands.getoutput('adb shell ' + CAMERA_ID)
        print(cameraID)
        current = cameraID.find('0')
        print(current)
        if current == -1:
            element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
            self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
            self.driver.find_element_by_name('Front and back camera switch').click()
            time.sleep(2)
            assert commands.getoutput('adb shell ' + CAMERA_ID).find(status) != -1, 'Switch to back/front camera failed'

    def _switchToSmile(self):
        self.driver.find_element_by_name('Show switch camera mode list').click()
        time.sleep(1)
        assert self.driver.find_element_by_id('com.intel.camera22:id/mode_wave_smile')

        self.driver.find_element_by_id('com.intel.camera22:id/mode_wave_smile').click()
        time.sleep(5)
        assert self.driver.find_element_by_name('Shutter button')

    def _setGeo(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[0].click()
        setGeo = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status == 'on':
            setGeo[7].click()
        elif status == 'off':
            setGeo[6].click()
        time.sleep(1)
        state = commands.getoutput('adb shell ' + Geolocation_STATE)
        assert state.find(status) != -1, 'set geolocation failed'

    def _setSize(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[1].click()
        setSize = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status == 'StandardScreen':
            setSize[7].click()
        elif status == 'WideScreen':
            setSize[6].click()
        time.sleep(1)
        state = commands.getoutput('adb shell ' + PictureSize_STATE)
        assert state.find(status) != -1, 'set picture size failed'

    def _setScenesStatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[2].click()
        setScenes = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')

        if status == 'barcode':
            setScenes[6].click()
        elif status == 'night-portrait':
            setScenes[7].click()
        elif status == 'portrait':
            setScenes[8].click()
        elif status == 'landscape':
            setScenes[9].click()
        elif status == 'night':
            setScenes[10].click()
        elif status == 'sports':
            setScenes[11].click()
        elif status == 'auto':
            setScenes[12].click()
        time.sleep(1)
        state = commands.getoutput('adb shell ' + Scene_STATE)
        assert state.find(status) != -1, 'set scenes failed'

    def _setScenesToAuto(self):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[2].click()
        setScenes = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        setScenes[11].click()
        time.sleep(1)
        state = commands.getoutput('adb shell ' + Scene_STATE)
        assert state.find('auto') != -1, 'set scenes failed'

    def _setExposureStatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[3].click()
        setExposure = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='6':
            setExposure[10].click()
        elif status =='3':
            setExposure[9].click()
        elif status =='0':
            setExposure[8].click()
        elif status =='-3':
            setExposure[7].click()
        elif status =='-6':
            setExposure[6].click()
        time.sleep(1)
        state = commands.getoutput('adb shell ' + Exposure_STATE)
        assert state.find(status) != -1, 'set Exposure failed'

    def _setWBstatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[4].click()
        setExposure = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='auto':
            setExposure[10].click()
        elif status =='incandescent':
            setExposure[9].click()
        elif status =='daylight':
            setExposure[8].click()
        elif status =='fluorescent':
            setExposure[7].click()
        elif status =='cloudy-daylight':
            setExposure[6].click()
        time.sleep(1)
        state = commands.getoutput('adb shell ' + WhiteBalance_STATE)
        assert state.find(status) != -1, 'set WhiteBalance failed'

    def _setISOsettingstatus(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()
        self.driver.execute_script("mobile: swipe", {"startX":"640", "startY":"180", "endX":"100", "endY":"180"})

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[5].click()
        setExposure = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='iso-auto':
            setExposure[10].click()
        elif status =='iso-100':
            setExposure[9].click()
        elif status =='iso-200':
            setExposure[8].click()
        elif status =='iso-400':
            setExposure[7].click()
        elif status =='iso-800':
            setExposure[6].click()
        time.sleep(1)
        state = commands.getoutput('adb shell ' + ISO_STATE)
        assert state.find(status) != -1, 'set ISO failed'

    def _setFlashStatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Flash settings').click()

        setFlash = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='auto':
            setFlash[2].click()
        elif status =='on':
            setFlash[1].click()
        elif status =='off':
            setFlash[0].click()
        time.sleep(1)
        state = commands.getoutput('adb shell ' + Flash_STATE)
        assert state.find(status) != -1, 'set Flash failed'

    def _captureAndCheck(self):
        
        #Get the number of photo in sdcard
        result = commands.getoutput('adb shell ls ' + DCIM_PATH)
        if result.find(CAMERA_FOLDER) == -1:
            print("no 100ANDRO folder.")
            beforeNo = '0'
        #Get the number of photo in sdcard
        else:
            beforeNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep IMG | wc -l')
        time.sleep(2)
        self.driver.find_element_by_name('Shutter button').click()
        time.sleep(5)
        self.driver.find_element_by_name('Shutter button').click()
        time.sleep(5)
        afterNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep IMG | wc -l')
        assert int(afterNo) == int(beforeNo) + 1, 'take picture fail!'

    def testCapturepictureWithGeoLocationOn(self):
        """
        Summary:testCapturepictureWithGeoLocationOn:Take a picture with  geolocation is on
        Steps:  1.Launch SmileCam activity
                2.Check geo-tag ,set to ON
                3.Touch shutter button to capture picture
                4.Exit  activity
        """ 
        self._checkCamera('0')
        self._switchToSmile()
        self._setGeo('on')
        self._captureAndCheck()
        self._setGeo('off')

    def testCapturepictureWithGeoLocationOff(self):
        """
        Summary:testCapturepictureWithGeoLocationOff: Take a picture with  geolocation is off
        Steps:  1.Launch SmileCam activity
                2.Check geo-tag ,set to Off
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setGeo('off')
        self._captureAndCheck()

    def testCapturePictureWithPictureSizeStandard(self):
        """
        Summary:testCapturePictureWithPictureSizeStandard: Take a picture with picture size is standard
        Steps:  1.Launch SmileCam activity
                2.Check photo size ,set to 8M
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setSize('StandardScreen')
        self._captureAndCheck()
        self._setSize('WideScreen')

    def testCaptureWithPictureSizeWidesreen(self):
        """
        Summary:testCaptureWithSize6M: Take a picture with  picture size is Widesreen
        Steps:  1.Launch SmileCam activity
                2.Check photo size ,set to 6M
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setSize('WideScreen')
        self._captureAndCheck()

    def testCapturePictureWithScenesBarcode(self):
        """
        Summary:testCapturePictureWithScenesBarcode: Capture image with Scene mode barcode
        Steps:  1.Launch single capture activity
                2.Set scene mode barcode
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setScenesStatus('barcode')
        self._captureAndCheck()
        self._setScenesToAuto()

    def testCapturePictureWithScenesNightPortrait(self):
        """
        Summary:testCapturePictureWithScenesNightPortrait: Capture image with Scene mode Night-portrait
        Steps:  1.Launch SmileCam activity
                2.Check scence mode ,set mode to Night-portrait
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setScenesStatus('night-portrait')
        self._captureAndCheck()
        self._setScenesToAuto()

    def testCapturePictureWithScenesPortrait(self):
        """
        Summary:testCapturePictureWithScenesPortrait: Take a picture with set scenes to Portrait
        Steps:  1.Launch SmileCam activity
                2.Check scence mode ,set mode to Portrait
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setScenesStatus('portrait')
        self._captureAndCheck()
        self._setScenesToAuto()

    def testCapturePictureWithScenesLandscape(self):
        """
        Summary:testCapturePictureWithScenesLandscape: Take a picture with set scenes to Landscape
        Steps:  1.Launch SmileCam activity
                2.Check scence mode ,set mode to Landscape
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setScenesStatus('landscape')
        self._captureAndCheck()
        self._setScenesToAuto()

    def testCapturePictureWithScenesNight(self):
        """
        Summary:testCapturePictureWithScenesNight: Take a picture with set scenes to Night
        Steps:  1.Launch SmileCam activity
                2.Check scence mode ,set mode to Night
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setScenesStatus('night')
        self._captureAndCheck()
        self._setScenesToAuto()

    def testCapturePictureWithScenesSport(self):
        """
        Summary:testCapturePictureWithScenesSport: Take a picture with set scenes to Sports
        Steps:  1.Launch SmileCam activity
                2.Check scence mode ,set mode to Sports
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setScenesStatus('sports')
        self._captureAndCheck()
        self._setScenesToAuto()

    def testCapturePictureWithScenesAuto(self):
        """
        Summary:testCapturePictureWithScenesAuto: Take a picture with set scenes to Auto
        Steps:  1.Launch SmileCam activity
                2.Check scence mode ,set mode to Auto
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setScenesStatus('auto')
        self._captureAndCheck()

    def testCaptureWithExposureSubtractTwo(self):
        """
        Summary:testCaptureWithExposureSubtractOne: Take a picture with Exposure -2
        Steps: 1.Launch SmileCam activity
               2.Check exposure setting icon ,set to -2
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setExposureStatus('-6')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureSubtractOne(self):
        """
        Summary:testCaptureWithExposureSubtractOne: Take a picture with Exposure -1
        Steps: 1.Launch SmileCam activity
               2.Check exposure setting icon ,set to -1
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setExposureStatus('-3')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureZero(self):
        """
        Summary:testCaptureWithExposureZero: Take a picture with Exposure 0
        Steps: 1.Launch SmileCam activity
               2.Check exposure setting icon ,set to 0
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setExposureStatus('0')
        self._captureAndCheck()

    def testCaptureWithExposureAddOne(self):
        """
        Summary:testCaptureWithExposureAddOne: Take a picture with Exposure +1
        Steps: 1.Launch SmileCam activity
               2.Check exposure setting icon ,set to 1
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setExposureStatus('3')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureAddTwo(self):
        """
        Summary:testCaptureWithExposureAddTwo: Take a picture with Exposure +2
        Steps: 1.Launch SmileCam activity
               2.Check exposure setting icon ,set to 2
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setExposureStatus('6')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCapturepictureWithWhiteBalanceAuto(self):
        """
        Summary:testCapturepictureWithWhiteBalanceAuto: Capture image with White Balance Auto
        Steps:  1.Launch SmileCam capture activity
                2.Set White Balance Auto
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setWBstatus('auto')
        self._captureAndCheck()

    # Test case 28
    def testCapturepictureWithWhiteBalanceIncandescent(self):
        """
        Summary:testCapturepictureWithWhiteBalanceIncandescent: Capture image with White Balance Incandescent
        Steps:  1.Launch SmileCam capture activity
                2.Set White Balance Incandescent
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setWBstatus('incandescent')
        self._captureAndCheck()
        self._setWBstatus('auto')

    # Test case 29
    def testCapturepictureWithWhiteBalanceDaylight(self):
        """
        Summary:testCapturepictureWithWhiteBalanceDaylight: Capture image with White Balance Daylight
        Steps:  1.Launch SmileCam capture activity
                2.Set White Balance Daylight
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setWBstatus('daylight')
        self._captureAndCheck()
        self._setWBstatus('auto')

    # Test case 30
    def testCapturepictureWithWhiteBalanceFluorescent(self):
        """
        Summary:testCapturepictureWithWhiteBalanceFluorescent: Capture image with White Balance Fluorescent
        Steps:  1.Launch SmileCam capture activity
                2.Set White Balance Fluorescent
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setWBstatus('fluorescent')
        self._captureAndCheck()
        self._setWBstatus('auto')

    # Test case 31
    def testCapturepictureWithWhiteBalanceCloudy(self):
        """
        Summary:testCapturepictureWithWhiteBalanceCloudy: Capture image with White Balance Cloudy
        Steps:  1.Launch SmileCam capture activity
                2.Set White Balance Cloudy
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setWBstatus('cloudy-daylight')
        self._captureAndCheck()
        self._setWBstatus('auto')

    def testCapturepictureWithISOAuto(self):
        """
        Summary:testCapturepictureWithISOAuto: Capture image with ISO Setting Auto
        Steps:  1.Launch SmileCam capture activity
                2.Set ISO Setting Auto
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setISOsettingstatus('iso-auto')
        self._captureAndCheck()

    # Test case 24
    def testCapturepictureWithISO100(self):
        """
        Summary:testCapturepictureWithISOHundred: Capture image with ISO Setting 100
        Steps:  1.Launch SmileCam capture activity
                2.Set ISO Setting 100
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setISOsettingstatus('iso-100')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    # Test case 25
    def testCapturepictureWithISO200(self):
        """
        Summary:testCapturepictureWithISOTwoHundred: Capture image with ISO Setting 200
        Steps:  1.Launch SmileCam capture activity
                2.Set ISO Setting 200
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setISOsettingstatus('iso-200')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    # Test case 26
    def testCapturepictureWithISO400(self):
        """
        Summary:testCapturepictureWithISOFourHundred: Capture image with ISO Setting 400
        Steps:  1.Launch SmileCam capture activity
                2.Set ISO Setting 400
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setISOsettingstatus('iso-400')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    # Test case 27
    def testCapturepictureWithISO800(self):
        """
        Summary:testCapturepictureWithISOEightHundred: Capture image with ISO Setting 800
        Steps:  1.Launch SmileCam capture activity
                2.Set ISO Setting 800
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setISOsettingstatus('iso-800')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    def testCapturePictureWithFlashOn(self):
        """
        Summary:testCapturePictureWithFlashOn: Take a picture with flash on
        Steps: 1.Launch SmileCam activity
               2.Check flash state,set to ON
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setFlashStatus('on')
        self._captureAndCheck()
        self._setFlashStatus('auto')

    # Test case 2
    def testCapturePictureWithFlashOff(self):
        """
        Summary:testCapturePictureWithFlashOff: Take a picture with flash off
        Steps:  1.Launch SmileCam activity
                2.Check flash state, set to OFF
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setFlashStatus('off')
        self._captureAndCheck()
        self._setFlashStatus('auto')

    def testCapturePictureWithFlashAuto(self):
        """
        Summary:testCapturePictureWithFlashAuto: Take a picture with flash auto
        Steps:  1.Launch SmileCam activity
                2.Check flash state, set to AUTO
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera('0')
        self._switchToSmile()
        self._setFlashStatus('auto')
        self._captureAndCheck()
