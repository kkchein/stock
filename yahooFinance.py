#-*- coding: utf-8 -*-
r"""get data from google finance
"""
import urllib.parse
import urllib.request
import datetime
import time
import csv
import sys
import os
from dataAnalysis import *
#"http://ichart.yahoo.com/table.csv?s=^TWII&a=2&b=2&c=2014"
#"http://finance.yahoo.com/d/quotes.csv?s=^TWII&f=p0ohgc1"
#p0 - last close value
#o - today open
#h - today high
#g - today low
#c1 - change

class YFClass():
    def __init__ (self):
        """constructor

        Args:
        Returns:
        Raises:
        """
        self.stockid="^TWII"
        self.startDateTime=datetime.datetime(1976, 1, 1, 8, 0, 0)
        self.outputFile="hitory.csv"
        self.yahooDateStrType="%Y-%m-%d"
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

        dstr=datetime.datetime.strftime(self.startDateTime, self.yahooDateStrType)
        urlstr="http://ichart.yahoo.com/table.csv?s={0:s}&a={1:d}&b={2:d}&c={3:d}".format(
            self.stockid,
            int(dstr[5:7]) - 1,
            int(dstr[8:10]),
            int(dstr[0:4]))
        #print(urlstr)
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Chrome')]
            content = opener.open(urlstr).read().decode("utf-8").split('\n')
            self.urlData2List(content, olist)
            olist.sort()
            print("ID: {0:s} StartDate: {1:s} DataSize:{2:d}".format(
                self.stockid, datetime.datetime.strftime(self.startDateTime, DataAnalysis.dataStrType), len(olist)))
            #for item in olist:
            #    print(item)
        except urllib.error.HTTPError:
            print("No data")
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
            ltemp=idata[icount].split(',')
            try:
                dt = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ltemp[0], self.yahooDateStrType)))
            except ValueError:
                continue
            try:
                openValue=float(ltemp[1].replace(",",""))
            except ValueError:
                openValue=0.0
            try:
                highValue=float(ltemp[2].replace(",",""))
            except ValueError:
                highValue=0.0
            try:
                lowValue=float(ltemp[3].replace(",",""))
            except ValueError:
                lowValue=0.0
            try:
                closeValue=float(ltemp[4].replace(",",""))
            except ValueError:
                closeValue=0.0
            try:
                volValue=float(ltemp[5].replace(",",""))
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
if __name__ == "__main__":
    symbollist=[[ "^STI",'Idx_STI'],     #^STI - 新加坡海峽時報指數
                ["^JKSE",'Idx_JKSE']]    #^JKSE - 印尼雅加達綜合指數 Jakarta Composite Index
    yfc=YFClass()
    #array=[]
    #yfc.getHistoryData(array)
    #yfc.list2csv("temp.csv", array)
    #yfc.csv2list("temp.csv", array)
    da=DataAnalysis()
    if os.path.exists("./csv")==True:
        csvdir="./csv/"
    else:
        csvdir="./"
    for icount in range(len(symbollist)):
        #print('{0:s} : {1:s}'.format(symbollist[icount][0],symbollist[icount][1]))
        array=[]
        filename=csvdir+symbollist[icount][1]
        sys.stdout.flush()
        da.csv2list(filename+".csv", array)
        lastlen=len(array)
        yfc.getLatest2List(isymbol=symbollist[icount][0], ilist=array)
        newlen=len(array)
        da.list2csv(filename+".csv", array)
        print("New add {0:d} data".format(newlen-lastlen))
        print(filename+"_2.csv processing...")
        rarray=[]
        da.listReduce(array, rarray)
        da.list2csv(filename+"_2.csv", rarray)

