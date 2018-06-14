#coding=utf-8
from appium import webdriver


import os

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def get_desired_capabilities(app):
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '5.1',
        'deviceName': 'Android Emulator',
        'app': PATH('../opt/' + app),
        'newCommandTimeout': 240
    }

    return desired_caps
desired_caps = get_desired_capabilities(u'aweme_aweGW_v1.8.3_61b8304.apk')
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.quit()
