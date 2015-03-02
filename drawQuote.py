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

class DrawQuote(QtGui.QWidget):
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
        self.posW=10
        self.stickW=8
        ###scene rect
        self.sceneRect=QtCore.QRectF()
        self.sceneRect.setBottomRight(QtCore.QPointF(0,self.value2Scene(self.data.vmin)))
        self.sceneRect.setTopLeft(QtCore.QPointF(-100,self.value2Scene(self.data.vmax)))
        ###
        self.viewRect=QtCore.QRectF()
        self.viewRect.setBottomRight(QtCore.QPointF(0,self.value2Scene(self.data.vmin)))
        self.viewRect.setTopLeft(QtCore.QPointF(-100,self.value2Scene(self.data.vmax)))
        ###
        self.scaleXOffset=0


        self.resizeFlag=False   #resize event flag
        ####
        self.ui=uic.loadUi("quoteView.ui", self) #load ui
        self.ui.graphicsView.setScene(QtGui.QGraphicsScene(self)) #set scene
        self.ui.graphicsView.viewport().installEventFilter(self.ui)    #install event filter
        #self.ui.graphicsView.scene().addRect(-100,-20000,100,20000, brush=QtGui.QBrush(QtGui.QColor(255,0,0)))
        #self.ui.graphicsView.scene().addRect(-200,-40000,20,200, brush=QtGui.QBrush(QtGui.QColor(0,255,0)))
        #self.ui.graphicsView.scene().addRect(-300,-60000,20,200, brush=QtGui.QBrush(QtGui.QColor(0,0,255)))
        #self.ui.graphicsView.scene().addRect(-400,-80000,20,200, brush=QtGui.QBrush(QtGui.QColor(255,255,0)))
        #self.ui.graphicsView.scene().addRect(-500,-100000,20,200, brush=QtGui.QBrush(QtGui.QColor(0,255,255)))
        #pentemp=QtGui.QPen(QtCore.Qt.red,
        #                   3,
        #                   QtCore.Qt.SolidLine,
        #                   QtCore.Qt.RoundCap,
        #                   QtCore.Qt.RoundJoin)
        #self.ui.graphicsView.scene().addLine(-100,
        #                                     -30000,
        #                                     -200,
        #                                     -31000,
        #                                     pettemp)
        ###
        self.setViewScene()
        ###setup event
        self.ui.pushButtonLoad.clicked.connect(self.loadBtnClicked)
        self.ui.pushButtonClearLog.clicked.connect(self.clearBtnClicked)
        self.ui.pushButtonLeft.clicked.connect(self.leftBtnClicked)
        self.ui.pushButtonRight.clicked.connect(self.rightBtnClicked)
        self.ui.pushButtonZoomIn.clicked.connect(self.zoomInBtnClicked)
        self.ui.pushButtonZoomOut.clicked.connect(self.zoomOutBtnClicked)
        ###
        self.ui.show()
    def leftBtnClicked (self):
        """button left click handler

        Args:
        Returns:
        Raises:
        """
        pass
    def rightBtnClicked (self):
        """button right click handler

        Args:
        Returns:
        Raises:
        """
        pass
    def zoomInBtnClicked (self):
        """button zoom in click handler

        Args:
        Returns:
        Raises:
        """
        if self.scaleXOffset>0:
            self.scaleXOffset=0
        self.scaleXOffset=self.scaleXOffset-1
        self.setViewScene()
    def zoomOutBtnClicked(self):
        """button zoom out click handler

        Args:
        Returns:
        Raises:
        """
        if self.scaleXOffset<0:
            self.scaleXOffset=0
        self.scaleXOffset=self.scaleXOffset+1
        self.setViewScene()
        #recttemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect()).boundingRect()
        #self.toLog("viewRect:L:{0:d} R;{1:d} T:{2:d} B:{3:d}".format(int(recttemp.left()),
        #                                                             int(recttemp.right()),
        #                                                             int(recttemp.top()),
        #                                                             int(recttemp.bottom())))
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
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File", ".", "csv (*.csv)")
        if os.path.exists(fileName)==False:
            self.toLog(fileName+" doesn't exist")
            return
        self.data.clear()
        #load data from csv
        self.data.loadFromCSV(fileName)
        self.clearBtnClicked()
        self.clearScene()
        self.setViewScene()
        self.drawCandleStick()
        self.assistData()
        self.drawAssistData()
        self.toLog("Data length {0:d}".format(len(self.data.sourceData)))
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
                self.toLog("Left Button Press (%d, %d)"% (pos.x(), pos.y()))
            elif event.button() == QtCore.Qt.RightButton:
                self.toLog("right Button Press (%d, %d)"% (pos.x(), pos.y()))
            pos = QtCore.QPointF(self.ui.graphicsView.mapToScene(event.pos()))
            #self.toLog('mouse press at: (%d, %d, %d, %d)' % (pos.x(), pos.y(), event.pos().x(), event.pos().y()))
        elif (event.type() == QtCore.QEvent.Paint):
            if self.resizeFlag==True:
                self.resizeFlag=False
                self.setViewScene()
                self.repaint()
        elif (event.type() == QtCore.QEvent.Resize):
            self.resizeFlag=True
        elif (event.type() == QtCore.QEvent.MouseMove):
            pos = QtCore.QPointF(self.ui.graphicsView.mapToScene(event.pos()))
            #self.toLog("movse move (%f, %f)"% (self.scene2pos(pos.x()), self.scene2Value(pos.y())))
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
        return (0-ix)
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
        ftemp=((0.0-ivalue)-self.posW/2)/self.posW
        if ftemp<0:
            ftemp=0
        return math.ceil(ftemp)
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
        return ivalue*100
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
        return (0.0-ivalue)/100
    def repaint (self):
        """repaint graphicsscene

        Args:
        Returns:
        Raises:
        """
        pass
        #self.clearScene()
        #self.setViewScene()
    def clearScene (self):
        """clear graphicsscene

        Args:
        Returns:
        Raises:
        """
        self.ui.graphicsView.scene().clear()
    def toLog (self, istr):
        """write string to log window

        Args:
            istr- input string
        Returns:
        Raises:
        """
        self.ui.textBrowser.append(istr)
    def setViewScene (self):
        """set viewport and scene

        Args:
        Returns:
        Raises:
        """
        try:
            lttemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect().topLeft())
            rbtemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect().bottomRight())
            recttemp=QtCore.QRectF(lttemp.x(),lttemp.y(), rbtemp.x()-lttemp.x(), rbtemp.y()-lttemp.y())
            #recttemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect()).boundingRect()
            #self.toLog("viewRect0:L:{0:d} R;{1:d} T:{2:d} B:{3:d}".format(int(recttemp.left()),
            #                                                              int(recttemp.right()),
            #                                                              int(recttemp.top()),
            #                                                              int(recttemp.bottom())))
            datawidth=(len(self.data.sourceData)+1)*self.posW
            #set scene
            if datawidth>recttemp.width():
                wtemp=datawidth
            else:
                wtemp=recttemp.width()
            self.sceneRect.setLeft(0-wtemp)
            self.sceneRect.setRight(0)
            self.sceneRect.setTop(self.value2Scene(self.data.vmax))
            self.sceneRect.setBottom(self.value2Scene(self.data.vmin))
            self.ui.graphicsView.setSceneRect(self.sceneRect)
            #self.toLog("scene: {0:f} {1:f}".format(self.data.vmax, self.data.vmin))
            #set view
            #tltemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.rect().topLeft())
            #brtemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.rect().bottomRight())
            #tltemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().geometry()).boundingRect().topLeft()
            #brtemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().geometry()).boundingRect().bottomRight()
            #tltemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect().topLeft())
            #brtemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect().bottomRight())
            posl=self.scene2pos(recttemp.left())
            posr=self.scene2pos(recttemp.right())
            btemp=self.data.getValueBoundaryForLastN(posl-posr+1, posr)
            #self.toLog("pos: {0:d} {1:d}".format(posl, posr))
            if btemp==None:
                maxtemp=self.value2Scene(self.data.vmax)
                mintemp=self.value2Scene(self.data.vmin)
            else:
                maxtemp=self.value2Scene(btemp[DataAnalysis.boundaryMax])
                mintemp=self.value2Scene(btemp[DataAnalysis.boundaryMin])
                #self.toLog("bvalue: {0:f} {1:f}".format(btemp[DataAnalysis.boundaryMax], btemp[DataAnalysis.boundaryMin]))
            self.viewRect.setTop(maxtemp)
            self.viewRect.setBottom(mintemp)
            if (self.scaleXOffset*self.posW+recttemp.left()+2)<0:
                self.viewRect.setLeft((self.scaleXOffset*self.posW+recttemp.left()+2))
            else:
                self.viewRect.setLeft(recttemp.left()+2)
            self.viewRect.setRight(recttemp.right()-1)
            self.ui.graphicsView.fitInView(self.viewRect)
            #self.toLog("viewRect1:L:{0:d} R;{1:d} T:{2:d} B:{3:d}".format(int(recttemp.left()),
            #                                                              int(recttemp.right()),
            #                                                              int(recttemp.top()),
            #                                                              int(recttemp.bottom())))
            #self.toLog("view: {0:f} {1:f}".format(maxtemp, mintemp))
            ###save back real viewrect data
            #tltemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.rect().topLeft())
            #brtemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.rect().bottomRight())
            #self.toLog(" vr0:{0:10d}/{1:10d}/{2:10d}/{3:10d}".format(int(tltemp.y()),
            #                                                         int(brtemp.y()),
            #                                                         int(tltemp.x()),
            #                                                         int(brtemp.x())))
            #self.toLog("ivr0:L-{0:d} R-{1:d} T-{2:d} B-{3:d}".format(int(self.viewRect.left()),
            #                                                         int(self.viewRect.right()),
            #                                                         int(self.viewRect.top()),
            #                                                         int(self.viewRect.bottom())))
            #recttemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().geometry()).boundingRect()
            #self.viewRect.setTop(recttemp.top())
            #self.viewRect.setBottom(recttemp.bottom())
            #self.viewRect.setLeft(recttemp.left())
            #self.viewRect.setRight(recttemp.right())
            #self.ui.graphicsView.fitInView(self.viewRect)
            #self.toLog("ivr1:L-{0:d} R-{1:d} T-{2:d} B-{3:d}".format(int(self.viewRect.left()),
            #                                                         int(self.viewRect.right()),
            #                                                         int(self.viewRect.top()),
            #                                                         int(self.viewRect.bottom())))
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
                dataPos=icount
                iarray=self.data.souceDataStart(dataPos)
                istart=iarray[GFClass.gfStart]
                ihigh=iarray[GFClass.gfHigh]
                ilow=iarray[GFClass.gfLow]
                iend=iarray[GFClass.gfEnd]
                ipos=icount+1
                self.ui.graphicsView.scene().addLine(self.pos2Scene(ipos),
                                                     self.value2Scene(ihigh),
                                                     self.pos2Scene(ipos),
                                                     self.value2Scene(ilow))
                if istart<=iend:
                    brushtemp=QtGui.QBrush(QtGui.QColor(255,0,0))
                    self.ui.graphicsView.scene().addRect(self.pos2Scene(ipos)-self.stickW/2,
                                                         self.value2Scene(iend),
                                                         self.stickW,
                                                         self.value2Scene(istart)-self.value2Scene(iend),
                                                         brush=brushtemp)
                else:
                    brushtemp=QtGui.QBrush(QtGui.QColor(0,255,0))
                    self.ui.graphicsView.scene().addRect(self.pos2Scene(ipos)-self.stickW/2,
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
                    for jcount in range(len(self.data.drawDataArray[icount].data)):
                        dataPos=jcount
                        ipos=jcount+1
                        iline=self.data.drawDataArray[icount].drawDataStart(dataPos)
                        if iline==None:
                            break
                        if iline!=0:
                            #pentemp=QtGui.QPen(self.data.drawDataArray[icount].color)
                            #pentemp.setWidth(int(self.data.drawDataArray[icount].penW))
                            pentemp=QtGui.QPen(self.data.drawDataArray[icount].color,
                                               self.data.drawDataArray[icount].penW,
                                               QtCore.Qt.SolidLine,
                                               QtCore.Qt.RoundCap,
                                               QtCore.Qt.RoundJoin)
                            if jcount!=0:
                                self.ui.graphicsView.scene().addLine(self.pos2Scene(ipos),
                                                                     self.value2Scene(iline),
                                                                     self.pos2Scene(ipos-1),
                                                                     self.value2Scene(lastLine),
                                                                     pen=pentemp)
                        #if "lastLine" in locals():
                        #    self.toLog("poa{0:d};{1:f};{2:f}".format(ipos,iline,lastLine))
                        #else:
                        #    self.toLog("pob{0:d};{1:f}".format(ipos,iline))
                        lastLine=iline
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
                                         midpenWidth=0, outpenWidth=0)
            self.data.addToDrawArray(bantemp[0])
            self.data.addToDrawArray(bantemp[1])
            self.data.addToDrawArray(bantemp[2])
            bantemp=self.data.calEmaBand(int(30*DataAnalysis.fibo), mul=DataAnalysis.fibo*4,
                                         midcolor=QtCore.Qt.lightGray, outcolor=QtCore.Qt.magenta)
            self.data.addToDrawArray(bantemp[0])
            self.data.addToDrawArray(bantemp[1])
            self.data.addToDrawArray(bantemp[2])
            matemp=self.data.calKKMA(112,16,
                                     color=QtCore.Qt.green,
                                     penWidth=0)
            self.data.addToDrawArray(matemp[0])
            self.data.addToDrawArray(matemp[1])
            
            matemp=self.data.calKKMA(280,40,
                                     color=QtCore.Qt.red,
                                     penWidth=0)
            self.data.addToDrawArray(matemp[0])
            self.data.addToDrawArray(matemp[1])
            matemp=self.data.calKKMA(28,4,
                                     color=QtCore.Qt.blue,
                                     penWidth=0)
            self.data.addToDrawArray(matemp[0])
            self.data.addToDrawArray(matemp[1])
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

