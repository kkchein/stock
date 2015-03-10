"""process data
"""
import sys
import collections
import math
from PyQt4 import QtCore

from googleFinance import *
class DrawData:
    """draw data object
    """
    dtypeLine=0
    def __init__ (self):
        """constructor

        Args:
        Returns:
        Raises:
        """
        self.clear()
    def clear (self):
        """constructor

        Args:
        Returns:
        Raises:
        """
        self.caption=""
        self.data=[]
        self.color=QtCore.Qt.black
        self.drawType=DrawData.dtypeLine
        self.penW=0
        self.enable=True
    def drawDataStart (self, istart):
        self.startPos=istart
        postemp=(len(self.data)-istart-1)
        if postemp>=len(self.data) or postemp<0:
            return None
        return self.data[postemp]
class DataAnalysis():
    """calss for analysis finance data
    """
    #fibonacci ratio constant
    fibo=1.6180339
    ###boundaryMax and boundaryMin are getValueBoundary return data index constant
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
        self.vmax=10000.0
        self.vmin=0.0
    def clear (self):
        del self.sourceData
        self.sourceData=[]
        del self.drawDataArray
        self.drawDataArray=[]
        self.startPos=0
        self.vmax=10000.0
        self.vmin=0.0
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
        vtemp=self.getValueBoundary()
        if vtemp==None:
            self.clear()
            raise Exception("Get value boundary fail...")
        self.vmax=vtemp[DataAnalysis.boundaryMax]
        self.vmin=vtemp[DataAnalysis.boundaryMin]

        #self.drawDataArray.append(self.calMA(5))
        #for icount in range(len(self.drawDataArray[0].data)):
        #    print(self.drawDataArray[0].data[icount])
    def getValueBoundaryAtPos (self, ipos):
        result=[0.0,10000000000000000000.0]
        if "sourceData" in self.__dict__:
            if len(self.sourceData)==0:
                return None
            if ipos>=len(self.sourceData):
                return None
            for icount in range(GFClass.gfStart, GFClass.gfEnd+1):
                if result[DataAnalysis.boundaryMax]<self.sourceData[ipos][icount]:
                    result[DataAnalysis.boundaryMax]=self.sourceData[ipos][icount]
                if result[DataAnalysis.boundaryMin]>self.sourceData[ipos][icount]:
                    result[DataAnalysis.boundaryMin]=self.sourceData[ipos][icount]
        if len(self.drawDataArray)>0:
            for icount in range(len(self.drawDataArray)):
                #print("data: ", self.drawDataArray[icount].data[ipos])
                if result[DataAnalysis.boundaryMax]<self.drawDataArray[icount].data[ipos]:
                    result[DataAnalysis.boundaryMax]=self.drawDataArray[icount].data[ipos]
                if result[DataAnalysis.boundaryMin]>self.drawDataArray[icount].data[ipos] and self.drawDataArray[icount].data[ipos]!=0:
                    result[DataAnalysis.boundaryMin]=self.drawDataArray[icount].data[ipos]
                #print("max: ",result[DataAnalysis.boundaryMax])
                #print("min: ",result[DataAnalysis.boundaryMin])
        return result
    def getValueBoundaryForLastN (self, inum, startNum=0):
        """get highest and lowest value in number data

        Args:
            inum- number
        Returns:
        Raises:
        """
        if len(self.sourceData)<=startNum:
            return None
        if inum>len(self.sourceData)-startNum:
            rangeNum=len(self.sourceData)-startNum
        else:
            rangeNum=inum
        result=[0.0, 0.0]
        #print("start:{0:d} num:{1:d}".format(startNum, rangeNum))
        for icount in range(rangeNum):
            rtemp=self.getValueBoundaryAtPos(len(self.sourceData)-icount-1-startNum)
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
            #print("{0:f} : {1:f} : {2:f} : {3:f}".format(rtemp[DataAnalysis.boundaryMax],
            #                                                    rtemp[DataAnalysis.boundaryMin],
            #                                                    result[DataAnalysis.boundaryMax],
            #                                                    result[DataAnalysis.boundaryMin]))
        #print("end")
        #sys.stdout.flush()
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
    def getValueBoundary (self):
        """get highest and lowest value in all data

        Args:
        Returns:
        Raises:
        """
        if len(self.sourceData)==0:
            return None
        vtemp=self.getValueBoundaryForLastN(len(self.sourceData))
        self.vmax=vtemp[DataAnalysis.boundaryMax]
        self.vmin=vtemp[DataAnalysis.boundaryMin]
        return vtemp
    def souceDataStart (self, istart):
        """get data

        Args:
            istart- data start
        Returns:
        Raises:
        """
        self.startPos=istart
        postemp=(len(self.sourceData)-istart-1)
        if postemp>=len(self.sourceData) or postemp<0:
            return None
        return self.sourceData[postemp]

    def addToDrawArray (self, idrawdata):
        if type(idrawdata) is DrawData:
            self.drawDataArray.append(idrawdata)
        self.getValueBoundary()
    def sourcedata2Drawdata (self, pos):
        if pos<GFClass.gfStart or pos>GFClass.gfVol:
            return None
        result=DrawData()
        for icount in range(len(self.sourceData)):
            result.data.append(self.sourceData[icount][pos])
        return result
    def calMA (self, period, inputData=None, capStr="", color=QtCore.Qt.black, penWidth=0):
        if inputData==None:
            if len(self.sourceData)==0:
                return None
        elif type(inputData)!=DrawData:
            return None
        result=DrawData()
        result.penW=penWidth
        result.color=color
        if capStr=="":
            result.caption="MA{0:d}".format(period)
        else:
            result.caption=capStr
        vtemp=collections.deque([]) #queue
        if inputData==None:
            loopLen=len(self.sourceData)
        else:
            loopLen=len(inputData.data)
        for icount in range(loopLen):
            if inputData==None:
                vtemp.append(self.sourceData[icount][GFClass.gfEnd])
            else:
                vtemp.append(inputData.data[icount])
            ftemp=0.0;
            if icount>=period-1:
                for jcount in range(period):
                    ftemp=ftemp+vtemp[jcount]
                ftemp=ftemp/period
                vtemp.popleft()
            result.data.append(ftemp)
        return result
    def calWMA (self, period, inputData=None, capStr="", color=QtCore.Qt.black, penWidth=0):
        if inputData==None:
            if len(self.sourceData)==0:
                return None
        elif type(inputData)!=DrawData:
            return None
        result=DrawData()
        result.penW=penWidth
        result.color=color
        if capStr=="":
            result.caption="WMA{0:d}".format(period)
        else:
            result.caption=capStr
        vtemp=collections.deque([]) #queue
        if inputData==None:
            loopLen=len(self.sourceData)
        else:
            loopLen=len(inputData.data)
        for icount in range(loopLen):

            if inputData==None:
                xtemp=self.sourceData[icount][GFClass.gfEnd]
            else:
                xtemp=inputData.data[icount]
            if xtemp!=0:
                vtemp.append(xtemp)
            ftemp=0.0;
            if len(vtemp)>=period:
                totalW=0
                for jcount in range(period):
                    totalW=totalW+jcount+1
                    ftemp=ftemp+vtemp[jcount]*(jcount+1)
                if totalW!=0:
                    ftemp=ftemp/totalW
                else:
                    ftemp=0
                vtemp.popleft()
            result.data.append(ftemp)
        return result
    def calEMA (self, period, inputData=None, capStr="", color=QtCore.Qt.black, penWidth=0):
        if inputData==None:
            if len(self.sourceData)==0:
                return None
        elif type(inputData)!=DrawData:
            return None
        result=DrawData()
        result.penW=penWidth
        result.color=color
        if capStr=="":
            result.caption="EMA{0:d}".format(period)
        else:
            result.caption=capStr
        alpha=2.0/(period+1)
        if inputData==None:
            loopLen=len(self.sourceData)
        else:
            loopLen=len(inputData.data)
        for icount in range(loopLen):
            if inputData==None:
                ftemp=self.sourceData[icount][GFClass.gfEnd]
            else:
                ftemp=inputData.data[icount]
            if icount==0:
                result.data.append(ftemp)
            elif result.data[len(result.data)-1]!=0:
                result.data.append(alpha*ftemp+(1-alpha)*result.data[len(result.data)-1])
            else:
                result.data.append(ftemp)
        return result
    def calHMA (self, period, inputData=None, capStr="", color=QtCore.Qt.black, penWidth=0):
        if inputData==None:
            if len(self.sourceData)==0:
                return None
        elif type(inputData)!=DrawData:
            return None
        if inputData==None:
            srcTemp=self.sourcedata2Drawdata(GFClass.gfEnd)
            if srcTemp==None:
                return None
        else:
            srcTemp=inputData
        wma1=self.calWMA(int(period/2), inputData=srcTemp)
        wma2=self.calWMA(period, inputData=srcTemp)
        wma3=DrawData()
        for icount in range(len(wma1.data)):
            vtemp=(2*wma1.data[icount]-wma2.data[icount])
            if wma1.data[icount]==0 or wma2.data[icount]==0 or vtemp<0:
                wma3.data.append(0)
            else:
                wma3.data.append(vtemp)
        result=self.calWMA(int(math.sqrt(period)), inputData=wma3)
        result.penW=penWidth
        result.color=color
        if capStr=="":
            result.caption="HMA{0:d}".format(period)
        else:
            result.caption=capStr
        return result
    def calKKMA (self, srcperiod, maperiod, inputData=None, capStr="", color=QtCore.Qt.black, penWidth=0):
        if inputData==None:
            if len(self.sourceData)==0:
                return None
        elif type(inputData)!=DrawData:
            return None
        if inputData==None:
            srctemp=self.sourcedata2Drawdata(GFClass.gfEnd)
        else:
            srctemp=inputData
        result0=self.calHMA(srcperiod, inputData=srctemp)
        result0.penW=penWidth
        result0.color=color
        if capStr=="":
            result0.caption="KKMA{0:d}{1:d}_1".format(srcperiod, maperiod)
        else:
            result0.caption=capStr+"_1"
        result1=self.calEMA(maperiod, inputData=result0)
        result1.penW=penWidth
        result1.color=color
        if capStr=="":
            result1.caption="KKMA{0:d}{1:d}_2".format(srcperiod, maperiod)
        else:
            result1.caption=capStr+"_2"
        return [result0, result1]
    def calEmaBand (self, period, mul=1, inputData=None, capStr="",
                    midcolor=QtCore.Qt.black,  outcolor=QtCore.Qt.black,
                    midpenWidth=0, outpenWidth=0):
        if inputData==None:
            if len(self.sourceData)==0:
                return None
        elif len(inputData)!=3:
            return None
        elif type(inputData[0])!=DrawData or type(inputData[1])!=DrawData or type(inputData[2])!=DrawData:
            return None
        ####
        if inputData==None:
            midBand=self.calEMA(period,color=midcolor,penWidth=midpenWidth)
        else:
            midBand=self.calEMA(period, inputData=inputData[2],color=midcolor,penWidth=midpenWidth)
        if capStr=="":
            midBand.caption="EBand{0:d}_M".format(period)
        else:
            midBand.caption=capStr+"_M"
        ####
        if inputData==None:
            srchi=self.sourcedata2Drawdata(GFClass.gfHigh)
            if srchi==None:
                return None
            hitemp=self.calEMA(period, inputData=srchi)
        else:
            hitemp=self.calEMA(period, inputData=inputData[0])
        if hitemp==None:
            return None
        ####
        if inputData==None:
            srclo=self.sourcedata2Drawdata(GFClass.gfLow)
            if srclo==None:
                return None
            lotemp=self.calEMA(period, inputData=srclo)
        else:
            lotemp=self.calEMA(period, inputData=inputData[0])
        if hitemp==None:
            return None
        ####
        hiBand=DrawData()
        hiBand.penW=outpenWidth
        hiBand.color=outcolor
        if capStr=="":
            hiBand.caption="EBand{0:d}_H".format(period)
        else:
            hiBand.caption=capStr+"_H"
        loBand=DrawData()
        loBand.penW=outpenWidth
        loBand.color=outcolor
        if capStr=="":
            loBand.caption="EBand{0:d}_L".format(period)
        else:
            loBand.caption=capStr+"_L"
        for icount in range(len(self.sourceData)):
            temph=hitemp.data[icount]-midBand.data[icount]
            templ=midBand.data[icount]-lotemp.data[icount]
            if temph > templ:
                offset=temph
            else:
                offset=templ
            hiBand.data.append(midBand.data[icount]+offset*mul)
            loBand.data.append(midBand.data[icount]-offset*mul)
        return [hiBand, midBand, loBand]

if __name__ == "__main__":
    data=DataAnalysis()
    data.loadFromCSV("test.csv")
    bantemp=data.calEmaBand(int(90*DataAnalysis.fibo), mul=DataAnalysis.fibo*12,
                            midcolor=QtCore.Qt.darkGreen, outcolor=QtCore.Qt.darkMagenta,
                            midpenWidth=0, outpenWidth=3)
    #data.addToDrawArray(bantemp[0])
    #data.addToDrawArray(bantemp[1])
    data.addToDrawArray(bantemp[2])
    result=data.getValueBoundary()
    print("1: {0:f} 2: {1:f}".format(result[0], result[1]))
    print("max: {0:f} min: {1:f}".format(data.vmax, data.vmin))

