import commands
import time
from selenium import webdriver

CAMERA_ID = 'cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'


def launchApp(self, package, activity):
    desired_caps = {
        'device': 'android',
        'browserName': '',
        'version': '4.4',
        'app-package': package,
        'app-activity': activity
        }
    self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

def tearDown(self):
    self.driver.quit()

def setCameraMode(self, status):
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