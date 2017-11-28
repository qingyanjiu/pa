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

def openUrl():
    driver = webdriver.Chrome()
    driver.get('http://wenshu.court.gov.cn/list/list?sorttype=1&conditions=searchWord+1+AJLX++案件类型:刑事案件')
    getData(driver)

def getData(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'dataItem')))
    ids = driver.find_elements_by_class_name("DocIds")
    if(len(ids) == 5):
        for id in ids:
            write_txt(id.get_property('value') + ';')
        sleep(10)
        driver.execute_script("$('.next').trigger('click')")
        getData(driver)

def main():
    openUrl()

if __name__ == '__main__':
    main()
