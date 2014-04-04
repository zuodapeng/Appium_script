import unittest
import commands
import time
from selenium import webdriver

CAMERA_ID = 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'
Geolocation_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_geo_location_key'
Exposure_STATE= 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_exposure_key'
ISO_STATE='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_iso_key'

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

    def _checkCamera(self):
        cameraID = commands.getoutput('adb shell ' + CAMERA_ID)
        print(cameraID)
        current = cameraID.find('0')
        print(current)
        if current == -1:
            element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
            self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
            self.driver.find_element_by_name('Front and back camera switch').click()

    def _switchToPanorama(self):
        self.driver.find_element_by_name('Show switch camera mode list').click()
        time.sleep(1)
        assert self.driver.find_element_by_id('com.intel.camera22:id/mode_wave_panorama')

        self.driver.find_element_by_id('com.intel.camera22:id/mode_wave_panorama').click()
        time.sleep(2)
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

    def _setExposureStatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[1].click()
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

    def _setISOsettingstatus(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[2].click()
        setExposure = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='iso-auto':
            setExposure[7].click()
        elif status =='iso-100':
            setExposure[6].click()
        elif status =='iso-200':
            setExposure[5].click()
        elif status =='iso-400':
            setExposure[4].click()
        elif status =='iso-800':
            setExposure[3].click()
        state = commands.getoutput('adb shell ' + ISO_STATE)
        assert state.find(status) != -1, 'set ISO failed'

    def _captureAndCheck(self):
        
        #Get the number of photo in sdcard
        result = commands.getoutput('adb shell ls ' + DCIM_PATH)
        if result.find(CAMERA_FOLDER) == -1:
            print("no 100ANDRO folder.")
            beforeNo = '0'
        #Get the number of photo in sdcard
        else:
            beforeNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep PAN | wc -l')
        time.sleep(2)
        self.driver.find_element_by_name('Shutter button').click()
        time.sleep(5)
        self.driver.find_element_by_name('Shutter button').click()
        time.sleep(5)
        afterNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep PAN | wc -l')
        assert int(afterNo) == int(beforeNo) + 1, 'take picture fail!'

    def testCapturepictureWithGeoLocationOn(self):
        """
        Summary:testCapturepictureWithGeoLocationOn: capture Panorama picture in geolocation on mode
        Steps:  1.Launch Panorama activity
                2.Check geo-tag ,set to ON
                3.Touch shutter button to capture picture
                4.Exit activity
        """ 
        self._checkCamera()
        self._switchToPanorama()
        self._setGeo('on')
        self._captureAndCheck()
        self._setGeo('off')

    def testCapturepictureWithGeoLocationOff(self):
        """
        Summary:testCapturepictureWithGeoLocationOff: capture Panorama picture in geolocation off mode
        Steps:  1.Launch Panorama activity
                2.Check geo-tag ,set to Off
                3.Touch shutter button to capture picture
                4.Exit activity
        """ 
        self._checkCamera()
        self._switchToPanorama()
        self._setGeo('off')
        self._captureAndCheck()

    def testCaptureWithExposureSubtractTwo(self):
        """
        Summary:testCaptureWithExposureSubtractTwo: capture Panorama picture with Exposure -2
        Steps:  1.Launch Panorama activity
                2.Check exposure setting icon ,set to -2
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPanorama()
        self._setExposureStatus('-6')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureSubtractOne(self):
        """
        Summary:testCaptureWithExposureSubtractOne: capture Panorama picture with Exposure -1
        Steps:  1.Launch Panorama activity
                2.Check exposure setting icon ,set to -1
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPanorama()
        self._setExposureStatus('-3')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureZero(self):
        """
        Summary:testCaptureWithExposureZero: capture Panorama picture with Exposure 0
        Steps:  1.Launch Panorama activity
                2.Check exposure setting icon ,set to 0
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._checkCamera()
        self._switchToPanorama()
        self._setExposureStatus('0')
        self._captureAndCheck()

    def testCaptureWithExposureAddOne(self):
        """
        Summary:testCaptureWithExposureAddOne:capture Panorama picture with Exposure +1
        Steps  : 1.Launch Panorama activity
                 2.Touch Exposure Setting icon, set Exposure +1
                 3.Touch shutter button to capture picture
                 4.Exit  activity 
        """
        self._checkCamera()
        self._switchToPanorama()
        self._setExposureStatus('3')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureAddTwo(self):
        """
        Summary:testCapturePictureWithExposureAddOne: capture Panorama picture with Exposure +2
        Steps:  1.Launch Panorama activity
                2.Touch Exposure Setting icon, set Exposure +2
                3.Touch shutter button to capture picture
                4.Exit  activity 
        """
        self._checkCamera()
        self._switchToPanorama()
        self._setExposureStatus('6')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCapturepictureWithISOSetting800(self):
        """
        Summary:testCapturepictureWithISOSetting800: Capture image with ISO Setting 800
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 800
        3.Touch shutter button
        4.Touch shutter button to capture picture
        5.Exit  activity 
        """
        self._checkCamera()
        self._switchToPanorama()
        self._setISOsettingstatus('iso-800')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    def testCapturepictureWithISOSetting400(self):
        """
        Summary:testCapturepictureWithISOSetting400: Capture image with ISO Setting 400
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 400
        3.Touch shutter button
        4.Touch shutter button to capture picture
        5.Exit  activity 
        """
        self._checkCamera()
        self._switchToPanorama()
        self._setISOsettingstatus('iso-400')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    def testCapturepictureWithISOSetting200(self):
        """
        Summary:testCapturepictureWithISOSetting200: Capture image with ISO Setting 200
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 200
        3.Touch shutter button
        4.Touch shutter button to capture picture
        5.Exit  activity    
        """
        self._checkCamera()
        self._switchToPanorama()
        self._setISOsettingstatus('iso-200')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    def testCapturepictureWithISOSetting100(self):
        """
        Summary:testCapturepictureWithISOSetting100: Capture image with ISO Setting 100
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 100
        3.Touch shutter button
        4.Touch shutter button to capture picture
        5.Exit  activity 
        """
        self._checkCamera()
        self._switchToPanorama()
        self._setISOsettingstatus('iso-100')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    def testCapturepictureWithISOSettingAuto(self):
        """
        Summary:testCapturepictureWithISOSettingAuto: Capture image with ISO Setting Auto
        Steps:  1.Launch Panorama activity
                2.Touch Geo-tag setting  icon,Set Geo-tag OFF
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity 
        """
        self._checkCamera()
        self._switchToPanorama()
        self._setISOsettingstatus('iso-auto')
        self._captureAndCheck()

