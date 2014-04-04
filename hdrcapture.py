import unittest
import commands
import time
from selenium import webdriver

CAMERA_ID = 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'
Geolocation_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_geo_location_key'
PictureSize_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_picture_size_key'
SelfTimer_STATE='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_delay_shooting_key'
FDFR_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_fdfr_key'

DCIM_PATH = '/mnt/sdcard/DCIM'
CAMERA_FOLDER = '100ANDRO'



class CameraTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {
            'device': 'android',
            'version': '4.4',
            'browserName': '',
            'app-package': 'com.intel.camera22',
            'app-activity': '.Camera'
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self._checkCamera('0')

    def tearDown(self):
        self.driver.back()
        self.driver.back()
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

    def _switchToHDR(self):
        self.driver.find_element_by_name('Show switch camera mode list').click()
        time.sleep(1)
        assert self.driver.find_element_by_id('com.intel.camera22:id/mode_wave_hdr')

        self.driver.find_element_by_id('com.intel.camera22:id/mode_wave_hdr').click()
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
            setGeo[4].click()
        elif status == 'off':
            setGeo[3].click()
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
            setSize[4].click()
        elif status == 'WideScreen':
            setSize[3].click()
        state = commands.getoutput('adb shell ' + PictureSize_STATE)
        assert state.find(status) != -1, 'set picture size failed'

    def _setSelftTimerstatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()
        self.driver.execute_script("mobile: swipe", {"startX":"640", "startY":"180", "endX":"100", "endY":"180"})

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[2].click()
        setExposure = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='10':
            setExposure[6].click()
        elif status =='5':
            setExposure[5].click()
        elif status =='3':
            setExposure[4].click()
        elif status =='0':
            setExposure[3].click()
        state = commands.getoutput('adb shell ' + SelfTimer_STATE)
        assert state.find(status) != -1, 'set ISO failed'

    def _setFDFRStatus(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        current = commands.getoutput('adb shell ' + FDFR_STATE)
        if current.find(status) == -1:
            self.driver.find_element_by_name('Face recognition').click()

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
        time.sleep(15)
        afterNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep IMG | wc -l')
        assert int(afterNo) == int(beforeNo) + 1, 'take picture fail!'

    def testCapturepictureWithGeoLocationOn(self):
        """
        Summary:testCapturepictureWithGeoLocationOn:Take a picture with  geolocation is on
        Steps:  1,Launch HDR capture activity
                2.Set photo Geo-tag ON
                3.Touch shutter button to capture picture
                4.Exit  activity
        """ 
        self._switchToHDR()
        self._setGeo('on')
        self._captureAndCheck()
        self._setGeo('off')

    def testCapturepictureWithGeoLocationOff(self):
        """
        Summary:testCapturepictureWithGeoLocationOff: Take a picture with  geolocation is off
        Steps:  1,Launch HDR capture activity
                2.Set photo Geo-tag OFF
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._switchToHDR()
        self._setGeo('off')
        self._captureAndCheck()

    def testCapturePictureWithPictureSizeStandard(self):
        """
        Summary:testCapturePictureWithPictureSizeStandard: Take a picture with picture size is standard
        Steps:  1,Launch HDR capture activity
                2.Set photo size 8M
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._switchToHDR()
        self._setSize('StandardScreen')
        self._captureAndCheck()
        self._setSize('WideScreen')

    def testCaptureWithPictureSizeWidesreen(self):
        """
        Summary:testCaptureWithSize6M: Take a picture with  picture size is Widesreen
        Steps:  1,Launch HDR capture activity
                2.Set photo size 6M
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._switchToHDR()
        self._setSize('WideScreen')
        self._captureAndCheck() 

    def testCapturePictureWithSelfTimerOff(self):
        """
        Summary:testCapturePictureWithSelfTimerOff: Capture image with Self-timer off
        Steps:  1.Launch HDR capture activity
                2.Set Self-timer off
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._switchToHDR()
        self._setSelftTimerstatus('0')
        self._captureAndCheck() 

    def testCapturePictureWithThreeSec(self):
        """
        Summary:testCapturePictureWithThreeSec: Capture image with Self-timer 3s
        Steps:  1.Launch HDR capture activity
                2.Set Self-timer 3s
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._switchToHDR()
        self._setSelftTimerstatus('3')
        self._captureAndCheck() 
        self._setSelftTimerstatus('0')

    def testCapturePictureWithFiveSec(self):
        """
        Summary:testCapturePictureWithFiveSec: Capture image with Self-timer 5s
        Steps:  1.Launch HDR capture activity
                2.Set Self-timer 5s
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._switchToHDR()
        self._setSelftTimerstatus('5')
        self._captureAndCheck() 
        self._setSelftTimerstatus('0')

    def testCapturePictureWithTenSec(self):
        """
        Summary:testCapturePictureWithTenSec: Capture image with Self-timer 10s
        Steps:  1.Launch HDR capture activity
                2.Set Self-timer 10s
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._switchToHDR()
        self._setSelftTimerstatus('10')
        self._captureAndCheck() 
        self._setSelftTimerstatus('0')

    def testCapturePictureWithFDOn(self):
        """
        Summary:testCapturePictureWithFDOn: Take a picture with FD/FR on
        Steps:  1.Launch HDR capture activity
                2.Set FD/FR ON
                3.Touch shutter button to capture picture
                4.Exit activity
        """
        self._switchToHDR()
        self._setFDFRStatus('on')
        self._captureAndCheck() 

    def testCapturePictureWithFDOff(self):
        """
        Summary:testCapturePictureWithFDOff: Take a picture with set FD/FR off
        Steps:  1.Launch HDR capture activity
                2.Set FD/FR OFF
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._switchToHDR()
        self._setFDFRStatus('off')
        self._captureAndCheck() 
        self._setFDFRStatus('on')

    