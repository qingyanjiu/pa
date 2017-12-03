# -*- coding: utf8 -*-
from selenium import webdriver
import urllib
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from time import sleep
import pytesseract
from PIL import Image
import codecs

searchDate = '2010-09-29'

def write_txt(text):
    f = codecs.open('C:\\ids\\刑事案件.txt', 'a', 'utf8')
    f.write(str(text))
    f.close()

def openUrl(params):
    driver = webdriver.Chrome()
    driver.get('http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6')
    driver.execute_script("$('#gover_search_key').val('"+params+"')")
    driver.execute_script("$('#btnSearch').trigger('click')")
    sleep(5)
    driver.execute_script("$(\"li[id*='_input_20']\").trigger('click')")
    sleep(5)
    getData(driver)

def getData(driver):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'dataItem')))
        ids = driver.find_elements_by_class_name("DocIds")
        if(len(ids) > 0):
            for id in ids:
                write_txt(id.get_property('value') + ';\n')
            driver.execute_script("$('.next').trigger('click')")
            sleep(5)
            if(driver.find_elements_by_class_name('next')[0].value_of_css_property('color') != 'rgba(153, 153, 153, 1)'):
                getData(driver)
            else:
                driver.close()
                updateSearchDate(searchDate)
                openUrl(getParams(searchDate))
    except exceptions.TimeoutException:
        if(driver.current_url == 'http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html'):
            print(Image.PILLOW_VERSION)
            url = "http://wenshu.court.gov.cn/User/ValidateCode"
            f = open('C:\\ids\\vcode.jpeg', 'wb')
            req = urllib.request.urlopen(url)
            buf = req.read()
            f.write(buf)
            sleep(5)
            image = Image.open(r'C:\ids\vcode.jpeg')
            vcode = pytesseract.image_to_string(image)
            print(vcode)
            driver.execute_script("$('#txtValidateCode').val("+vcode+")")
            driver.execute_script("$('.btn_validatecode').trigger('click')")
        else:
            driver.close()
            updateSearchDate(searchDate)
            openUrl(getParams(searchDate))



def getParams(date):
    params = '裁判日期:'+date+' TO '+date
    print(params)
    return params

def updateSearchDate(date):
    year = date.split('-')[0]
    month = date.split('-')[1]
    day = date.split('-')[2]
    if(day != '31'):
        day = int(day) + 1
        if(day < 10):
            day = '0' + str(day)
    else:
        day = '01'
        if(month != '12'):
            month = int(month) + 1
            if(month < 10):
                month = '0' + str(month)
        else:
            month = '01'
            year = int(year) + 1

    global searchDate
    searchDate = str(year) + '-' + str(month) + '-' + str(day)

def main():
    params = getParams(searchDate)
    openUrl(params)

if __name__ == '__main__':
    main()
