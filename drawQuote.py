"""draw google financial data

"""
import sys
import os
import traceback
import math
import PyqtQevent
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from dataAnalysis import *

class DrawQuote(QtGui.QMainWindow):
    """draw finance data from csv file
    """
    def __init__ (self):
        """constructor

        Args:
        Returns:
        Raises:
        """
        QtGui.QWidget.__init__(self)
        self.data=DataAnalysis()    #create data analysis object
        ###
        self.lastPos=0
        ###
        self.posW=10
        self.stickW=8
        self.dotW=6
        ###scene rect
        self.sceneRect=QtCore.QRectF()
        self.sceneRect.setBottomRight(QtCore.QPointF(0,self.value2Scene(self.data.vmin)))
        self.sceneRect.setTopLeft(QtCore.QPointF(-100,self.value2Scene(self.data.vmax)))
        self.viewRect=QtCore.QRectF()
        self.viewRect.setBottomRight(QtCore.QPointF(0,self.value2Scene(self.data.vmin)))
        self.viewRect.setTopLeft(QtCore.QPointF(-100,self.value2Scene(self.data.vmax)))
        ###
        self.valueSceneRect=QtCore.QRectF()
        self.valueSceneRect.setBottomRight(QtCore.QPointF(0,self.value2Scene(self.data.vmin)))
        self.valueSceneRect.setTopLeft(QtCore.QPointF(-50,self.value2Scene(self.data.vmax)))
        self.valueViewRect=QtCore.QRectF()
        self.valueViewRect.setBottomRight(QtCore.QPointF(0,self.value2Scene(self.data.vmin)))
        self.valueViewRect.setTopLeft(QtCore.QPointF(-50,self.value2Scene(self.data.vmax)))
        ###
        self.scaleXOffset=0
        self.scaleYRation=1.0
        ###
        self.resizeFlag=False   #resize event flag
        ###
        self.crossTempLine=[]
        self.drawTempLine=[]
        self.drawTempPoint=[]
        self.drawMoveTempLine=[]
        ###load pyqt ui
        self.ui=uic.loadUi("./res/quoteViewMainWindow.ui", self) #load ui
        ###setup main graphicsview
        self.ui.graphicsView.setScene(QtGui.QGraphicsScene(self)) #set scene
        self.ui.graphicsView.viewport().installEventFilter(self.ui)    #install event filter
        ###load toolbar button
        self.actionLoad = QtGui.QAction(QtGui.QIcon('./res/Actions-document-open-icon.png'),
                                        "Open stick data", self, triggered=self.loadBtnClicked)
        self.ui.toolBar.addAction(self.actionLoad)
        ###clear log toolbar button
        self.actionClearLog = QtGui.QAction(QtGui.QIcon('./res/Actions-edit-clear-icon.png'),
                                            "Clear log window", self, triggered=self.clearBtnClicked)
        self.ui.toolBar.addAction(self.actionClearLog)
        ###fit windows toolbar button
        self.actionFitWindow = QtGui.QAction(QtGui.QIcon('./res/Printing-Fit-To-Width-icon.png'),
                                             "Fit window", self, triggered=self.fitBtnClicked)
        self.ui.toolBar.addAction(self.actionFitWindow)
        ###zoom in toolbar button
        self.actionZoomIn = QtGui.QAction(QtGui.QIcon('./res/Zoom-In-icon.png'),
                                          "Zoom In", self, triggered=self.zoomInBtnClicked)
        self.ui.toolBar.addAction(self.actionZoomIn)
        ###zoom out toolbar button
        self.actionZoomOut = QtGui.QAction(QtGui.QIcon('./res/Zoom-Out-icon.png'),
                                           "Zoom Out", self, triggered=self.zoomOutBtnClicked)
        self.ui.toolBar.addAction(self.actionZoomOut)
        ###cross line  toolbar button
        self.actionCrossLine = QtGui.QAction(QtGui.QIcon('./res/add-icon.png'),
                                             "Assistant cross line", self, triggered=self.checkBoxCrossLineChanged)
        self.actionCrossLine.setCheckable(True)
        self.ui.toolBar.addAction(self.actionCrossLine)
        ###drag toolbar button
        self.actionDrag = QtGui.QAction(QtGui.QIcon('./res/Drag-icon.png'),
                                        "Drag view", self, triggered=self.checkBoxDragChanged)
        self.actionDrag.setCheckable(True)
        self.ui.toolBar.addAction(self.actionDrag)
        ###draw line toolbar button
        self.actionDrawLine = QtGui.QAction(QtGui.QIcon('./res/Line-icon.png'),
                                            "Draw line", self, triggered=self.checkBoxDrawLineChanged)
        self.actionDrawLine.setCheckable(True)
        self.ui.toolBar.addAction(self.actionDrawLine)
        ###setup status bar
        self.labelCurrent=QtGui.QLabel(self)
        self.labelCurrent.setMinimumWidth(150)
        self.ui.statusbar.addWidget(self.labelCurrent)
        self.labelValue=QtGui.QLabel(self)
        self.ui.statusbar.addWidget(self.labelValue)
        ###
        self.ui.show()
    def checkBoxDrawLineChanged (self):
        if self.actionDrawLine.isChecked()==False:
            self.drawTempPoint=[]
            if len(self.drawTempLine)!=0:
                for icount in range(len(self.drawTempLine)):
                    self.ui.graphicsView.scene().removeItem(self.drawTempLine[icount])
                self.drawTempLine=[]
            if len(self.drawMoveTempLine)!=0:
                for icount in range(len(self.drawMoveTempLine)):
                    self.ui.graphicsView.scene().removeItem(self.drawMoveTempLine[icount])
                self.drawMoveTempLine=[]
    def checkBoxDragChanged (self):
        if self.actionDrag.isChecked()==True:
            self.ui.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        else:
            self.ui.graphicsView.setDragMode(QtGui.QGraphicsView.NoDrag)
    def checkBoxCrossLineChanged (self):
        if self.actionCrossLine.isChecked()==False:
            if len(self.crossTempLine)!=0:
                for icount in range(len(self.crossTempLine)):
                    self.ui.graphicsView.scene().removeItem(self.crossTempLine[icount])
                self.crossTempLine=[]
    def fitBtnClicked (self):
        """button left click handler

        Args:
        Returns:
        Raises:
        """
        #self.scaleXOffset=0
        #self.getRealViewRect()
        self.setView(self.getViewRightPos())
    def zoomInBtnClicked (self):
        """button zoom in click handler

        Args:
        Returns:
        Raises:
        """
        #if self.scaleXOffset>1:
        #    self.scaleXOffset=0
        self.scaleXOffset=self.scaleXOffset-2
        #self.getRealViewRect()
        self.setView(self.getViewRightPos())
        #self.scaleXOffset=0
    def zoomOutBtnClicked(self):
        """button zoom out click handler

        Args:
        Returns:
        Raises:
        """
        #if self.scaleXOffset<-1:
        #    self.scaleXOffset=0
        self.scaleXOffset=self.scaleXOffset+2
        #self.getRealViewRect()
        self.setView(self.getViewRightPos())
    def clearBtnClicked (self):
        """button clear log click handler

        Args:
        Returns:
        Raises:
        """
        self.ui.textBrowser.clear()
    def loadBtnClicked (self):
        """button load handler

        Args:
        Returns:
        Raises:
        """
        ###open file dialog
        if os.path.exists("./csv")==True:
            csvdir="./csv/"
        else:
            csvdir="./"
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File", csvdir, "csv (*.csv)")
        if os.path.exists(fileName)==False:
            self.toLog(fileName+" doesn't exist")
            return
        if self.actionCrossLine.isChecked()==True:
            self.actionCrossLine.setChecked(False)
            self.checkBoxDragChanged()
        self.data.clear()
        #self.clearBtnClicked()
        self.clearScene()
        #load data from csv
        self.data.loadFromCSV(fileName)
        self.assistData()
        self.setScene()
        self.setView()
        self.drawCandleStick()
        self.drawAssistData()
        self.toLog("Data length {0:d}".format(len(self.data.sourceData)))
    def drawCrossLineAndText (self, pos):
        """draw assisntant cross line and stick bar information

        Args:
            pos - scane position
        Returns:
        Raises:
        """
        if len(self.data.sourceData)<=0:
            return
        ipos=self.scene2pos(pos.x())
        if ipos!=self.lastPos:
            self.lastPos=ipos
            if ipos<len(self.data.sourceData):
                iarray=self.data.sourceData[ipos]
                idate=iarray[DataAnalysis.gfDate]
                istart=iarray[DataAnalysis.gfStart]
                ihigh=iarray[DataAnalysis.gfHigh]
                ilow=iarray[DataAnalysis.gfLow]
                iend=iarray[DataAnalysis.gfEnd]
                ivol=iarray[DataAnalysis.gfVol]
                self.labelValue.setText("{0:s} End:{1:.2f}  start:{2:.2f} High:{3:.2f} Low:{4:.2f} Vol:{5:.2f}".format(datetime.datetime.strftime(idate, DataAnalysis.dataStrType),
                                                                                                                          iend,
                                                                                                                          istart,
                                                                                                                          ihigh,
                                                                                                                          ilow,
                                                                                                                          ivol))
            else:
                self.labelValue.setText("")
        if len(self.crossTempLine)!=0:
            for icount in range(len(self.crossTempLine)):
                self.ui.graphicsView.scene().removeItem(self.crossTempLine[icount])
            self.crossTempLine=[]
        self.crossTempLine.append(self.ui.graphicsView.scene().addLine(self.pos2Scene(ipos),
                                                                  self.sceneRect.bottom(),
                                                                  self.pos2Scene(ipos),
                                                                  self.sceneRect.top()))

        self.crossTempLine.append(self.ui.graphicsView.scene().addLine(self.sceneRect.right(),
                                                                  pos.y(),
                                                                  self.sceneRect.left(),
                                                                  pos.y()))
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
            if event.button() == QtCore.Qt.LeftButton:
                if self.actionDrawLine.isChecked()==True:
                    self.drawTempPoint.append(pos)
                    if len(self.drawMoveTempLine)!=0:
                        for icount in range(len(self.drawMoveTempLine)):
                            self.ui.graphicsView.scene().removeItem(self.drawMoveTempLine[icount])
                        self.drawMoveTempLine=[]
                    if len(self.drawTempPoint)>=2:
                        self.drawTempLine.append(self.ui.graphicsView.scene().addLine(self.drawTempPoint[0].x(),
                                                                                      self.drawTempPoint[0].y(),
                                                                                      self.drawTempPoint[1].x(),
                                                                                      self.drawTempPoint[1].y()))
                        del self.drawTempPoint
                        self.drawTempPoint=[]
                #pass
            elif event.button() == QtCore.Qt.RightButton:
                if self.actionCrossLine.isChecked()==False:
                    self.actionCrossLine.setChecked(True)
                    self.checkBoxDragChanged()
                    self.drawCrossLineAndText(pos)
                if len(self.data.drawDataArray)!=0:
                    ipos=self.scene2pos(pos.x())
                    laststr=""
                    resultstr="Assistant Data\n"
                    for icount in range(len(self.data.drawDataArray)):
                        strtemp=self.data.drawDataArray[icount].caption.split("_")[0]
                        if icount==0:
                            laststr=strtemp
                        if laststr!=strtemp:
                            laststr=strtemp
                            resultstr=resultstr+"\n"
                        resultstr=resultstr+"{0:s} - {1:.2f};  ".format(self.data.drawDataArray[icount].caption,
                                                                        self.data.drawDataArray[icount][ipos])
                    if resultstr!="":
                        self.toLog(resultstr)
        elif (event.type() == QtCore.QEvent.Paint):
            if self.resizeFlag==True:
                self.resizeFlag=False
                self.getRealViewRect()
                self.setView()
        elif (event.type() == QtCore.QEvent.Resize):
            self.resizeFlag=True
        elif (event.type() == QtCore.QEvent.MouseMove):
            pos = QtCore.QPointF(self.ui.graphicsView.mapToScene(event.pos()))
            self.labelCurrent.setText("Pos:{0:d} Value:{1:.2f}".format(self.scene2pos(pos.x()), self.scene2Value(pos.y())))
            if self.actionCrossLine.isChecked()==True:
                self.drawCrossLineAndText(pos)
            if self.actionDrawLine.isChecked()==True:
                if len(self.drawMoveTempLine)!=0:
                    for icount in range(len(self.drawMoveTempLine)):
                        self.ui.graphicsView.scene().removeItem(self.drawMoveTempLine[icount])
                    self.drawMoveTempLine=[]
                if len(self.drawTempPoint)==1:
                    self.drawMoveTempLine.append(self.ui.graphicsView.scene().addLine(self.drawTempPoint[0].x(),
                                                                                      self.drawTempPoint[0].y(),
                                                                                      pos.x(),
                                                                                      pos.y()))
        elif (event.type() == QtCore.QEvent.MouseButtonRelease):
            #pos = QtCore.QPointF(self.ui.graphicsView.mapToScene(event.pos()))
            if event.button() == QtCore.Qt.LeftButton:
                pass
            elif event.button() == QtCore.Qt.RightButton:
                pass
        elif (event.type() == QtCore.QEvent.WindowDeactivate):
            if self.actionCrossLine.isChecked()==True:
                self.actionCrossLine.setChecked(False)
                self.checkBoxDragChanged()
        else:
            pass
            #self.toLog(PyqtQevent.eventStr[event.type()])
        return QtGui.QWidget.eventFilter(self, source, event)
    def x2Scene (self, ix):
        """convert x to graphicsSecne coordinate

        Args:
        Returns:
        Raises:
        """
        return ix
    def pos2X (self, ipos):
        """convert stick position to X

        Args:
        Returns:
        Raises:
        """
        return ipos*self.posW+self.posW/2
    def pos2Scene (self, ipos):
        """convert stick position to graphicsSecne coordinate

        Args:
        Returns:
        Raises:
        """
        return self.x2Scene(self.pos2X(ipos))
    def scene2pos (self, ivalue):
        """convert graphicsSecne coordinate to stick position

        Args:
        Returns:
        Raises:
        """
        ftemp=ivalue/self.posW
        return round(ftemp)
    def y2Scene (self, iy):
        """convert y to graphicsSecne coordinate

        Args:
        Returns:
        Raises:
        """
        return (0-iy)
    def value2Y (self, ivalue):
        """convert stock value to y

        Args:
        Returns:
        Raises:
        """
        return ivalue
    def value2Scene (self, ivalue):
        """convert stock value to graphicsSecne coordinate

        Args:
        Returns:
        Raises:
        """
        return self.y2Scene(self.value2Y(ivalue))
    def scene2Value (self, ivalue):
        """convert graphicsSecne coordinate to stock value

        Args:
        Returns:
        Raises:
        """
        return (0.0-ivalue)
    def clearScene (self):
        """clear graphicsscene

        Args:
        Returns:
        Raises:
        """
        self.ui.graphicsView.scene().clear()
        self.scaleXOffset=0
    def toLog (self, istr):
        """write string to log window

        Args:
            istr- input string
        Returns:
        Raises:
        """
        self.ui.textBrowser.append(istr)
    def getRealViewRect (self):
        #lttemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect().topLeft())
        #rbtemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect().bottomRight())
        #self.realViewRect=QtCore.QRectF(lttemp.x(),lttemp.y(), rbtemp.x()-lttemp.x(), rbtemp.y()-lttemp.y())
        self.realViewRect=self.ui.graphicsView.rect()
        #self.realBarNum=self.realViewRect.width()/self.posW
        #temp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect())
        #ptemp=temp.value(0)
        #self.toLog("xxx {0:f}, {1:f}".format(ptemp.x(),ptemp.y()))
        #ptemp=temp.value(1)
        #self.toLog("xxx {0:f}, {1:f}".format(ptemp.x(),ptemp.y()))
        #ptemp=temp.value(2)
        #self.toLog("xxx {0:f}, {1:f}".format(ptemp.x(),ptemp.y()))
        #ptemp=temp.value(3)
        #self.toLog("xxx {0:f}, {1:f}".format(ptemp.x(),ptemp.y()))
    def setScene (self):
        viewVisibleBar=self.realViewRect.width()/self.posW
        datawidth=(len(self.data.sourceData))*self.posW
        #set scene
        self.sceneRect.setRight(datawidth)
        ltemp=datawidth-self.realViewRect.width()
        if ltemp<0:
            self.sceneRect.setLeft(ltemp)
        else:
            self.sceneRect.setLeft(-100)
        self.sceneRect.setTop(self.value2Scene(self.data.vmax))
        self.sceneRect.setBottom(self.value2Scene(self.data.vmin))
        self.ui.graphicsView.setSceneRect(self.sceneRect)
    def getViewRightPos (self):
        rbtemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect().bottomRight())
        return self.scene2pos(rbtemp.x())
    def setView (self, rpos=-1):
        """set viewport and scene

        Args:
        Returns:
        Raises:
        """
        try:
            #set view
            posr=rpos
            if posr==-1:
                posr=len(self.data.sourceData)
            realBarNum=self.realViewRect.width()/self.posW
            posl=posr-realBarNum
            if posl<0:
                posl=0
            btemp=self.data.getValueBoundaryForLastN(posr-posl, posl)
            if btemp==None:
                maxtemp=self.value2Scene(self.data.vmax)
                mintemp=self.value2Scene(self.data.vmin)
            else:
                maxtemp=self.value2Scene(btemp[DataAnalysis.boundaryMax])
                mintemp=self.value2Scene(btemp[DataAnalysis.boundaryMin])
            self.viewRect.setTop(maxtemp)
            self.viewRect.setBottom(mintemp)
            self.scaleYRation=(mintemp-maxtemp)/self.realViewRect.height()
            #self.toLog("max{0:.2f} min{1:.2f} hei{2:.2f} rat{3:.2f}".format(maxtemp, mintemp, self.realViewRect.height(), self.scaleYRation))
            self.viewRect.setRight(posr*self.posW)
            lptemp=posr*self.posW-(realBarNum+self.scaleXOffset)*self.posW
            self.viewRect.setLeft(lptemp)
            self.ui.graphicsView.fitInView(self.viewRect)
        except Exception as e:
            self.toLog(traceback.format_exc())

    def drawCandleStick (self):
        """draw candle stick on view

        Args:
        Returns:
        Raises:
        """
        try:
            if len(self.data.sourceData)==0:
                return
            for icount in range(len(self.data.sourceData)):
                iarray=self.data.sourceData[icount]
                istart=iarray[DataAnalysis.gfStart]
                ihigh=iarray[DataAnalysis.gfHigh]
                ilow=iarray[DataAnalysis.gfLow]
                iend=iarray[DataAnalysis.gfEnd]
                self.ui.graphicsView.scene().addLine(self.pos2Scene(icount),
                                                     self.value2Scene(ihigh),
                                                     self.pos2Scene(icount),
                                                     self.value2Scene(ilow))
                if istart<=iend:
                    brushtemp=QtGui.QBrush(QtGui.QColor(255,0,0))
                    self.ui.graphicsView.scene().addRect(self.pos2Scene(icount)-self.stickW/2,
                                                         self.value2Scene(iend),
                                                         self.stickW,
                                                         self.value2Scene(istart)-self.value2Scene(iend),
                                                         brush=brushtemp)
                else:
                    brushtemp=QtGui.QBrush(QtGui.QColor(0,255,0))
                    self.ui.graphicsView.scene().addRect(self.pos2Scene(icount)-self.stickW/2,
                                                         self.value2Scene(istart),
                                                         self.stickW,
                                                         self.value2Scene(iend)-self.value2Scene(istart),
                                                         brush=brushtemp)
        except Exception as e:
            self.toLog(traceback.format_exc())

    def final (self):
        pass
    def drawAssistData (self):
        """draw assistant line

        Args:
        Returns:
        Raises:
        """
        try:
            if len(self.data.drawDataArray)==0:
                return
            for icount in range(len(self.data.drawDataArray)):
                if self.data.drawDataArray[icount].enable==False:
                    continue
                if self.data.drawDataArray[icount].drawType==DrawData.dtypeLine:
                    lastLine=0
                    for jcount in range(len(self.data.drawDataArray[icount].data)):
                        iline=self.data.drawDataArray[icount][jcount]
                        if iline==None:
                            break
                        if iline!=0 and lastLine!=0:
                            #pentemp=QtGui.QPen(self.data.drawDataArray[icount].color)
                            #pentemp.setWidth(int(self.data.drawDataArray[icount].penW))
                            pentemp=QtGui.QPen(self.data.drawDataArray[icount].color,
                                               self.data.drawDataArray[icount].penW,
                                               QtCore.Qt.SolidLine,
                                               QtCore.Qt.RoundCap,
                                               QtCore.Qt.RoundJoin)
                            pentemp.setCosmetic(True)
                            if jcount!=0:
                                self.ui.graphicsView.scene().addLine(self.pos2Scene(jcount),
                                                                     self.value2Scene(iline),
                                                                     self.pos2Scene(jcount-1),
                                                                     self.value2Scene(lastLine),
                                                                     pen=pentemp)
                        #if "lastLine" in locals():
                        #    self.toLog("poa{0:d};{1:f};{2:f}".format(ipos,iline,lastLine))
                        #else:
                        #    self.toLog("pob{0:d};{1:f}".format(ipos,iline))
                        lastLine=iline
                if self.data.drawDataArray[icount].drawType==DrawData.dtypeDiff:
                    boundarytemp=len(self.data.drawDataArray[icount].data)
                    for jcount in range(boundarytemp):
                        if jcount==0:
                            continue
                        if jcount==boundarytemp-1:
                            continue
                        lastV=self.data.drawDataArray[icount].data[jcount-1]
                        curV=self.data.drawDataArray[icount].data[jcount]
                        if curV==0 and lastV==0:
                            continue
                        nextV=self.data.drawDataArray[icount].data[jcount+1]
                        htemp=abs(self.value2Scene(self.dotW*self.scaleYRation))
                        otemp=abs(self.value2Scene(self.dotW/2*self.scaleYRation))
                        if curV>lastV and curV>=nextV:
                            #self.toLog("{0:d}-big {1:.2f}".format(jcount,curV))
                            ihigh=self.data.sourceData[jcount][DataAnalysis.gfHigh]
                            brushtemp=QtGui.QBrush(QtGui.QColor(255,0,0))
                            self.ui.graphicsView.scene().addEllipse(self.pos2Scene(jcount)-self.dotW/2,
                                                                    self.value2Scene(ihigh)-htemp-otemp,
                                                                    self.dotW,
                                                                    htemp,
                                                                    brush=brushtemp)
                        if curV<lastV and curV<=nextV:
                            #self.toLog("{0:d}-small {1:.2f}".format(jcount,curV))
                            ilow=self.data.sourceData[jcount][DataAnalysis.gfLow]
                            brushtemp=QtGui.QBrush(QtGui.QColor(0,255,0))
                            self.ui.graphicsView.scene().addEllipse(self.pos2Scene(jcount)-self.dotW/2,
                                                                    self.value2Scene(ilow)+otemp,
                                                                    self.dotW,
                                                                    htemp,
                                                                    brush=brushtemp)
        except Exception as e:
            self.toLog(traceback.format_exc())
    def assistData (self):
        """setup assistant line data

        Args:
        Returns:
        Raises:
        """
        try:
            ####
            #self.data.addToDrawArray(self.data.calMA(10, color=QtCore.Qt.red))
            #self.data.addToDrawArray(self.data.calWMA(10, color=QtCore.Qt.green))
            #self.data.addToDrawArray(self.data.calEMA(10, color=QtCore.Qt.blue))
            #self.data.addToDrawArray(self.data.calHMA(10, color=QtCore.Qt.magenta))
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
            #self.data.addToDrawArray(matemp[2])
            #matemp=self.data.calKKMA(112,16,
            #                         color=QtCore.Qt.green,
            #                         penWidth=2)
            #self.data.addToDrawArray(matemp[0])
            #self.data.addToDrawArray(matemp[1])
            #self.data.addToDrawArray(matemp[2])
            #matemp=self.data.calKKMA(28,4,
            #                         color=QtCore.Qt.blue,
            #                         penWidth=2)
            #self.data.addToDrawArray(matemp[0])
            #self.data.addToDrawArray(matemp[1])
            #self.data.addToDrawArray(matemp[2])
            ####
            bantemp=self.data.calEmaBand(int(90*DataAnalysis.fibo), mul=DataAnalysis.fibo*12,
                                         midcolor=QtCore.Qt.darkGreen, outcolor=QtCore.Qt.darkMagenta,
                                         midpenWidth=0, outpenWidth=3)
            self.data.addToDrawArray(bantemp[0])
            self.data.addToDrawArray(bantemp[1])
            self.data.addToDrawArray(bantemp[2])
            bantemp=self.data.calEmaBand(int(30*DataAnalysis.fibo), mul=DataAnalysis.fibo*4,
                                         midcolor=QtCore.Qt.lightGray, outcolor=QtCore.Qt.magenta,
                                         midpenWidth=0, outpenWidth=3)
            self.data.addToDrawArray(bantemp[0])
            self.data.addToDrawArray(bantemp[1])
            self.data.addToDrawArray(bantemp[2])
            matemp=self.data.calKKMA(int(175*DataAnalysis.fibo),
                                     int(25*DataAnalysis.fibo),
                                     color=QtCore.Qt.red,
                                     penWidth=0)
            self.data.addToDrawArray(matemp[0])
            self.data.addToDrawArray(matemp[1])
            #matemp[2].enable=False
            #self.data.addToDrawArray(matemp[2])
            matemp=self.data.calKKMA(int(70*DataAnalysis.fibo),
                                     int(10*DataAnalysis.fibo),
                                     color=QtCore.Qt.green,
                                     penWidth=0)
            self.data.addToDrawArray(matemp[0])
            self.data.addToDrawArray(matemp[1])
            #matemp[2].enable=False
            #self.data.addToDrawArray(matemp[2])
            matemp=self.data.calKKMA(int(18*DataAnalysis.fibo),
                                     int(2*DataAnalysis.fibo),
                                     color=QtCore.Qt.blue,
                                     penWidth=0)
            self.data.addToDrawArray(matemp[0])
            self.data.addToDrawArray(matemp[1])
            self.data.addToDrawArray(matemp[2])
            ###
            
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

