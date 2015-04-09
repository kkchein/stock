#-*- coding: utf-8 -*-
r"""get data from google finance
"""
import urllib.parse
import urllib.request
import re
import datetime
import csv
import time
import sys
from dataAnalysis import *


#"https://www.google.com/finance/historical?q=TPE:TAIEX&startdate=1/1/1985&start=0&num=30"

class GFClass():
    #gfDate=0
    #gfStart=1
    #gfHigh=2
    #gfLow=3
    #gfEnd=4
    #gfVol=5
    def __init__ (self):
        """constructor

        Args:
        Returns:
        Raises:
        """
        self.stockid="TPE:TAIEX"
        self.startDateTime=datetime.datetime(1976, 1, 1, 8, 0, 0)
        self.displayNum=30
        self.outputFile="hitory.csv"
        self.googleDateStrType="%b %d, %Y"
        self.googleUrlDateStrType="%m/%d/%Y"
    def getHistoryData (self, olist, isymbol=None, isdt=None):
        """get history data from google finance

        Args:
            olist- output data list
            isymbol- stock symbol
            isdt- the date start to get data
        Returns:
        Raises:
            False- no data
            True- data ready
        """
        if isdt!=None:
            self.startDateTime=isdt
        if isymbol!=None:
            self.stockid=isymbol

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Chrome')]
        urlstr="https://www.google.com/finance/historical?q={0:s}&startdate={1:s}&start=0&num={2:d}".format(
            self.stockid, datetime.datetime.strftime(self.startDateTime, self.googleUrlDateStrType), self.displayNum)
        content = opener.open(urlstr).read()
        totalSizeStr=r'google\.finance\.applyPagination\(\s+\d+,\s+\d+,\s+(\d+),\s+'
        reg_row_size =  re.compile( totalSizeStr )
        match_r_sz = reg_row_size.search( content.decode("utf-8") )
        if (match_r_sz is None):
            print("There is no data.")
            return False
        row_size = int (match_r_sz.groups()[0])
        print("ID: {0:s} StartDate: {1:s} DataSize:{2:d}".format(
            self.stockid, datetime.datetime.strftime(self.startDateTime, DataAnalysis.dataStrType), row_size))
        if row_size%self.displayNum!=0:
            pageSize=int(row_size/self.displayNum)+1
        else:
            pageSize=int(row_size/self.displayNum)
        #print("page "+ str(pageSize))
        ##Open, high, low, close, volume
        dataStr = r'<td class="lm">(.+)' +  \
            '\s<td class="rgt">(.+)' + \
            '\s<td class="rgt">(.+)' + \
            '\s<td class="rgt">(.+)' + \
            '\s<td class="rgt">(.+)' + \
            '\s<td class="rgt rm">(.+)'
        reg_price = re.compile( dataStr )
        for icount in range(pageSize):
            urlstr="https://www.google.com/finance/historical?q={0:s}&startdate={1:s}&start={2:d}&num={3:d}".format(
                self.stockid, datetime.datetime.strftime(self.startDateTime, "%m/%d/%Y"), icount*self.displayNum, self.displayNum)
            #print(urlstr)
            content = opener.open(urlstr).read()
            stock_data = reg_price.findall( content.decode("utf-8") )
            self.urlData2List(stock_data, olist)
        olist.sort()
        return True
    def urlData2List (self, idata, odata):
        """convert google data to data

        Args:
            idata- google input data
            odata- output data
        Returns:
        Raises:
        """
        for icount in range(len(idata)):
            dt = datetime.datetime.fromtimestamp(time.mktime(time.strptime(idata[icount][0], self.googleDateStrType)))
            try:
                openValue=float(idata[icount][1].replace(",",""))
            except ValueError:
                openValue=0.0
            try:
                highValue=float(idata[icount][2].replace(",",""))
            except ValueError:
                highValue=0.0
            try:
                lowValue=float(idata[icount][3].replace(",",""))
            except ValueError:
                lowValue=0.0
            try:
                closeValue=float(idata[icount][4].replace(",",""))
            except ValueError:
                closeValue=0.0
            try:
                volValue=float(idata[icount][5].replace(",",""))
            except ValueError:
                volValue=0.0
            odata.append([dt, openValue, highValue, lowValue, closeValue, volValue])
    def getLatest2List (self, ilist, isymbol):
        """according list from csv, get lastest data from google finance

        Args:
            ilist- google input data
            isymbol- stock symbol
        Returns:
        Raises:
        """
        if len(ilist)>0:
            lastdt=ilist[len(ilist)-1][0]+datetime.timedelta(days=1)
        else:
            lastdt=datetime.datetime(1985, 1, 1, 0, 0, 0)
        self.getHistoryData(ilist, isymbol, lastdt)
def symbol2Filename (isymbol):
    return symbolstr.replace(":","")
if __name__ == "__main__":
    symbollist=["TPE:2330",             #台積電
                "TPE:2382",             #廣達
                "TPE:2395",             #研華
                "TPE:0050",             #台灣50
                "TPE:0061",             #寶滬深
                "TPE:2002",             #中鋼
                "TPE:TAIEX",            #台灣加權指數
                "INDEXNIKKEI:NI225",    #日經
                "INDEXBOM:SENSEX"]      #孟買敏感30指數、BSE SENSEX
    gfc=GFClass()
    da=DataAnalysis()
    for symbolstr in symbollist:
        array=[]
        filename=symbol2Filename(symbolstr)
        print(filename+".csv processing...")
        sys.stdout.flush()
        da.csv2list(filename+".csv", array)
        lastlen=len(array)
        gfc.getLatest2List(isymbol=symbolstr, ilist=array)
        newlen=len(array)
        da.list2csv(filename+".csv", array)
        print("New add {0:d} data".format(newlen-lastlen))
        #for icount in range(len(array)):
        #    print(array[icount])
        print(filename+"_2.csv processing...")
        rarray=[]
        da.listReduce(array, rarray)
        da.list2csv(filename+"_2.csv", rarray)

    
