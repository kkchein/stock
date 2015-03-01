r"""get data from google finance
"""
import urllib.parse
import urllib.request
import re
import datetime
import csv
import time
import sys

#"https://www.google.com/finance/historical?q=TPE:TAIEX&startdate=1/1/1985&start=0&num=30"

class GFClass():
    gfDate=0
    gfStart=1
    gfHigh=2
    gfLow=3
    gfEnd=4
    gfVol=5
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
        self.dataStrType="%Y/%m/%d"
    def getHistoryData (self, olist, isymbol=None, isdt=None):
        """get history data from google finance

        Args:
            olist- output data list
            isymbol- stock symbol
            isdt- the date start to get data
            ofile- output file (csv format), if None, print
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
            self.stockid, datetime.datetime.strftime(self.startDateTime, self.dataStrType), row_size))
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
    def csv2list (self, icsvfilename, odata):
        """read csv data into memory

        Args:
            icsvfilename- csv file name
            odata- output data
        Returns:
        Raises:
        """
        try:
            csvFileR=open(icsvfilename, "r")
        except FileNotFoundError:
            return
        csvContent=csv.reader(csvFileR, delimiter=',')
        for i in csvContent:
            dt = datetime.datetime.fromtimestamp(time.mktime(time.strptime(i[0], self.dataStrType)))
            try:
                openValue=float(i[1].replace(",",""))
            except ValueError:
                openValue=0.0
            try:
                highValue=float(i[2].replace(",",""))
            except ValueError:
                highValue=0.0
            try:
                lowValue=float(i[3].replace(",",""))
            except ValueError:
                lowValue=0.0
            try:
                closeValue=float(i[4].replace(",",""))
            except ValueError:
                closeValue=0.0
            try:
                volValue=float(i[5].replace(",",""))
            except ValueError:
                volValue=0.0
            odata.append([dt, openValue, highValue, lowValue, closeValue, volValue])
        odata.sort()
        csvFileR.close()
    def list2csv (self, ocsvfilename, idata):
        """save list data to csv

        Args:
            ocsvfilename- csv file name
            idata- input data
        Returns:
        Raises:
        """
        csvFileW=open(ocsvfilename, "w", newline='')
        csvContent=csv.writer(csvFileW, delimiter=',')
        for icount in range(len(idata)):
            csvContent.writerow([datetime.datetime.strftime(idata[icount][0], self.dataStrType),
                             str(idata[icount][1]),
                             str(idata[icount][2]),
                             str(idata[icount][3]),
                             str(idata[icount][4]),
                             str(idata[icount][5])])
        csvFileW.close
def symbol2Filename (isymbol):
    return symbolstr.replace(":","")+".csv"
if __name__ == "__main__":
    symbollist=["TPE:2330",
                "TPE:2382",
                "TPE:2395",
                "TPE:0050",
                "TPE:TAIEX"]
    gfc=GFClass()
    #sdatetime=datetime.datetime(1985, 1, 1, 0, 0, 0)
    #gfc.getHistoryData(olist=array, isymbol=symbolstr, isdt=sdatetime)
    #gfc.list2csv(filename, array)
    for symbolstr in symbollist:
        array=[]
        filename=symbol2Filename(symbolstr)
        print(filename+" processing...")
        sys.stdout.flush()
        gfc.csv2list(symbolstr.replace(":","")+".csv", array)
        lastlen=len(array)
        gfc.getLatest2List(isymbol=symbolstr, ilist=array)
        newlen=len(array)
        gfc.list2csv(filename, array)
        print("New add {0:d} data".format(newlen-lastlen))
        #for icount in range(len(array)):
        #    print(array[icount])
    
