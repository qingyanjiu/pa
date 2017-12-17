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
import time

searchDate = '2012-04-20'
currentYear = '2012';

def write_txt(text):
    f = codecs.open('C:\\ids\\刑事案件test-'+currentYear+'.txt', 'a', 'utf8')
    # f = codecs.open(r'/Users/user/Documents/刑事案件test-'+currentYear+'.txt', 'a', 'utf8')
    f.write(str(text))
    f.close()

def openUrl(params):
    print('open new page,params : ' + params + ' [' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ']')
    driver = webdriver.Chrome()
    try:
        driver.get('http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6')
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'dataItem')))
        driver.execute_script("$('#gover_search_key').val('"+params+"')")
        driver.execute_script("$('#btnSearch').trigger('click')")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'dataItem')))
        sleep(10)
        driver.execute_script("$(\"li[id*='_input_20']\").trigger('click')")
        #判断每页显示20条是否已经选中
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"li[id*='_input_20'][class='selected']")))
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'dataItem')))
        sleep(10)
        getData(driver)
    except exceptions.UnexpectedAlertPresentException:
            print('website alerts || maybe over 400 records of today, skip to next day')
            skipToNextDay(driver)
    except exceptions.TimeoutException:
        if(driver.current_url == 'http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html'
            or driver.current_url == 'http://wenshu.court.gov.cn/waf_verify.htm'):
            dealWithValidationImage(driver)
        else:
            print('openUrl exception, maybe weak net work,retry today')
            driver.close()
            sleep(10)
            openUrl(params)

def getData(driver):
    # if(driver.current_url == 'http://wenshu.court.gov.cn/waf_verify.htm'):
    if(driver.current_url == 'http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html'
       or driver.current_url == 'http://wenshu.court.gov.cn/waf_verify.htm'):
        dealWithValidationImage(driver)
    else:
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'dataItem')))
            ids = driver.find_elements_by_class_name("DocIds")
            if(len(ids) > 0):
                for id in ids:
                    write_txt(id.get_property('value') + ';\n')
                driver.execute_script("$('.next').trigger('click')")
                sleep(5)
                if(driver.current_url == 'http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html'
                   or driver.current_url == 'http://wenshu.court.gov.cn/waf_verify.htm'):
                    dealWithValidationImage(driver)
                else:
                    if(driver.find_elements_by_class_name('next')[0].value_of_css_property('color') != 'rgba(153, 153, 153, 1)'):
                        getData(driver)
                    elif(driver.find_elements_by_class_name('next')[0].value_of_css_property('color') == 'rgba(153, 153, 153, 1)'):
                        driver.close()
                        updateSearchDate(searchDate)
                        openUrl(getParams(searchDate))
                    else:
                        print('maybe exists some unknown issue, skip to next day')
                        skipToNextDay(driver)
        except exceptions.UnexpectedAlertPresentException:
            print('maybe over 400 records of today, skip to next day')
            skipToNextDay(driver)
        except exceptions.TimeoutException:
            if(driver.current_url == 'http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html'
               or driver.current_url == 'http://wenshu.court.gov.cn/waf_verify.htm'):
                dealWithValidationImage(driver)
            else:
                driver.close()
                sleep(10)
                openUrl(getParams(searchDate))



def getParams(date):
    params = '裁判日期:'+date+' TO '+date
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
            global currentYear
            currentYear = year

    global searchDate
    searchDate = str(year) + '-' + str(month) + '-' + str(day)

def dealWithValidationImage(driver):
    print('validationImage')
    driver.save_screenshot(r'ValidateCode.png')
    sleep(3)
    image = Image.open(r'ValidateCode.png')
    box = (506,141,564,164)
    # box = (594,142,652,169)
    region = image.crop(box)
    region.save(r'ValidateCode.png')
    vcode = pytesseract.image_to_string(region)
    print('validationCode:%s' % vcode)
    driver.execute_script("$('#txtValidateCode').val('"+vcode+"')")
    driver.execute_script("$('#btnLogin').trigger('click')")
    sleep(10)
    driver.close()
    params = getParams(searchDate)
    openUrl(params)

def skipToNextDay(driver):
    driver.close()
    sleep(10)
    updateSearchDate(searchDate)
    openUrl(getParams(searchDate))

def main():
    params = getParams(searchDate)
    openUrl(params)

if __name__ == '__main__':
    main()
