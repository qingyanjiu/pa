# -*- coding: utf8 -*-
from selenium import webdriver
from urllib import request
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from time import sleep
import pytesseract
from PIL import Image
import codecs



def main():
    driver = webdriver.Chrome()
    driver.get('http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html')
    driver.save_screenshot(r'ValidateCode.png')
    sleep(3)
    image = Image.open(r'ValidateCode.png')
    # box = (506,141,564,164)
    box = (594,142,652,169)
    region = image.crop(box)
    region.save(r'ValidateCode.png')
    vcode = pytesseract.image_to_string(region)
    print('validationCode:%s' % vcode)
    driver.execute_script("$('#txtValidateCode').val('"+vcode+"')")
    driver.execute_script("$('#btnLogin').trigger('click')")
    sleep(5)

if __name__ == '__main__':
    main()
