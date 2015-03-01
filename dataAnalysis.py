"""process data
"""
import sys
import collections
from PyQt4 import QtCore

from googleFinance import *
class DrawData:
    dtypeLine=0
    def __init__ (self):
        self.clear()
    def clear (self):
        self.caption=""
        self.data=[]
        self.color=QtCore.Qt.black
        self.drawType=DrawData.dtypeLine
    def drawDataStart (self, istart):
        self.startPos=istart
        if istart>=len(self.data):
            return None
        return self.data[len(self.data)-istart-1]
class DataAnalysis():
    """calss to analysis data
    """
    boundaryMax=0
    boundaryMin=1
    def __init__ (self):
        """constructor

        Args:
        Returns:
        Raises:
        """
        self.gfc=GFClass()
        self.sourceData=[]
        self.drawDataArray=[]
        self.startPos=0
    def clear (self):
        del self.sourceData
        self.sourceData=[]
        del self.drawDataArray
        self.drawDataArray=[]
        self.startPos=0
    def loadFromCSV (self, ifname):
        """load data from csv file

        Args:
            ifname- csv file name
        Returns:
        Raises:
        """
        self.sourceData=[]  #clear data
        self.gfc.csv2list(ifname, self.sourceData)
        self.drawDataArray=[]
        #self.drawDataArray.append(self.calMA(5))
        #for icount in range(len(self.drawDataArray[0].data)):
        #    print(self.drawDataArray[0].data[icount])
    def getValueBoundaryAtPos (self, ipos):
        result=[0.0,10000000000000000000.0]
        if "sourceData" in self.__dict__:
            if len(self.sourceData)==0:
                return None
            for icount in range(GFClass.gfStart, GFClass.gfEnd+1):
                if result[DataAnalysis.boundaryMax]<self.sourceData[ipos][icount]:
                    result[DataAnalysis.boundaryMax]=self.sourceData[ipos][icount]
                if result[DataAnalysis.boundaryMin]>self.sourceData[ipos][icount]:
                    result[DataAnalysis.boundaryMin]=self.sourceData[ipos][icount]
        if len(self.drawDataArray)>0:
            for icount in range(len(self.drawDataArray)):
                if result[DataAnalysis.boundaryMax]<self.drawDataArray[icount].data[ipos]:
                    result[DataAnalysis.boundaryMax]=self.drawDataArray[icount].data[ipos]
                if result[DataAnalysis.boundaryMin]>self.drawDataArray[icount].data[ipos] and self.drawDataArray[icount].data[ipos]!=0:
                    result[DataAnalysis.boundaryMin]=self.drawDataArray[icount].data[ipos]
        return result
    def getValueBoundaryForLastN (self, inum, startNum=0):
        """get highest and lowest value in number data

        Args:
            inum- number
        Returns:
        Raises:
        """
        if inum>len(self.sourceData)-startNum:
            rangeNum=len(self.sourceData)-startNum
        else:
            rangeNum=inum
        result=[0.0, 0.0]
        for icount in range(rangeNum):
            rtemp=self.getValueBoundaryAtPos(len(self.sourceData)-icount-1+startNum)
            if icount==0:
                if rtemp==None:
                    return None
                result[DataAnalysis.boundaryMax]=rtemp[DataAnalysis.boundaryMax]
                result[DataAnalysis.boundaryMin]=rtemp[DataAnalysis.boundaryMin]
            else:
                if result[DataAnalysis.boundaryMax]<rtemp[DataAnalysis.boundaryMax]:
                    result[DataAnalysis.boundaryMax]=rtemp[DataAnalysis.boundaryMax]
                if result[DataAnalysis.boundaryMin]>rtemp[DataAnalysis.boundaryMin]:
                    result[DataAnalysis.boundaryMin]=rtemp[DataAnalysis.boundaryMin]
        return result
        #result=[0.0,0.0]
        #if len(self.sourceData)==0:
        #    return None
        #if inum>len(self.sourceData)-startNum:
        #    rangeNum=len(self.sourceData)-startNum
        #else:
        #    rangeNum=inum
        #
        #for icount in range(rangeNum):
        #    dtemp=self.sourceData[len(self.sourceData)-icount-1+startNum]
        #    if icount==0:
        #        result=[dtemp[1], dtemp[1]]
        #        for jcount in range(2, 5):
        #            if result[0]<dtemp[jcount]:
        #                result[0]=dtemp[jcount]
        #            if result[1]>dtemp[jcount]:
        #                result[1]=dtemp[jcount]
        #    else:
        #        if icount>=len(self.sourceData):
        #            break
        #        for jcount in range(1, 5):
        #            if result[0]<dtemp[jcount]:
        #                result[0]=dtemp[jcount]
        #            if result[1]>dtemp[jcount]:
        #                result[1]=dtemp[jcount]
        #return result
    def souceDataStart (self, istart):
        """get data

        Args:
            istart- data start
        Returns:
        Raises:
        """
        self.startPos=istart
        if istart>=len(self.sourceData):
            return None
        return self.sourceData[len(self.sourceData)-istart-1]
    def addToDrawArray (self, idrawdata):
        if type(idrawdata) is DrawData:
            self.drawDataArray.append(idrawdata)
    def calMA (self, period, capStr="", icolor=QtCore.Qt.black):
        if len(self.sourceData)==0:
            return
        result=DrawData()
        result.color=icolor
        if capStr=="":
            result.caption="MA{0:d}".format(period)
        else:
            result.caption=capStr
        vtemp=collections.deque([]) #queue
        for icount in range(len(self.sourceData)):
            vtemp.append(self.sourceData[icount][GFClass.gfEnd])
            ftemp=0.0;
            if icount>=period-1:
                for jcount in range(period):
                    ftemp=ftemp+vtemp[jcount]
                ftemp=ftemp/period
                vtemp.popleft()
            result.data.append(ftemp)
        return result

