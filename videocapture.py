import unittest
import commands
import time
from selenium import webdriver

CAMERA_ID = 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'
Geolocation_STATE ='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_geo_location_key'
Exposure_STATE= 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_exposure_key'
WhiteBalance_STATE='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_whitebalance_key'
Flash_STATE= 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_video_flashmode_key'
VideoSize_STATE= 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_video_quality_key'

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

    def _switchToVideo(self):
        self.driver.find_element_by_name('Show switch camera mode list').click()
        time.sleep(1)
        assert self.driver.find_element_by_id('com.intel.camera22:id/mode_wave_video')

        self.driver.find_element_by_id('com.intel.camera22:id/mode_wave_video').click()
        time.sleep(5)
        assert self.driver.find_element_by_name('Shutter button')

    def _setGeo(self, status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[1].click()
        setGeo = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status == 'on':
            setGeo[6].click()
        elif status == 'off':
            setGeo[5].click()
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

    def _setVideoSizeStatus(self,status,hs):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[2].click()
        setVideoSize = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status == '6' and hs == '1':
            setVideoSize[9].click()
        elif status == '6' and hs == '0':
            setVideoSize[8].click()
        elif status == '5' and hs == '1':
            setVideoSize[7].click()
        elif status == '5' and hs == '0':
            setVideoSize[6].click()
        elif status == '4' and hs == '0':
            setVideoSize[5].click()
        state = commands.getoutput('adb shell ' + VideoSize_STATE)
        assert state.find(status) != -1, 'set geolocation failed'

    def _setExposureStatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Camera settings').click()

        options = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        options[3].click()
        setExposure = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='6':
            setExposure[9].click()
        elif status =='3':
            setExposure[8].click()
        elif status =='0':
            setExposure[7].click()
        elif status =='-3':
            setExposure[6].click()
        elif status =='-6':
            setExposure[5].click()
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
            setExposure[9].click()
        elif status =='incandescent':
            setExposure[8].click()
        elif status =='daylight':
            setExposure[7].click()
        elif status =='fluorescent':
            setExposure[6].click()
        elif status =='cloudy-daylight':
            setExposure[5].click()
        state = commands.getoutput('adb shell ' + WhiteBalance_STATE)
        assert state.find(status) != -1, 'set WhiteBalance failed'

    def _setFlashStatus(self,status):
        element = self.driver.find_element_by_id('com.intel.camera22:id/second_menu_indicator_bar')
        self.driver.execute_script("mobile: swipe", {"startX":"360", "startY":"10", "endX":"360", "endY":"200", "element":element.id})
        self.driver.find_element_by_name('Flash settings').click()

        setFlash = self.driver.find_elements_by_id('com.intel.camera22:id/hori_list_button')
        if status =='torch':
            setFlash[1].click()
        elif status =='off':
            setFlash[0].click()
        time.sleep(1)
        state = commands.getoutput('adb shell ' + Flash_STATE)
        assert state.find(status) != -1, 'set flash failed'

    def _recordAndCheck(self):
        
        #Get the number of photo in sdcard
        result = commands.getoutput('adb shell ls ' + DCIM_PATH)
        if result.find(CAMERA_FOLDER) == -1:
            print("no 100ANDRO folder.")
            beforeNo = '0'
        #Get the number of photo in sdcard
        else:
            beforeNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep VID | wc -l')
        time.sleep(2)
        self.driver.find_element_by_name('Shutter button').click()
        time.sleep(30)
        self.driver.find_element_by_name('Shutter button').click()
        time.sleep(2)
        afterNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep VID | wc -l')
        assert int(afterNo) == int(beforeNo) + 1, 'take picture fail!'

    def _captureDuringRecordingAndCheck(self):
        
        #Get the number of photo in sdcard
        result = commands.getoutput('adb shell ls ' + DCIM_PATH)
        if result.find(CAMERA_FOLDER) == -1:
            print("no 100ANDRO folder.")
            beforeNo = '0'
        #Get the number of photo in sdcard
        else:
            beforeNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep VID | wc -l')
        time.sleep(2)
        self.driver.find_element_by_name('Shutter button').click()
        time.sleep(10)

        result2 = commands.getoutput('adb shell ls ' + DCIM_PATH)
        if result.find(CAMERA_FOLDER) == -1:
            print("no 100ANDRO folder.")
            beforeNo2 = '0'
        #Get the number of photo in sdcard
        else:
            beforeNo2 = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep IMG | wc -l')

        self.driver.execute_script("mobile: tap",{ "touchCount": 1, "x": 360, "y": 640}) 
        time.sleep(2)
        afterNo2 = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep IMG | wc -l')
        assert int(afterNo2) == int(beforeNo2) + 1, 'take picture fail!'

        self.driver.find_element_by_name('Shutter button').click()
        time.sleep(2)
        afterNo = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep VID | wc -l')
        assert int(afterNo) == int(beforeNo) + 1, 'take video fail!'

    def testRecordVideoWithFlashOn(self):
        """
        Summary:testRecordVideoWithFlashOn:Record an video in flash on mode
        Steps  : 1.Launch video activity
                 2.Check flash state,set to ON
                 3.Touch shutter button to capture 30s video
                 4.Exit  activity
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setFlashStatus('torch')
        self._recordAndCheck()

    def testRecordVideoWithFlashOff(self):
        """
        Summary:testRecordVideoWithFlashOff:Record an video in flash off mode
        Steps  : 1.Launch video activity
                 2.Check flash state,set to Off
                 3.Touch shutter button to capture 30s video
                 4.Exit  activity
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setFlashStatus('off')
        self._recordAndCheck()

    def testRecordVideoWithGeoLocationOn(self):
        """
        Summary:testRecordVideoWithGeoLocationOn:Record an video in GeoLocation On
        Steps  : 1.Launch video activity
                 2.Check geo-tag ,set to ON
                 3.Touch shutter button to capture 30s video
                 4.Exit  activity
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setGeo('on')
        self._recordAndCheck()
        self._setGeo('off')

    def testRecordVideoWithGeoLocationOff(self):
        """
        Summary:testRecordVideoWithGeoLocationOff:Record an video in GeoLocation Off
        Steps  : 1.Launch video activity
                 2.Check geo-tag ,set to Off
                 3.Touch shutter button to capture 30s video
                 4.Exit  activity
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setGeo('off')
        self._recordAndCheck()

    def testRecordVideoWithVideoSizeFHDHS(self):
        """
        Summary:testRecordVideoWithVideoSizeFHDHS:Record an video in FHDHS video size mode
        Steps  : 1,Launch video activity
                 2.Check video size ,set to FHD
                 3.Touch shutter button to capture 30s video
                 4.Exit  activit
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setVideoSizeStatus('6','1')
        self._recordAndCheck()
        self._setVideoSizeStatus('6','0')

    def testRecordVideoWithVideoSizeFHD(self):
        """
        Summary:testRecordVideoWithVideoSizeFHD:Record an video in FHD video size mode
        Steps  : 1,Launch video activity
                 2.Check video size ,set to FHD
                 3.Touch shutter button to capture 30s video
                 4.Exit  activit
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setVideoSizeStatus('6','0')
        self._recordAndCheck()

    def testRecordVideoWithVideoSizeHDHS(self):
        """
        Summary:testRecordVideoWithVideoSizeHD:Record an video in HDHS video size mode
        Steps  : 1,Launch video activity
                 2.Check video size ,set to HD
                 3.Touch shutter button to capture 30s video
                 4.Exit  activit
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setVideoSizeStatus('5','1')
        self._recordAndCheck()
        self._setVideoSizeStatus('6','0')

    def testRecordVideoWithVideoSizeHD(self):
        """
        Summary:testRecordVideoWithVideoSizeHD:Record an video in HD video size mode
        Steps  : 1,Launch video activity
                 2.Check video size ,set to HD
                 3.Touch shutter button to capture 30s video
                 4.Exit  activit
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setVideoSizeStatus('5','0')
        self._recordAndCheck()
        self._setVideoSizeStatus('6','0')

    def testRecordVideoWithVideoSizeSD(self):
        """
        Summary:testRecordVideoWithVideoSizeSD:Record an video in SD video size mode
        Steps  : 1.Launch video activity
                 2.Check video size ,set to SD
                 3.Touch shutter button to capture 30s video
                 4.Exit  activit
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setVideoSizeStatus('4','0')
        self._recordAndCheck()
        self._setVideoSizeStatus('6','0')

    def testRecordVideoCaptureVideoWithExposureAuto(self):
        """
        Summary:testRecordVideoCaptureVideoWithExposureAuto: Capture video with Exposure auto
        Steps:  1.Launch Video activity
        2.Touch Exposure Setting icon, set Exposure auto
        3.Touch shutter button
        4.Touch shutter button to capture picture
        5.Exit  activity 
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setExposureStatus('0')
        self._recordAndCheck()

    def testRecordVideoCaptureVideoWithExposure1(self):
        """
        Summary:testRecordVideoCaptureVideoWithExposure1: Capture video with Exposure 1
        Steps:  1.Launch Video activity
        2.Touch Exposure Setting icon, set Exposure 1
        3.Touch shutter button 
        4.Touch shutter button to capture picture
        5.Exit  activity  
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setExposureStatus('3')
        self._recordAndCheck()
        self._setExposureStatus('0')

    def testRecordVideoCaptureVideoWithExposure2(self):
        """
        Summary:testRecordVideoCaptureVideoWithExposure2: Capture video with Exposure 2
        Steps:  1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure 2
                3.Touch shutter button 
                4.Touch shutter button to capture picture
                5.Exit  activity   
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setExposureStatus('6')
        self._recordAndCheck()
        self._setExposureStatus('0')

    def testRecordVideoCaptureVideoWithExposureRed1(self):
        """
        Summary:testRecordVideoCaptureVideoWithExposureRed1: Capture video with Exposure -1
        Steps:  1.Launch Video activity
        2.Touch Exposure Setting icon, set Exposure -1
        3.Touch shutter button
        4.Touch shutter button to capture picture
        5.Exit  activity   
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setExposureStatus('-3')
        self._recordAndCheck()
        self._setExposureStatus('0')

    def testRecordVideoCaptureVideoWithExposureRed2(self):
        """
        Summary:testRecordVideoCaptureVideoWithExposureRed2: Capture video with Exposure -2
        Steps:  1.Launch Video activity
        2.Touch Exposure Setting icon, set Exposure -2
        3.Touch shutter button
        4.Touch shutter button to capture picture
        5.Exit  activity    
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setExposureStatus('-6')
        self._recordAndCheck()
        self._setExposureStatus('0')

    def testRecordVideoCaptureVideoWithBalanceAuto(self):
        """
        Summary:testRecordVideoCaptureVideoWithBalanceAuto: Capture video with White Balance Auto
        Steps:  1.Launch video activity
        2.Set White Balance Auto
        3.Touch shutter button to capture 30s video
        4.Exit  activity
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setWBstatus('auto')
        self._recordAndCheck()

    def testRecordVideoCaptureVideoWithBalanceIncandescent(self):
        """
        Summary:testRecordVideoCaptureVideoWithBalanceIncandescent: Capture video with White Balance Incandescent
        Steps:  1.Launch video activity
        2.Set White Balance Incandescent
        3.Touch shutter button to capture 30s video
        4.Exit  activity
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setWBstatus('incandescent')
        self._recordAndCheck()
        self._setWBstatus('auto')

    def testRecordVideoCaptureVideoWithBalanceDaylight(self):
        """
        Summary:testRecordVideoCaptureVideoWithBalanceDaylight: Capture video with White Balance Daylight
        Steps:  1.Launch video activity
        2.Set White Balance Daylight
        3.Touch shutter button to capture 30s video
        4.Exit  activity
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setWBstatus('daylight')
        self._recordAndCheck()
        self._setWBstatus('auto')

    def testRecordVideoCaptureVideoWithBalanceFluorescent(self):
        """
        Summary:testRecordVideoCaptureVideoWithBalanceFluorescent: Capture video with White Balance Fluorescent
        Steps:  1.Launch video activity
        2.Set White Balance Fluorescent
        3.Touch shutter button to capture 30s video
        4.Exit  activity
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setWBstatus('fluorescent')
        self._recordAndCheck()
        self._setWBstatus('auto')

    def testRecordVideoCaptureVideoWithBalanceCloudy(self):
        """
        Summary:testRecordVideoCaptureVideoWithBalanceCloudy: Capture video with White Balance Cloudy
        Steps:  1.Launch video activity
        2.Set White Balance Cloudy
        3.Touch shutter button to capture 30s video
        4.Exit  activity
        """
        self._setCamera('0')
        self._switchToVideo()
        self._setWBstatus('cloudy-daylight')
        self._recordAndCheck()
        self._setWBstatus('auto')

    def testRearFaceRecordVideoWithGeoLocationOn(self):
        """
        Summary:testRearFaceRecordVideoWithGeoLocationOn:Record an video with rear face camera and set GeoLocation On
        Steps  : 1.Launch video activity
                 2.Set to front face camera
                 3.Check geo-tag,set to ON
                 4.Touch shutter button to capture 30s video
                 5.Exit  activity
        """
        self._setCamera('1')
        self._switchToVideo()
        self._setFrontGeo('on')
        self._recordAndCheck()
        self._setFrontGeo('off')

    def testRearFaceRecordVideoWithGeoLocationOff(self):
        """
        Summary:testRearFaceRecordVideoWithGeoLocationOff:Record an video with rear face camera and set GeoLocation Off
        Steps  : 1.Launch video activity
                 2.Set to front face camera
                 3.Check geo-tag,set to ON
                 4.Touch shutter button to capture 30s video
                 5.Exit  activity
        """
        self._setCamera('1')
        self._switchToVideo()
        self._setFrontGeo('off')
        self._recordAndCheck()

    def testRecordVideoWithCaptureImage(self):
        """
        Summary:testRecordVideoWithCaptureImage: Capture image when record video
        Steps:  1.Launch video activity
                2.Touch shutter button to capture 30s video
        3.Touch screen to capture a picture during recording video
        4.Exit  activity   
        """
        self._setCamera('0')
        self._switchToVideo()
        self._captureDuringRecordingAndCheck()

    