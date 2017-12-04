from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
import codecs

def write_txt(text):
    f = codecs.open('C:\\ids\\刑事案件.txt', 'a', 'utf8')
    f.write(str(text))
    f.close()

def openUrl():
    app = QApplication([])
    webview= QWebView()
    loop = QEventLoop()
    webview.loadFinished.connect(loop.quit)
    webview.load(QUrl('http://wenshu.court.gov.cn/list/list?sorttype=1&conditions=searchWord+1+AJLX++案件类型:刑事案件'))
    loop.exec_()
    webview.show()
    getData(app,webview)

def getData(app,webview):
    frame = webview.page().mainFrame()
    ids = frame.findAllElements('.DocIds')
    print(len(ids))
    if(len(ids) == 5):
        for id in ids:
            write_txt(id.get_property('value') + ';')
        frame.findFirstElement(".next").evaluateJavaScript('this.click()')
        getData(app,webview)
        app.exec_()


def main():
    openUrl()

if __name__ == '__main__':
    main()
