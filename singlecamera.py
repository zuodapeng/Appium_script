import unittest
import commands
import time
from selenium import webdriver

CAMERA_ID = 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'
Hints_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_hints_key'
Geolocation_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_geo_location_key'
PictureSize_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_picture_size_key'
Scene_STATE = 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_scenemode_key'
Exposure_STATE= 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_exposure_key'
WhiteBalance_STATE='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_whitebalance_key'
ISO_STATE='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_iso_key'
SelfTimer_STATE='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_delay_shooting_key'
Flash_STATE= 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_flashmode_key'
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

    def tearDown(self):
        self.driver.back()
        self.driver.back()
        self.driver.quit()

    def _setCamera(self,status):
        # status == 0 is back camera, status == 1 is front camera
        time.sleep(2)
        cameraID = commands.getoutput('adb shell ' + CAMERA_ID)
        print(cameraID)
        current = cameraID.find(status)
        print(current)
        if current == -1:
            element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
            self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
            self.driver.find_element_by_name('Front and back camera switch').click()

            time.sleep(2)
            assert commands.getoutput('adb shell ' + CAMERA_ID).find(status) != -1, 'Switch to back/front camera failed'

    def _setHint(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[1].click()
        setHint = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status == 'on':
            setHint[8].click()
        elif status == 'off':
            setHint[7].click()
        state = commands.getoutput('adb shell ' + Hints_STATE)
        assert state.find(status) != -1, 'set hints failed'

    def _setGeo(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[2].click()
        setGeo = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status == 'on':
            setGeo[8].click()
        elif status == 'off':
            setGeo[7].click()
        state = commands.getoutput('adb shell ' + Geolocation_STATE)
        assert state.find(status) != -1, 'set geolocation failed'

    def _setFrontGeo(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_element_by_id('com.intel.camera22:id/hori_list_button')
        options.click()
        setGeo = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status == 'on':
            setGeo[2].click()
        elif status == 'off':
            setGeo[1].click()
        state = commands.getoutput('adb shell ' + Geolocation_STATE)
        assert state.find(status) != -1, 'set geolocation failed'

    def _setSize(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[3].click()
        setSize = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status == 'StandardScreen':
            setSize[8].click()
        elif status == 'WideScreen':
            setSize[7].click()
        state = commands.getoutput('adb shell ' + PictureSize_STATE)
        assert state.find(status) != -1, 'set picture size failed'

    def _setScenes(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[4].click()
        setScenes = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')

        if status == 'barcode':
            setScenes[7].click()
        elif status == 'night-portrait':
            setScenes[8].click()
        elif status == 'portrait':
            setScenes[9].click()
        elif status == 'landscape':
            setScenes[10].click()
        elif status == 'night':
            setScenes[11].click()
        elif status == 'sports':
            setScenes[12].click()
        elif status == 'auto':
            setScenes[13].click()


        state = commands.getoutput('adb shell ' + Scene_STATE)
        assert state.find(status) != -1, 'set scenes failed'

    def _setExposureStatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[5].click()
        setExposure = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='6':
            setExposure[11].click()
        elif status =='3':
            setExposure[10].click()
        elif status =='0':
            setExposure[9].click()
        elif status =='-3':
            setExposure[8].click()
        elif status =='-6':
            setExposure[7].click()
        state = commands.getoutput('adb shell ' + Exposure_STATE)
        assert state.find(status) != -1, 'set Exposure failed'

    def _setWBstatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[6].click()
        setExposure = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='auto':
            setExposure[11].click()
        elif status =='incandescent':
            setExposure[10].click()
        elif status =='daylight':
            setExposure[9].click()
        elif status =='fluorescent':
            setExposure[8].click()
        elif status =='cloudy-daylight':
            setExposure[7].click()
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
            setExposure[11].click()
        elif status =='iso-100':
            setExposure[10].click()
        elif status =='iso-200':
            setExposure[9].click()
        elif status =='iso-400':
            setExposure[8].click()
        elif status =='iso-800':
            setExposure[7].click()
        state = commands.getoutput('adb shell ' + ISO_STATE)
        assert state.find(status) != -1, 'set ISO failed'

    def _setSelftTimerstatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()
        self.driver.execute_script("mobile: swipe", {"startX":"640", "startY":"180", "endX":"100", "endY":"180"})

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[6].click()
        setExposure = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='10':
            setExposure[10].click()
        elif status =='5':
            setExposure[9].click()
        elif status =='3':
            setExposure[8].click()
        elif status =='0':
            setExposure[7].click()
        state = commands.getoutput('adb shell ' + SelfTimer_STATE)
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

        state = commands.getoutput('adb shell ' + Flash_STATE)
        assert state.find(status) != -1, 'set flash failed'

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
        assert int(afterNo) > int(beforeNo), 'take picture fail!'

    def testCapturepictureWithHintsOn(self):
        """
        Summary:testCapturepictureWithHintsOn: Take a picture with  hints is on
        Steps:  1.Launch camera app
                2.Set hints on
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setHint('on')
        self._captureAndCheck()
        self._setHint('off')

    def testCapturepictureWithHintsOff(self):
        """
        Summary:testCapturepictureWithHintsOff: Take a picture with  hints is off
        Steps:  1.Launch camera app
                2.Set hints off
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setHint('off')
        self._captureAndCheck()

    def testCapturepictureWithGeoLocationOn(self):
        """
        Summary:testCapturepictureWithGeoLocationOn:Take a picture with  geolocation is on
        Steps:  1.Launch camera app
                2.Set geo location on 
                3.Touch shutter button to capture picture
                4.Exit  activity
        """ 
        self._setCamera('0')
        self._setGeo('on')
        self._captureAndCheck()
        self._setGeo('off')

    def testCapturepictureWithGeoLocationOff(self):
        """
        Summary:testCapturepictureWithGeoLocationOff: Take a picture with  geolocation is off
        Steps:  1.Launch camera app
                2.Set geo location off 
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setGeo('off')
        self._captureAndCheck()

    def testCaptureWithPictureSizeWidesreen(self):
        """
        Summary:testCaptureWithSize6M: Take a picture with  picture size is Widesreen
        Steps:  1.Launch single capture activity
                2.Set picture size is Widesreen
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setSize('WideScreen')
        self._captureAndCheck()

    def testCapturePictureWithPictureSizeStandard(self):
        """
        Summary:testCapturePictureWithPictureSizeStandard: Take a picture with picture size is standard
        Steps:  1.Launch single capture activity
                2.Set picture size is standard
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setSize('StandardScreen')
        self._captureAndCheck()
        self._setSize('WideScreen')

    def testCapturePictureWithScenesBarcode(self):
        """
        Summary:testCapturePictureWithScenesBarcode: Capture image with Scene mode barcode
        Steps:  1.Launch single capture activity
                2.Set scene mode barcode
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setScenes('barcode')
        self._captureAndCheck()
        self._setScenes('auto')

    def testCapturePictureWithScenesNightportrait(self):
        """
        Summary:testCapturePictureWithScenesNightportrait: Capture image with Scene mode Night-portrait
        Steps:  1.Launch single capture activity
                2.Set scene mode night-portrait
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setScenes('night-portrait')
        self._captureAndCheck()
        self._setScenes('auto')

    def testCapturePictureWithScenesPortrait(self):
        """
        Summary:testCapturePictureWithScenesPortrait: Take a picture with set scenes to Portrait
        Steps:  1.Launch single capture activity
                2.Set scene mode Portrait
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setScenes('portrait')
        self._captureAndCheck()
        self._setScenes('auto')

    def testCapturePictureWithScenesLandscape(self):
        """
        Summary:testCapturePictureWithScenesLandscape: Take a picture with set scenes to Landscape
        Steps:  1.Launch single capture activity
                2.Set scene mode Landscape
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setScenes('landscape')
        self._captureAndCheck()
        self._setScenes('auto')

    def testCapturePictureWithScenesNight(self):
        """
        Summary:testCapturePictureWithScenesNight: Take a picture with set scenes to Night
        Steps:  1.Launch single capture activity
                2.Set scene mode Night
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setScenes('night')
        self._captureAndCheck()
        self._setScenes('auto')

    def testCapturePictureWithScenesSport(self):
        """
        Summary:testCapturePictureWithScenesSport: Take a picture with set scenes to Sports
        Steps:  1.Launch single capture activity
                2.Set scene mode Sports
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setScenes('sports')
        self._captureAndCheck()
        self._setScenes('auto')

    def testCapturePictureWithScenesAuto(self):
        """
        Summary:testCapturePictureWithScenesAuto: Take a picture with set scenes to Auto
        Steps:  1.Launch single capture activity
                2.Set scene mode Auto
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setScenes('auto')
        self._captureAndCheck()

    def testCaptureWithExposureSubtractTwo(self):
        """
        Summary:testCaptureWithExposureRedOne: Take a picture with Exposure -2
        Steps: 1.Launch single capture activity
               2.Set exposure -2
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._setCamera('0')
        self._setExposureStatus('-6')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureSubtractOne(self):
        """
        Summary:testCaptureWithExposureRedOne: Take a picture with Exposure -1
        Steps: 1.Launch single capture activity
               2.Set exposure -1
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._setCamera('0')
        self._setExposureStatus('-3')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureZero(self):
        """
        Summary:testCaptureWithExposureZero: Take a picture with Exposure 0
        Steps: 1.Launch single capture activity
               2.Set exposure 0
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._setCamera('0')
        self._setExposureStatus('0')
        self._captureAndCheck()

    def testCaptureWithExposureAddOne(self):
        """
        Summary:testCaptureWithExposurePlusOne: Take a picture with Exposure +1
        Steps: 1.Launch single capture activity
               2.Set exposure +1
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._setCamera('0')
        self._setExposureStatus('3')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCaptureWithExposureAddTwo(self):
        """
        Summary:testCaptureWithExposurePlusTwo: Take a picture with Exposure +2
        Steps: 1.Launch single capture activity
               2.Set exposure +2
               3.Touch shutter button to capture picture
               4.Exit  activity
        """
        self._setCamera('0')
        self._setExposureStatus('6')
        self._captureAndCheck()
        self._setExposureStatus('0')

    def testCapturepictureWithWhiteBalanceCloudy(self):
        """
        Summary:testCapturepictureWithWhiteBalanceCloudy: Capture image with White Balance Cloudy
        Steps:  1.Launch single capture activity
                2.Set White Balance Cloudy
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setWBstatus('cloudy-daylight')
        self._captureAndCheck()
        self._setWBstatus('auto')

    def testCapturepictureWithWhiteBalanceFluorescent(self):
        """
        Summary:testCapturepictureWithWhiteBalanceFluorescent: Capture image with White Balance Fluorescent
        Steps:  1.Launch single capture activity
                2.Set White Balance Fluorescent
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setWBstatus('fluorescent')
        self._captureAndCheck()
        self._setWBstatus('auto')

    def testCapturepictureWithWhiteBalanceDaylight(self):
        """
        Summary:testCapturepictureWithWhiteBalanceDaylight: Capture image with White Balance Daylight
        Steps:  1.Launch single capture activity
                2.Set White Balance Daylight
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setWBstatus('daylight')
        self._captureAndCheck()
        self._setWBstatus('auto')

    def testCapturepictureWithWhiteBalanceIncandescent(self):
        """
        Summary:testCapturepictureWithWhiteBalanceIncandescent: Capture image with White Balance Incandescent
        Steps:  1.Launch single capture activity
                2.Set White Balance Incandescent
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setWBstatus('incandescent')
        self._captureAndCheck()
        self._setWBstatus('auto')

    def testCapturepictureWithWhiteBalanceAuto(self):
        """
        Summary:testCapturepictureWithWhiteBalanceAuto: Capture image with White Balance Auto
        Steps:  1.Launch single capture activity
                2.Set White Balance Auto
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setWBstatus('auto')
        self._captureAndCheck()

    def testCapturepictureWithISOAuto(self):
        """
        Summary:testCapturepictureWithISOAuto: Capture image with ISO Setting Auto
        Steps:  1.Launch single capture activity
                2.Set ISO Setting Auto
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setISOsettingstatus('iso-auto')
        self._captureAndCheck()

    def testCapturepictureWithISO100(self):
        """
        Summary:testCapturepictureWithISOHundred: Capture image with ISO Setting 100
        Steps:  1.Launch single capture activity
                2.Set ISO Setting 100
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setISOsettingstatus('iso-100')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    def testCapturepictureWithISO200(self):
        """
        Summary:testCapturepictureWithISOTwoHundred: Capture image with ISO Setting 200
        Steps:  1.Launch single capture activity
                2.Set ISO Setting 200
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setISOsettingstatus('iso-200')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    def testCapturepictureWithISO400(self):
        """
        Summary:testCapturepictureWithISOFourHundred: Capture image with ISO Setting 400
        Steps:  1.Launch single capture activity
                2.Set ISO Setting 400
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setISOsettingstatus('iso-400')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    def testCapturepictureWithISOEightHundred(self):
        """
        Summary:testCapturepictureWithISOEightHundred: Capture image with ISO Setting 800
        Steps:  1.Launch single capture activity
                2.Set ISO Setting 800
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setISOsettingstatus('iso-800')
        self._captureAndCheck()
        self._setISOsettingstatus('iso-auto')

    def testCapturepictureWithSelfTimerOff(self):
        """
        Summary:testCapturepictureWithSelfTimerOff: Capture image with Self-timer off
        Steps:  1.Launch single capture activity
                2.Set Self-timer off
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setSelftTimerstatus('0')
        self._captureAndCheck()

    def testCapturepictureWithSelfTimerThreeSec(self):
        """
        Summary:testCapturepictureWithSelfTimerThreeSec: Capture image with Self-timer 3s
        Steps:  1.Launch single capture activity
                2.Set Self-timer 3s
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setSelftTimerstatus('3')
        self._captureAndCheck()
        self._setSelftTimerstatus('0')

    def testCapturepictureWithSelfTimerFiveSec(self):
        """
        Summary:testCapturepictureWithSelfTimerFiveSec: Capture image with Self-timer 5s
        Steps:  1.Launch single capture activity
                2.Set Self-timer 5s
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setSelftTimerstatus('5')
        self._captureAndCheck()
        self._setSelftTimerstatus('0')

    def testCapturepictureWithSelfTimerTenSec(self):
        """
        Summary:testCapturepictureWithSelfTimerTenSec: Capture image with Self-timer 10s
        Steps:  1.Launch single capture activity
                2.Set Self-timer 10s
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setSelftTimerstatus('10')
        self._captureAndCheck()
        self._setSelftTimerstatus('0')

    def testCapturePictureWithFlashOn(self):
        """
        Summary:testCapturePictureWithFlashOn: Take a picture with flash on
        Steps:  1.Launch single capture activity
                2.Set flash ON
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setFlashStatus('on')
        self._captureAndCheck()
        self._setFlashStatus('auto')

    def testCapturePictureWithFlashOff(self):
        """
        Summary:testCapturePictureWithFlashOff: Take a picture with flash off
        Steps:  1.Launch single capture activity
                2.Set flash Off
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setFlashStatus('off')
        self._captureAndCheck()
        self._setFlashStatus('auto')

    def testCapturePictureWithFlashAuto(self):
        """
        Summary:testCapturePictureWithFlashAuto: Take a picture with flash auto
        Steps:  1.Launch single capture activity
                2.Set flash auto
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setFlashStatus('auto')
        self._captureAndCheck()

    def testCapturePictureWithFDON(self):
        """
        Summary:testCapturePictureWithFDON: Take a picture with set FD/FR on
        Steps:  1.Launch single capture activity
                2.Set FD/FR ON
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setFDFRStatus('on')
        self._captureAndCheck()

    def testCapturePictureWithFDOff(self):
        """
        Summary:testCapturePictureWithFDOff: Take a picture with set FD/FR off
        Steps:  1.Launch single capture activity
                2.Set FD/FR Off
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('0')
        self._setFDFRStatus('off')
        self._captureAndCheck()
        self._setFDFRStatus('on')

    def testRearFaceCapturepictureWithGeoLocationOn(self):
        """
        Summary:testRearFaceCapturepictureWithGeoLocationOn: Take a picture using fear face camera and set geolocation on 
        Steps:  1.Launch camera app
                2.Set geolocation on 
                3.Touch shutter button to capture picture
                4.Exit  activity
        """ 
        self._setCamera('1')
        self._setFrontGeo('on')
        self._captureAndCheck()
        self._setFrontGeo('off')

    def testRearFaceCapturepictureWithGeoLocationOff(self):
        """
        Summary:testRearFaceCapturepictureWithGeoLocationOff: Take a picture using fear face camera and set geolocation off
        Steps:  1.Launch camera app
                2.Set geo location off 
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('1')
        self._setFrontGeo('off')
        self._captureAndCheck()

    def testRearFaceCapturePictureWithFDOff(self):
        """
        Summary:testRearFaceCapturePictureWithFDOff: Take a picture using fear face camera and set FD/FR off
        Steps:  1.Launch single capture activity
                2.Set FD/FR Off
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('1')
        self._setFDFRStatus('off')
        self._captureAndCheck()
        self._setFDFRStatus('on')

    def testRearFaceCapturePictureWithFDON(self):
        """
        Summary:testRearFaceCapturePictureWithFDON: Take a picture using fear face camera and set FD/FR on
        Steps:  1.Launch single capture activity
                2.Set FD/FR ON
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        self._setCamera('1')
        self._setFDFRStatus('on')
        self._captureAndCheck()
