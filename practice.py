import sys
import PyQt4.QtCore
import PyQt4.QtGui
import PyQt4.uic
import PyqtQevent

class DrawQuote(PyQt4.QtGui.QWidget):
    """class to load ui
    """
    def __init__ (self):
        """constructor

        Args:
        Returns:
        Raises:
        """
        PyQt4.QtGui.QWidget.__init__(self)
        self.resizeFlag=False
        #load ui
        self.ui=PyQt4.uic.loadUi("quoteView.ui", self)
        self.ui.graphicsView.setScene(PyQt4.QtGui.QGraphicsScene(self))
        #self.ui.graphicsView.setSceneRect(PyQt4.QtCore.QRectF(self.ui.graphicsView.viewport().rect()))
        self.ui.graphicsView.setSceneRect(PyQt4.QtCore.QRectF(0,0,10,10))
        #self.ui.textBrowser.append("{0:s}".format(str(self.ui.graphicsView.rect())))
        self.ui.graphicsView.installEventFilter(self.ui)
        self.setCoordinate(PyQt4.QtCore.QEvent.Resize)
        self.ui.show()
    def viewX (self, ix):
        return self.zeroX-ix
    def viewY (self, iy):
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
        if ievent==PyQt4.QtCore.QEvent.Resize:
            self.zeroX=int(self.ui.graphicsView.rect().width()/2)
            self.zeroY=int(self.ui.graphicsView.rect().height()/2)
            self.vwidth=self.ui.graphicsView.rect().width()-10
            self.vheitht=self.ui.graphicsView.rect().height()-10
        else:
            self.zeroX=0-ix
            self.zeroY=0-iy
        try:
            self.ui.graphicsView.scene().removeItem(self.axisX)
            self.ui.graphicsView.scene().removeItem(self.axisY)
            self.ui.graphicsView.scene().removeItem(self.rect)
        except AttributeError:
            pass
        #self.ui.textBrowser.append("position:{0:f}:{1:f}".format(self.zeroX, self.zeroY))
        self.axisX=self.ui.graphicsView.scene().addLine(self.viewX(0),self.viewY(0),self.viewX(50),self.viewY(0))
        self.axisY=self.ui.graphicsView.scene().addLine(self.viewX(0),self.viewY(0),self.viewX(0),self.viewY(50))
        #self.rect=self.ui.graphicsView.scene().addRect(self.viewX(self.vwidth),self.viewY(self.vheitht),self.vwidth,self.vheitht)
    def eventFilter(self, source, event):
        """event filter function

        Args:
            source- source object
            event- event
        Returns:
        Raises:
        """
        #self.ui.textBrowser.append(PyqtQevent.eventStr[event.type()])
        if (event.type() == PyQt4.QtCore.QEvent.MouseButtonPress):
            pos = PyQt4.QtCore.QPointF(self.ui.graphicsView.mapToScene(event.pos()))
            self.ui.textBrowser.append('mouse press at: (%d, %d)' % (pos.x(), pos.y()))
            #self.ui.textBrowser.append('mouse press at: (%d, %d)' % (event.pos().x(), event.pos().y()))
            try:
                self.ui.graphicsView.scene().removeItem(self.lastrect)
            except AttributeError:
                pass
            self.lastrect=self.ui.graphicsView.scene().addRect(pos.x(),pos.y(),10, 10)
        elif (event.type() == PyQt4.QtCore.QEvent.Paint):
            if self.resizeFlag==True:
                self.resizeFlag=False
                self.ui.textBrowser.append("Resize paint")
                self.setCoordinate(PyQt4.QtCore.QEvent.Resize)
        elif (event.type() == PyQt4.QtCore.QEvent.Resize):
            self.resizeFlag=True
        return PyQt4.QtGui.QWidget.eventFilter(self, source, event)
    def final (self):
        pass

if __name__ == "__main__":
    try:
        app = PyQt4.QtGui.QApplication(sys.argv)
        mainui=DrawQuote()
        app.exec_()
    finally:
        if "mainui" in locals():
            mainui.final()

