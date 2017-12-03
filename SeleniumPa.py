# -*- coding: utf8 -*-
from selenium import webdriver
import urllib
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import json
import codecs

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
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'dataItem')))
    ids = driver.find_elements_by_class_name("DocIds")
    if(driver.find_elements_by_class_name('next')[0].value_of_css_property('color') != 'rgba(153, 153, 153, 1)'):
        for id in ids:
            write_txt(id.get_property('value') + ';')
        sleep(10)
        # driver.execute_script("$('.next').trigger('click')")
        # getData(driver)
    else:
        date = "2017-12"
        openUrl(getParams(date))

def getParams(date):
    params = '裁判日期:2017-12-01 TO 2017-12-31'
    return params

def main():
    params = getParams("2017-12")
    openUrl(params)

if __name__ == '__main__':
    main()
