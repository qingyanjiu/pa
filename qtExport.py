from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
import urllib
from time import sleep
import json


def main():
    app = QApplication([])
    webview= QWebView()
    loop = QEventLoop()
    webview.loadFinished.connect(loop.quit)
    webview.load(QUrl('http://wenshu.court.gov.cn/list/list?sorttype=1&conditions=searchWord+1+AJLX++案件类型:刑事案件'))
    loop.exec_()
    webview.show()
    frame = webview.page().mainFrame()
    frame.findAllElements('#DocIds')

if __name__ == '__main__':
    main()
