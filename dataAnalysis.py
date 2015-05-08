"""process data
"""
import sys
import collections
import math
import csv
import datetime
import time
from PyQt4 import QtCore

class DrawData:
    """draw data object
    """
    dtypeNone=0
    dtypeLine=1
    dtypeDiff=2
    dtypeValue=3
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
        """get drawdata at start position

        Args:
            istart - start position
        Returns:
        Raises:
        """
        self.startPos=istart
        postemp=(len(self.data)-istart-1)
        if postemp>=len(self.data) or postemp<0:
            return None
        return self.data[postemp]
    def __getitem__ (self, ind):
        return self.data[ind]
    def __str__ (self):
        stemp=self.caption+"\n"
        for icount in range(len(self.data)):
            stemp=stemp+"Value: {0:.2f}\n".format(self.data[icount].caption, len(self.data[icount]))
        return stemp
    def __len__ (self):
        return len(self.data)
class DataAnalysis():
    """calss for analysis finance data
    """
    #fibonacci ratio constant
    fibo=1.6180339
    ###boundaryMax and boundaryMin are getValueBoundary return data index constant
    boundaryMax=0
    boundaryMin=1
    ###
    gfDate=0
    gfStart=1
    gfHigh=2
    gfLow=3
    gfEnd=4
    gfVol=5
    dataStrType="%Y/%m/%d"
    def __init__ (self):
        """constructor

        Args:
        Returns:
        Raises:
        """
        self.sourceData=[]
        self.drawDataArray=[]
        self.startPos=0
        self.vmax=10000.0
        self.vmin=0.0
        self.clearTemp()
    def __str__ (self):
        stemp="Source data size: {0:d}\n".format(len(self.sourceData))
        for icount in range(len(self.drawDataArray)):
            stemp=stemp+"{0:s} - size {1:d}\n".format(self.drawDataArray[icount].caption, len(self.drawDataArray[icount]))
        return stemp
    def clear (self):
        """clear data

        Args:
        Returns:
        Raises:
        """
        del self.sourceData
        self.sourceData=[]
        del self.drawDataArray
        self.drawDataArray=[]
        self.startPos=0
        self.vmax=10000.0
        self.vmin=0.0
        ###
        self.clearTemp()
    def clearTemp (self):
        self.starttemp=[]
        self.endtemp=[]
        self.hightemp=[]
        self.lowtemp=[]
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
            dt = datetime.datetime.fromtimestamp(time.mktime(time.strptime(i[0], DataAnalysis.dataStrType)))
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
            csvContent.writerow([datetime.datetime.strftime(idata[icount][0], DataAnalysis.dataStrType),
                             str(idata[icount][1]),
                             str(idata[icount][2]),
                             str(idata[icount][3]),
                             str(idata[icount][4]),
                             str(idata[icount][5])])
        csvFileW.close
    def listReduce (self, idata, odata, period=2):
        icount=0
        pcount=0
        while icount<len(idata):
            if pcount==0:
                dtemp=idata[icount][DataAnalysis.gfDate]
                stemp=idata[icount][DataAnalysis.gfStart]
                htemp=idata[icount][DataAnalysis.gfHigh]
                ltemp=idata[icount][DataAnalysis.gfLow]
                etemp=idata[icount][DataAnalysis.gfEnd]
                vtemp=idata[icount][DataAnalysis.gfVol]
            else:
                if htemp<idata[icount][DataAnalysis.gfHigh]:
                    htemp=idata[icount][DataAnalysis.gfHigh]
                if ltemp>idata[icount][DataAnalysis.gfLow]:
                    ltemp=idata[icount][DataAnalysis.gfLow]
                etemp=idata[icount][DataAnalysis.gfEnd]
                vtemp=vtemp+idata[icount][DataAnalysis.gfVol]
            icount=icount+1
            pcount=pcount+1
            if pcount==period:
                pcount=0
                odata.append([dtemp, stemp, htemp, ltemp, etemp, vtemp])
            else:
                if icount==len(idata):
                    odata.append([dtemp, stemp, htemp, ltemp, etemp, vtemp])
            
    def loadFromCSV (self, ifname):
        """load data from csv file

        Args:
            ifname- csv file name
        Returns:
        Raises:
        """
        #self.sourceData=[]  #clear data
        self.clear()
        self.csv2list(ifname, self.sourceData)
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
        """get max/min value at position

        Args:
            ipos - position
        Returns:
        Raises:
        """
        result=[0.0,10000000000000000000.0]
        if "sourceData" in self.__dict__:
            if len(self.sourceData)==0:
                return None
            if ipos>=len(self.sourceData):
                return None
            if result[DataAnalysis.boundaryMax]<self.sourceData[ipos][DataAnalysis.gfHigh]:
                result[DataAnalysis.boundaryMax]=self.sourceData[ipos][DataAnalysis.gfHigh]
            if result[DataAnalysis.boundaryMin]>self.sourceData[ipos][DataAnalysis.gfLow]:
                result[DataAnalysis.boundaryMin]=self.sourceData[ipos][DataAnalysis.gfLow]
        else:
            return None
        if len(self.drawDataArray)>0:
            for icount in range(len(self.drawDataArray)):
                if self.drawDataArray[icount].drawType==DrawData.dtypeLine:
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
        if len(self.sourceData)<=startNum:
            return None
        if inum+startNum>len(self.sourceData):
            rangeNum=len(self.sourceData)-startNum
        else:
            rangeNum=inum
        result=[0.0, 0.0]
        #print("start:{0:d} num:{1:d}".format(startNum, rangeNum))
        for icount in range(int(rangeNum)):
            rtemp=self.getValueBoundaryAtPos(icount+int(startNum))
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
    def addToDrawArray (self, idrawdata):
        """add draw data into array

        Args:
            idrawdata- draw data
        Returns:
        Raises:
        """
        if type(idrawdata) is DrawData:
            self.drawDataArray.append(idrawdata)
        self.getValueBoundary()
    def sourcedata2Drawdata (self, pos):
        """convert source data to drawdata

        Args:
            pos - source data offset position
        Returns:
        Raises:
        """
        if pos<DataAnalysis.gfStart or pos>DataAnalysis.gfVol:
            return None
        result=DrawData()
        for icount in range(len(self.sourceData)):
            result.data.append(self.sourceData[icount][pos])
        return result
    def calMAOnetick (self, period, odata, iData):
        if type(odata)!=DrawData:
            raise Exception("odata is not DrawData.")
        self.endtemp.append(iData)
        if len(self.endtemp)>=period:
            vtemp=0.0
            for icount in range(period):
                vtemp=vtemp+self.endtemp[len(self.endtemp)-1-icount]
            odata.data.append(vtemp/period)
        else:
            odata.data.append(0)
    def calMA (self, period, inputData=None, capStr="", color=QtCore.Qt.black, penWidth=0):
        """calculate moving average

        Args:
            period - moving average period
            inpuData - original data, None- use source data as input
            capStr - caption string
            color - drawing color
            penWidth - drawing pen width
        Returns:
        Raises:
        """
        if inputData==None:
            if len(self.sourceData)==0:
                return None
            inputData=self.sourcedata2Drawdata(DataAnalysis.gfEnd)
        elif type(inputData)!=DrawData:
            return None
        result=DrawData()
        result.penW=penWidth
        result.color=color
        if capStr=="":
            result.caption="MA{0:d}".format(period)
        else:
            result.caption=capStr
        #for icount in range(len(inputData)):
        #    data2.calMAOnetick(period, result, inputData[icount][DataAnalysis.gfEnd])
        vtemp=collections.deque([]) #queue
        loopLen=len(inputData)
        for icount in range(loopLen):
            vtemp.append(inputData[icount])                
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
                xtemp=self.sourceData[icount][DataAnalysis.gfEnd]
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
                ftemp=self.sourceData[icount][DataAnalysis.gfEnd]
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
            srcTemp=self.sourcedata2Drawdata(DataAnalysis.gfEnd)
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
            srctemp=self.sourcedata2Drawdata(DataAnalysis.gfEnd)
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
        #calculate diff
        result2=DrawData()
        result2.drawType=DrawData.dtypeDiff
        if capStr=="":
            result2.caption="KKMA{0:d}{1:d}_Diff".format(srcperiod, maperiod)
        else:
            result2.caption=capStr+"_Diff"
        for icount in range(len(result0.data)):
            result2.data.append(result0.data[icount]-result1.data[icount])
        return [result0, result1, result2]
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
            srchi=self.sourcedata2Drawdata(DataAnalysis.gfHigh)
            if srchi==None:
                return None
            hitemp=self.calEMA(period, inputData=srchi)
        else:
            hitemp=self.calEMA(period, inputData=inputData[0])
        if hitemp==None:
            return None
        ####
        if inputData==None:
            srclo=self.sourcedata2Drawdata(DataAnalysis.gfLow)
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
    def calHmaBand (self, period, mul=1, inputData=None, capStr="",
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
            midBand=self.calHMA(period,color=midcolor,penWidth=midpenWidth)
        else:
            midBand=self.calHMA(period, inputData=inputData[2],color=midcolor,penWidth=midpenWidth)
        if capStr=="":
            midBand.caption="HBand{0:d}_M".format(period)
        else:
            midBand.caption=capStr+"_M"
        ####
        if inputData==None:
            srchi=self.sourcedata2Drawdata(DataAnalysis.gfHigh)
            if srchi==None:
                return None
            hitemp=self.calHMA(period, inputData=srchi)
        else:
            hitemp=self.calHMA(period, inputData=inputData[0])
        if hitemp==None:
            return None
        ####
        if inputData==None:
            srclo=self.sourcedata2Drawdata(DataAnalysis.gfLow)
            if srclo==None:
                return None
            lotemp=self.calHMA(period, inputData=srclo)
        else:
            lotemp=self.calHMA(period, inputData=inputData[0])
        if hitemp==None:
            return None
        ####
        hiBand=DrawData()
        hiBand.penW=outpenWidth
        hiBand.color=outcolor
        if capStr=="":
            hiBand.caption="HBand{0:d}_H".format(period)
        else:
            hiBand.caption=capStr+"_H"
        loBand=DrawData()
        loBand.penW=outpenWidth
        loBand.color=outcolor
        if capStr=="":
            loBand.caption="HBand{0:d}_L".format(period)
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
            #hiBand.data.append(midBand.data[icount]+temph*mul)
            #loBand.data.append(midBand.data[icount]-templ*mul)
        return [hiBand, midBand, loBand]
    def calATR (self, period, mul=1, capStr=""):
        if len(self.sourceData)==0:
            return None
        if capStr=="":
            rstr="ATR{0:d}".format(period)
        else:
            rstr=capStr
        self.sourceData[0][DataAnalysis.gfEnd]
        vatemp=DrawData()
        for icount in range(len(self.sourceData)):
            if icount==0:
                rtemp=math.fabs(self.sourceData[icount][DataAnalysis.gfHigh]-self.sourceData[icount][DataAnalysis.gfLow])
                vatemp.data.append(rtemp)
            else:
                rtemp=math.fabs(self.sourceData[icount][DataAnalysis.gfHigh]-self.sourceData[icount-1][DataAnalysis.gfLow])
                stemp=math.fabs(self.sourceData[icount][DataAnalysis.gfHigh]-self.sourceData[icount-1][DataAnalysis.gfEnd])
                if stemp>rtemp:
                    rtemp=stemp
                stemp=math.fabs(self.sourceData[icount][DataAnalysis.gfLow]-self.sourceData[icount-1][DataAnalysis.gfEnd])
                if stemp>rtemp:
                    rtemp=stemp
                vatemp.data.append(rtemp)
        #for item in vatemp.data:
        #    print(item)
        result=self.calHMA(period,vatemp,rstr)
        result.drawType=DrawData.dtypeValue
        return result


if __name__ == "__main__":
    data=DataAnalysis()
    data.loadFromCSV("./csv/test.csv")
    temp=data.calATR(14)
    for item in temp.data:
        print(item)
    #bantemp=data.calEmaBand(int(90*DataAnalysis.fibo), mul=DataAnalysis.fibo*12,
    #                        midcolor=QtCore.Qt.darkGreen, outcolor=QtCore.Qt.darkMagenta,
    #                        midpenWidth=0, outpenWidth=3)
    #print(bantemp[0])
    #print(bantemp[0][0])
    #print(bantemp[0][1])
    #data.addToDrawArray(bantemp[0])
    #data.addToDrawArray(bantemp[1])
    #data.addToDrawArray(bantemp[2])
    #result=data.getValueBoundary()
    #result=data.getValueBoundaryForLastN(5)
    #print("1: {0:f} 2: {1:f}".format(result[0], result[1]))
    #print("max: {0:f} min: {1:f}".format(data.vmax, data.vmin))
    #print(data)

