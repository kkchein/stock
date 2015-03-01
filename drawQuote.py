"""draw google financial data

"""
import sys
import os
import traceback
import PyqtQevent
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from dataAnalysis import *

class DrawQuote(QtGui.QWidget):
    """class to draw finance data from csv file
    """
    def __init__ (self):
        """constructor

        Args:
        Returns:
        Raises:
        """
        self.posW=8
        self.stickW=6
        self.stickOffsetX=50
        self.stickOffsetY=50
        self.startData=0
        self.data=DataAnalysis()
        self.aLine=[]

        QtGui.QWidget.__init__(self)
        self.resizeFlag=False
        #load ui
        self.ui=uic.loadUi("quoteView.ui", self)
        self.ui.graphicsView.setScene(QtGui.QGraphicsScene(self)) #set scene
        #self.ui.graphicsView.setSceneRect(QtCore.QRectF(self.ui.graphicsView.viewport().rect()))
        self.ui.graphicsView.setSceneRect(QtCore.QRectF(0,0,10,10))   #set scent rect
        #self.toLog("{0:s}".format(str(self.ui.graphicsView.rect())))
        self.ui.graphicsView.installEventFilter(self.ui)    #install event filter
        ###
        self.valueMax=self.ui.graphicsView.rect().height()-10-self.stickOffsetY
        self.valueMin=0
        ###
        self.setCoordinate(QtCore.QEvent.Resize)      #set coordinate
        self.ui.pushButtonLoad.clicked.connect(self.loadBtnClicked)
        self.ui.pushButtonClearLog.clicked.connect(self.clearBtnClicked)
        self.ui.pushButtonLeft.clicked.connect(self.leftBtnClicked)
        self.ui.pushButtonRight.clicked.connect(self.rightBtnClicked)
        self.ui.pushButtonZoomIn.clicked.connect(self.zoomInBtnClicked)
        self.ui.pushButtonZoomOut.clicked.connect(self.zoomOutBtnClicked)
        self.ui.horizontalScrollBar.valueChanged.connect(self.scrollBarChanged)
        self.ui.show()
    def eventFilter(self, source, event):
        """event filter function

        Args:
            source- source object
            event- event
        Returns:
        Raises:
        """
        #self.toLog(PyqtQevent.eventStr[event.type()])
        if (event.type() == QtCore.QEvent.MouseButtonPress):
            pos = QtCore.QPointF(self.ui.graphicsView.mapToScene(event.pos()))
            #self.toLog('mouse press at: (%d, %d)' % (pos.x(), pos.y()))
            #self.toLog('mouse press at: (%d, %d)' % (event.pos().x(), event.pos().y()))
            #if "lastrect" in self.__dict__:
            #    self.ui.graphicsView.scene().removeItem(self.lastrect)
            #self.lastrect=self.ui.graphicsView.scene().addRect(pos.x(),pos.y(),10, 10)
            #self.toLog("num:{0:d}".format(self.x2Num(pos.x())))
            snum=self.x2Num(pos.x())
            #if "positionLine" in self.__dict__ and self.positionLine!=None:
            #    self.ui.graphicsView.scene().removeItem(self.positionLine)
            #self.positionLine=self.ui.graphicsView.scene().addLine(self.num2X(snum),
            #                                                self.value2Y(self.valueMin),
            #                                                self.num2X(snum),
            #                                                self.value2Y(self.valueMax))
            #
            dataPos=self.startData+snum
            iarray=self.data.souceDataStart(dataPos-1)
            if iarray!=None:
                self.toLog("{0:s} Open:{1:.2f} High:{2:.2f} Low:{3:.2f} Close:{4:.2f} Vol:{5:.2f}".format(
                    datetime.datetime.strftime(iarray[GFClass.gfDate], "%Y/%m/%d"),
                    iarray[GFClass.gfStart],
                    iarray[GFClass.gfHigh],
                    iarray[GFClass.gfLow],
                    iarray[GFClass.gfEnd],
                    iarray[GFClass.gfVol]))
            #self.axisX=self.ui.graphicsView.scene().addLine(self.viewX(0)-self.stickOffsetX,
            #                                                self.value2Y(iarray[GFClass.gfStart]),
            #                                                self.viewX(self.vwidth)-self.stickOffsetX,
            #                                                self.value2Y(iarray[GFClass.gfStart]))
            if len(self.data.drawDataArray)!=0:
                if len(self.aLine)!=0:
                    for icount in range(len(self.aLine)):
                        self.ui.graphicsView.scene().removeItem(self.aLine[icount])
                    self.aLine=[]
                strtemp=""
                for icount in range(len(self.data.drawDataArray)):
                    itemp=self.data.drawDataArray[icount].drawDataStart(dataPos-1)
                    if itemp==None:
                        return QtGui.QWidget.eventFilter(self, source, event)
                    self.aLine.append(QtGui.QGraphicsTextItem("{0:.2f}".format(itemp)))
                    self.aLine[len(self.aLine)-1].setPos(self.num2X(0)+self.posW/2,self.value2Y(itemp)-10)
                    self.aLine[len(self.aLine)-1].setDefaultTextColor(self.data.drawDataArray[icount].color)
                    self.ui.graphicsView.scene().addItem(self.aLine[len(self.aLine)-1])
                    self.aLine.append(self.drawAssistLine(snum, itemp))
                    strtemp=strtemp+"{0:s}: {1:.2f};    ".format(self.data.drawDataArray[icount].caption, itemp)
                self.toLog(strtemp)
        elif (event.type() == QtCore.QEvent.Paint):
            if self.resizeFlag==True:
                self.resizeFlag=False
                self.repaint()
        elif (event.type() == QtCore.QEvent.Resize):
            self.resizeFlag=True
        return QtGui.QWidget.eventFilter(self, source, event)
    def repaint (self):
        self.clearScene()
        self.setCoordinate(QtCore.QEvent.Resize)
        self.calValueBoundary()
        self.drawAllData()
    def clearScene (self):
        self.ui.graphicsView.scene().clear()
        self.positionLine=None
        self.axisX=None
        self.axisY=None
        self.aLine=[]
        self.valueMax=self.ui.graphicsView.rect().height()-10-self.stickOffsetY
        self.valueMin=0
    def toLog (self, istr):
        """write string to log window

        Args:
            istr- input string
        Returns:
        Raises:
        """
        self.ui.textBrowser.append(istr)
    def viewX (self, ix):
        """tranfrom user coordinate x to view coordinate x

        Args:
            ix- x position
        Returns:
        Raises:
        """
        return self.zeroX-ix
    def viewY (self, iy):
        """tranfrom user coordinate y to view coordinate y

        Args:
            iy- y position
        Returns:
        Raises:
        """
        return self.zeroY-iy
    def setCoordinate (self, ievent, ix=0.0, iy=0.0):
        """set coordinate

        Args:
            ievent- QEvent.Resize: use graphicsView size to change coordinate; others: use ix iy to set
            ix- coordinate x
            iy- coordinate y
        Returns:
        Raises:
        """
        try:
            if ievent==QtCore.QEvent.Resize:
                self.zeroX=self.ui.graphicsView.rect().width()/2
                self.zeroY=self.ui.graphicsView.rect().height()/2
                self.vwidth=self.ui.graphicsView.rect().width()-10-self.stickOffsetX
                self.vheight=self.ui.graphicsView.rect().height()-10-self.stickOffsetY
            else:
                self.zeroX=0-ix
                self.zeroY=0-iy
            if "axisX" in self.__dict__ and self.axisX!=None:
                self.ui.graphicsView.scene().removeItem(self.axisX)
            self.axisX=self.ui.graphicsView.scene().addLine(self.viewX(0)-self.stickOffsetX,
                                                            self.value2Y(self.valueMin),
                                                            self.viewX(self.vwidth)-self.stickOffsetX,
                                                            self.value2Y(self.valueMin))
            if "axisY" in self.__dict__ and self.axisY!=None:
                self.ui.graphicsView.scene().removeItem(self.axisY)
            self.axisY=self.ui.graphicsView.scene().addLine(self.viewX(0)-self.stickOffsetX,
                                                            self.value2Y(self.valueMin),
                                                            self.viewX(0)-self.stickOffsetX,
                                                            self.value2Y(self.valueMax))
            #if "boundaryrect" in self.__dict__:
            #    self.ui.graphicsView.scene().removeItem(self.boundaryrect)
            #self.boundaryrect=self.ui.graphicsView.scene().addRect(self.viewX(self.vwidth),self.viewY(self.vheight),self.vwidth,self.vheight)
        except Exception as e:
            self.toLog(traceback.format_exc())
    def leftBtnClicked (self):
        self.startData=self.startData+1
        self.repaint()
    def rightBtnClicked (self):
        if self.startData>0:
            self.startData=self.startData-1
            self.repaint()
    def zoomInBtnClicked (self):
        if self.stickW>1:
            self.stickW=self.stickW-1
            self.posW=self.stickW+2
            self.repaint()
    def zoomOutBtnClicked(self):
        self.stickW=self.stickW+1
        self.posW=self.stickW+2
        self.repaint()
    def scrollBarChanged (self, ivalue):
        if ivalue>0:
            self.startData=ivalue
            self.repaint()
    def clearBtnClicked (self):
        """clear log button click handler

        Args:
        Returns:
        Raises:
        """
        self.ui.textBrowser.clear()
        if "positionLine" in self.__dict__ and self.positionLine!=None:
            self.ui.graphicsView.scene().removeItem(self.positionLine)
    def loadBtnClicked (self):
        """load button handler

        Args:
        Returns:
        Raises:
        """
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File", ".", "csv (*.csv)")
        if os.path.exists(fileName)==False:
            self.toLog(fileName+" doesn't exist")
            return
        self.data.clear()
        self.clearScene()
        self.setCoordinate(QtCore.QEvent.Resize)
        self.clearBtnClicked()
        self.data.loadFromCSV(fileName)
        self.assistData()
        self.calValueBoundary()
        self.drawAllData()
        self.toLog("Data length {0:d}".format(len(self.data.sourceData)))

    def calValueBoundary (self):
        """calculate value boundary

        Args:
        Returns:
        Raises:
        """
        try:
            #raise Exception("sss")
            self.drawNum=int(self.vwidth/self.posW)-1
            #self.toLog("w number:{0:d}".format(self.drawNum))
            bound=self.data.getValueBoundaryForLastN(self.drawNum, self.startData)
            if bound==None:
                return
            self.valueMax=bound[DataAnalysis.boundaryMax]*1.01
            self.valueMin=bound[DataAnalysis.boundaryMin]*0.99
            #self.toLog("bound:{0:f};{1:f}".format(bound[DataAnalysis.boundaryMax], bound[DataAnalysis.boundaryMin]))
            self.ui.horizontalScrollBar.setMaximum(len(self.data.sourceData)-self.drawNum+10)
            self.ui.horizontalScrollBar.setPageStep(int(self.drawNum/10))
            self.ui.horizontalScrollBar.setInvertedAppearance(True)
            self.ui.horizontalScrollBar.setInvertedControls(False)
            self.ui.horizontalScrollBar.setInvertedControls(True)
        except Exception as e:
            self.toLog(traceback.format_exc())
    def drawAllData (self):
        """draw stick with data

        Args:
        Returns:
        Raises:
        """
        try:
            self.drawCandleStick()
            self.drawData()
        except Exception as e:
            self.toLog(traceback.format_exc())
    def num2X (self, inum):
        """transform position number to view coodinate x

        Args:
            inum- position
        Returns:
            view x
        Raises:
        """
        return self.viewX(self.posW*inum+self.posW/2)-self.stickOffsetX
    def x2Num (self, ix):
        return int((self.viewX(ix)-self.stickOffsetX)/self.posW)

    def value2Y (self, ivalue):
        """transform data value to view coodinate y

        Args:
            ivalue- data value
        Returns:
        Raises:
        """
        ivtemp=(float(ivalue)-float(self.valueMin))*float(self.vheight)/(float(self.valueMax)-float(self.valueMin))
        result=self.viewY(ivtemp)-self.stickOffsetY
        #self.toLog("ivalue:{0:f};ivtemp:{1:f};result:{2:f}".format(
        #    ivalue,
        #    ivtemp,
        #    result))
        return result
    def drawCandleStick (self):
        """draw candle stick on view

        Args:
        Returns:
        Raises:
        """
        if "drawNum" not in self.__dict__:
            return
        for icount in range(self.drawNum):
            dataPos=self.startData+icount
            iarray=self.data.souceDataStart(dataPos)
            if iarray==None:
                break
            istart=iarray[GFClass.gfStart]
            ihigh=iarray[GFClass.gfHigh]
            ilow=iarray[GFClass.gfLow]
            iend=iarray[GFClass.gfEnd]
            ipos=icount+1
            self.ui.graphicsView.scene().addLine(self.num2X(ipos),
                                                 self.value2Y(ihigh),
                                                 self.num2X(ipos),
                                                 self.value2Y(ilow))
            if istart<=iend:
                brushtemp=QtGui.QBrush(QtGui.QColor(255,0,0))
                self.ui.graphicsView.scene().addRect(self.num2X(ipos)-self.stickW/2,
                                                     self.value2Y(iend),
                                                     self.stickW,
                                                     self.value2Y(istart)-self.value2Y(iend),
                                                     brush=brushtemp)
            else:
                brushtemp=QtGui.QBrush(QtGui.QColor(0,255,0))
                self.ui.graphicsView.scene().addRect(self.num2X(ipos)-self.stickW/2,
                                                     self.value2Y(istart),
                                                     self.stickW,
                                                     self.value2Y(iend)-self.value2Y(istart),
                                                     brush=brushtemp)
    def drawData (self):
        if "drawNum" not in self.__dict__:
            return
        if len(self.data.drawDataArray)==0:
            return
        for icount in range(len(self.data.drawDataArray)):
            if self.data.drawDataArray[icount].drawType==DrawData.dtypeLine:
                for jcount in range(self.drawNum):
                    dataPos=self.startData+jcount
                    ipos=jcount+1
                    iline=self.data.drawDataArray[icount].drawDataStart(dataPos)
                    if iline==None:
                        break
                    if jcount!=0:
                        if iline!=0:
                            pentemp=QtGui.QPen(self.data.drawDataArray[icount].color)
                            pentemp.setWidth(self.data.drawDataArray[icount].penW)
                            self.ui.graphicsView.scene().addLine(self.num2X(ipos),
                                                                 self.value2Y(iline),
                                                                 self.num2X(ipos-1),
                                                                 self.value2Y(lastLine),
                                                                 pen=pentemp)
                            #self.toLog("po{0:d};{1:f};{2:f}".format(ipos,iline,lastLine))
                    lastLine=iline
    def drawAssistLine (self, ipos, ivalue):
        return self.ui.graphicsView.scene().addLine(self.num2X(0),
                                                    self.value2Y(ivalue),
                                                    self.num2X(ipos),
                                                    self.value2Y(ivalue),
                                                    pen=QtGui.QPen(QtCore.Qt.lightGray))
    def final (self):
        pass
    def assistData (self):
        try:
            ####
            #self.data.addToDrawArray(self.data.calMA(60, color=QtCore.Qt.red))
            #self.data.addToDrawArray(self.data.calWMA(60, color=QtCore.Qt.green))
            #self.data.addToDrawArray(self.data.calEMA(60, color=QtCore.Qt.blue))
            #self.data.addToDrawArray(self.data.calHMA(60, color=QtCore.Qt.magenta))
            ####option 1
            #bantemp=self.data.calEmaBand(int(90*DataAnalysis.fibo), mul=DataAnalysis.fibo*12,
            #                             midcolor=QtCore.Qt.darkGreen, outcolor=QtCore.Qt.darkMagenta,
            #                             midpenWidth=0, outpenWidth=3)
            #self.data.addToDrawArray(bantemp[0])
            #self.data.addToDrawArray(bantemp[1])
            #self.data.addToDrawArray(bantemp[2])
            #bantemp=self.data.calEmaBand(int(30*DataAnalysis.fibo), mul=DataAnalysis.fibo*4,
            #                             midcolor=QtCore.Qt.lightGray, outcolor=QtCore.Qt.magenta)
            #self.data.addToDrawArray(bantemp[0])
            #self.data.addToDrawArray(bantemp[1])
            #self.data.addToDrawArray(bantemp[2])
            #matemp=self.data.calKKMA(280,40,
            #                         color=QtCore.Qt.red,
            #                         penWidth=2)
            #self.data.addToDrawArray(matemp[0])
            #self.data.addToDrawArray(matemp[1])
            #matemp=self.data.calKKMA(112,16,
            #                         color=QtCore.Qt.green,
            #                         penWidth=2)
            #self.data.addToDrawArray(matemp[0])
            #self.data.addToDrawArray(matemp[1])
            #matemp=self.data.calKKMA(28,4,
            #                         color=QtCore.Qt.blue,
            #                         penWidth=2)
            #self.data.addToDrawArray(matemp[0])
            #self.data.addToDrawArray(matemp[1])
            ####
            bantemp=self.data.calEmaBand(int(90*DataAnalysis.fibo), mul=DataAnalysis.fibo*12,
                                         midcolor=QtCore.Qt.darkGreen, outcolor=QtCore.Qt.darkMagenta,
                                         midpenWidth=0, outpenWidth=3)
            self.data.addToDrawArray(bantemp[0])
            self.data.addToDrawArray(bantemp[1])
            self.data.addToDrawArray(bantemp[2])
            bantemp=self.data.calEmaBand(int(30*DataAnalysis.fibo), mul=DataAnalysis.fibo*4,
                                         midcolor=QtCore.Qt.lightGray, outcolor=QtCore.Qt.magenta)
            self.data.addToDrawArray(bantemp[0])
            self.data.addToDrawArray(bantemp[1])
            self.data.addToDrawArray(bantemp[2])
            #matemp=self.data.calKKMA(280,40,
            #                         color=QtCore.Qt.red,
            #                         penWidth=2)
            #self.data.addToDrawArray(matemp[0])
            #self.data.addToDrawArray(matemp[1])
            matemp=self.data.calKKMA(112,16,
                                     color=QtCore.Qt.green,
                                     penWidth=2)
            self.data.addToDrawArray(matemp[0])
            self.data.addToDrawArray(matemp[1])
            #matemp=self.data.calKKMA(28,4,
            #                         color=QtCore.Qt.blue,
            #                         penWidth=2)
            #self.data.addToDrawArray(matemp[0])
            #self.data.addToDrawArray(matemp[1])
        except Exception as e:
            self.toLog(traceback.format_exc())

if __name__ == "__main__":
    try:
        app = QtGui.QApplication(sys.argv)
        mainui=DrawQuote()
        app.exec_()
    finally:
        if "mainui" in locals():
            mainui.final()

