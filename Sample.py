from selenium import webdriver
import urllib
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import json


def main():
    driver = webdriver.Chrome()
    driver.get('http://wenshu.court.gov.cn/list/list?sorttype=1&conditions=searchWord+1+AJLX++案件类型:刑事案件')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'dataItem')))
    # firstdocvalue= driver.find_elements_by_class_name('DocIds')[0].get_property('value')
    driver.execute_script("$('.next').trigger('click')")
    # driver.get('http://wenshu.court.gov.cn/')
    # driver.execute_script("$('#gover_search_key').text('2017-11-25')")
    # driver.execute_script("$('.head_search_btn').trigger('click')")
    sleep(5)
    # driver.execute_script("$('#ckall').trigger('click')")
    # driver.execute_script("$('.list-operate').eq(1).trigger('click')")
    ids = driver.find_elements_by_class_name("DocIds");
    idList = [id.get_property('value').split('|')[0] for id in ids]
    # driver.close()
    print(idList)
    resplist = []
    caselist = []
    for id in idList:
        resp = urllib.request.urlopen("http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + id)
        driver.implicitly_wait(20)
        # print(resp.read().decode("utf-8"))
        resplist.append(resp.read().decode("utf-8"))
    for response in resplist:
        temp = response.split('jsonHtmlData = ')[1]
        temp = temp.split('var jsonData')[0]
        result = temp.replace('\\','')
        # print(result)
        # print(result.split('Title":"')[1].split('","PubDate')[0])
        # print(result.split('PubDate":"')[1].split('","Html')[0])
        # print(result.split('Html":"')[1].split('"}";')[0])
        case = {}
        case["title"] = result.split('Title":"')[1].split('","PubDate')[0]
        case["pubDate"] = result.split('PubDate":"')[1].split('","Html')[0]
        case["content"] = result.split('Html":"')[1].split('"}";')[0]
        caselist.append(case)

    print(json.dumps(caselist, ensure_ascii=False))


if __name__ == '__main__':
    main()
