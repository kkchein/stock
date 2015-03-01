#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------
#   抓上市與上櫃各股相關資料
#   Version : 1.1
#   Author : Amin white
#   Release Date : 2012-01-01
#   Python version : 2.7.2
#---------------------------------------------
import csv, time, codecs, urllib, os
#from sgmllib import SGMLParser
import html.parser as SGMLParser
 
def main():   
    stockkind = ["sii", "otc"]
    stocktype = [u"上市", u"上櫃"]
    stocknoclass = ({ "01": u"水泥工業",
                      "02": u"食品工業",
                      "03": u"塑膠工業",
                      "04": u"紡織纖維",
                      "05": u"電機機械",
                      "06": u"電器電纜",
                      "07": u"化學生技醫療",
                      "08": u"玻璃陶瓷",
                      "09": u"造紙工業",
                      "10": u"鋼鐵工業",
                      "11": u"橡膠工業",
                      "12": u"汽車工業",
                      "13": u"電子工業",
                      "14": u"建材營造",
                      "15": u"航運業",
                      "16": u"觀光事業",
                      "17": u"金融保險業",
                      "18": u"貿易百貨",
                      "19": u"綜合企業",
                      "20": u"其他",
                      "21": u"化學工業",
                      "22": u"生技醫療業",
                      "23": u"油電燃氣業",
                      "24": u"半導體業",
                      "25": u"電腦及週邊設備業",
                      "26": u"光電業",
                      "27": u"通信網路業",
                      "28": u"電子零組件業",
                      "29": u"電子通路業",
                      "30": u"資訊服務業",
                      "31": u"其他電子業",
                      "91": u"存託憑證"})
     
    #指定儲存的路徑,可自行變更儲存路徑
    workdir = '.\\'
    if not os.path.isdir(workdir):
        os.makedirs(workdir)
    savefile = workdir + 'stockinfo.csv'
    #開始寫入檔案準備
    writefile = open(savefile, 'wb')
    #指定檔案以UTF8儲存
    writefile.write(codecs.BOM_UTF8)
    #指定CSV檔分隔的方式
    writer = csv.writer(writefile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    #寫入欄位說明
    writer.writerow([u'股票代號'.encode('utf8'), u'股票種類'.encode('utf8'), u'產業分類編號'.encode('utf8'), \
                     u'產業分類名稱'.encode('utf8'), u'公司名稱'.encode('utf8'), u'公司資本額'.encode('utf8'),\
                     u'公司地址'.encode('utf8'), u'公司電話'.encode('utf8'), u'公司開幕日'.encode('utf8'), \
                     u'公司上市上櫃日'.encode('utf8')])
     
    for i in range(0, len(stockkind)):
        kindname = stockkind[i]
        cstocktype= stocktype[i]       
        count = 0
        for classno in sorted(stocknoclass.items(), key=lambda stocknoclass:stocknoclass[0], reverse = False):
            #個股票網址
            url = "http://mops.twse.com.tw/mops/web/ajax_t51sb01?step=1&firstin=1&TYPEK=%s&code=%s" %(kindname, classno[0])
            #解析網頁開始
            webcode = urllib.urlopen(url)
            if webcode.code == 200:
                stock = ParseWebData()
                stock.parse(webcode.read())
                webcode.close()
                stock.close()
                if stock.webexist:
                    print(kindname + " " + classno[0] + " " + classno[1] + " web parser OK......")
                else:
                    print(kindname + " " + classno[0] + " " + classno[1] + " not exist......")
                    continue;
                for j in range(0, len(stock.stockid)):
                    #處理中文編碼
                    stockid = unicode(stock.stockid[j],"utf-8")
                    companyname = unicode(stock.stockcompanyname[j],"utf-8")
                    companyaddress = unicode(stock.stockcompanyaddress[j],"utf-8")
                    companytel = unicode(stock.stockcompanytel[j],"utf-8")
                    companyopendate = unicode(stock.stockcompanyopendate[j],"utf-8")
                    companylistingdate = unicode(stock.stockcompanylistingdate[j],"utf-8")
                    companycapital = unicode(stock.stockcompanycapital[j],"utf-8")
                    #寫入股票資料
                    writer.writerow([ '%s' %stockid.encode('utf8'), '%s' %cstocktype.encode('utf8'), '%s' %classno[0].encode('utf8'),\
                                      '%s' %classno[1].encode('utf8'), '%s' %companyname.encode('utf8'), '%s' %companycapital.encode('utf8'),\
                                      '%s' %companyaddress.encode('utf8'), '%s' %companytel.encode('utf8'), '%s' %companylistingdate.encode('utf8'), \
                                      '%s' %companyopendate.encode('utf8')])
                count += 1
                print(kindname + " " + classno[0] + " " + classno[1] + " data write to csv OK......\n")
            if(count%6) == 0:
                time.sleep(10)
    #關閉檔案           
    writefile.close()
class ParseWebData(SGMLParser.HTMLParser):
    #初始化class等同constructor
    def __init__(self):
        SGMLParser.HTMLParser.__init__(self)
    #初始化變數數值
    def reset(self):
        SGMLParser.HTMLParser.reset(self)
        self.webexist = False
        self.nowrapflag = False
        self.styleflag = False
        self.nowrapcount = 0
        self.stylecount = 0
        self.stockcompanyname = []
        self.stockcompanyaddress = []
        self.stockcompanytel = []
        self.stockcompanyopendate = []
        self.stockcompanylistingdate = []
        self.stockcompanycapital = []
        self.stockid = []
         
    def parse(self,data):
        self.feed(data)
        self.close()
    def start_table(self, attrs):
        if attrs[0][0] == 'class' and attrs[0][1] == 'noBorder':
            self.webexist = True                 
    def start_td(self, attrs):
        for name, value in attrs:
            if len(attrs) == 1:
                if name == 'nowrap':
                    self.nowrapflag = True
                    self.nowrapcount += 1                       
            elif len(attrs) == 2:
                #print len(attrs)
                if name == 'style':
                    if value == 'text-align:left !important;' or value == 'text-align:right !important;':
                        self.styleflag = True
                        self.stylecount += 1                  
    def handle_data(self, text):
        if self.nowrapflag :
            if self.nowrapcount == 1:
                self.stockid.append(text)
                #print "stockid : " + text
                self.nowrapflag = False
            elif self.nowrapcount == 7:
                self.stockcompanyopendate.append(text)
                #print "opendate : " + text
                self.nowrapflag = False
            elif self.nowrapcount == 8:
                self.stockcompanylistingdate.append(text)
                #print "listingdate : " + text
                self.nowrapflag = False
            elif self.nowrapcount == 10:
                self.nowrapcount = 0
                self.nowrapflag = False
             
        if self.styleflag :
            if self.stylecount == 1:
                self.stockcompanyname.append(text)
                #print "name : " + text
                self.styleflag = False
            elif self.stylecount == 2:
                self.stockcompanyaddress.append(text)
                #print "address : " + text
                self.styleflag = False
            elif self.stylecount == 4:
                self.stockcompanytel.append(text)
                #print "tel : " + text
                self.styleflag = False
            elif self.stylecount == 5:
                self.stockcompanycapital.append(text.strip().replace(",", ""))
                #print "capital : " + text.strip().replace(",", "")
                self.styleflag = False
            elif self.stylecount == 14:
                self.stylecount = 0
                self.styleflag = False   
if __name__ == "__main__":
    main()
