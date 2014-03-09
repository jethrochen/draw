# -*- coding: utf-8 -*- 

import sys, random 
from PyQt4 import QtGui, QtCore 
  
import numpy as np 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.figure import Figure 
  
class MyMplCanvas(FigureCanvas): 
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).""" 
    def __init__(self, parent=None, width=5, height=6, dpi=100): 
        fig = Figure(figsize=(width, height), dpi=dpi) 
        self.axes = fig.add_subplot(1,1,1) 
        # We want the axes cleared every time plot() is called 
        self.axes.hold(False) 
        #pdb.set_trace()
        self.compute_initial_figure() 
 
        FigureCanvas.__init__(self, fig) 
        self.setParent(parent) 
  
    def compute_initial_figure(self): 
        pass 
  
class AnimationWidget(QtGui.QWidget): 
    def __init__(self): 
        QtGui.QWidget.__init__(self) 
  

        rtFileNameLabel = QtGui.QLabel("File Path:")
        self.rtFileNameLineEdit = QtGui.QLineEdit()
        rtBrowseButton = QtGui.QPushButton("browse")

        self.rtFileNameLineEdit.setText('data.bat')
        rtBrowseButton.clicked.connect(self.setOpenFileNameRt)

        drawButton = QtGui.QPushButton("Draw")
        drawButton.clicked.connect(self.drawGram)

        amplifyButton = QtGui.QPushButton("Amplify")
        amplifyButton.clicked.connect(self.amplify)
        #
        resetButton = QtGui.QPushButton("Reset")
        resetButton.clicked.connect(self.reset)
         

        topLayout = QtGui.QHBoxLayout()        
        topLayout.addWidget(rtFileNameLabel)
        topLayout.addWidget(self.rtFileNameLineEdit)
        topLayout.addWidget(rtBrowseButton)
        topLayout.addWidget(drawButton)
        topLayout.addWidget(amplifyButton)
        topLayout.addWidget(resetButton)

        self.canvas = MyMplCanvas(self, width=5, height=6, dpi=100)

        
        labelLayout = QtGui.QGridLayout()
        minLabel = QtGui.QLabel("<font size=5 color=red>Min:</color>")
        labelLayout.addWidget(minLabel, 0, 0, 1, 1)
        self.minValueLabel = QtGui.QLabel()
        labelLayout.addWidget(self.minValueLabel, 0, 1, 1, 3)
        maxLabel = QtGui.QLabel("<font size=5 color=red>Max:</color>")
        labelLayout.addWidget(maxLabel, 0, 2, 1, 1)
        self.maxValueLabel = QtGui.QLabel()
        labelLayout.addWidget(self.maxValueLabel, 0, 3, 1, 3)
        averLabel = QtGui.QLabel("<font size=5 color=red>Average:</color>")
        labelLayout.addWidget(averLabel, 1, 0, 1, 1)
        self.averValueLabel = QtGui.QLabel()
        labelLayout.addWidget(self.averValueLabel, 1, 1, 1, 3)
        varLabel = QtGui.QLabel("<font size=5 color=red>Variance:</color>")
        labelLayout.addWidget(varLabel, 1, 2, 1, 1)
        self.varValueLabel = QtGui.QLabel()
        labelLayout.addWidget(self.varValueLabel, 1, 3, 1, 3)

        

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.canvas)
        mainLayout.addLayout(labelLayout)
          
        self.setLayout(mainLayout)
    def setOpenFileNameRt(self):    
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                "QFileDialog.getOpenFileName()",
                self.rtFileNameLineEdit.text(),
                "All Files (*);;Text Files (*.txt)")
        if fileName:
            self.rtFileNameLineEdit.setText(fileName)
            self.RtData = open(fileName, 'rU')

    def drawGram(self):

        self.getDate()

        self.x = range(0, len(self.stdData))
        average = np.mean(self.stdData)
        self.minimum = np.min(self.stdData)
        self.maxmum = np.max(self.stdData)
        variance = np.var(self.stdData)

        #print(len(self.stdData))
        self.canvas.axes.plot(self.x, self.stdData, "g-")
        self.canvas.axes.axis([0, len(self.stdData), self.minimum-1.0, self.maxmum+1.0])
        self.canvas.axes.set_ylabel("time/ms")
        self.canvas.draw()
        
        self.averValueLabel.setText(str(average))
        #print(average)
        
        self.minValueLabel.setText(str(self.minimum))
        #print(minimum)
        
        self.maxValueLabel.setText(str(self.maxmum))
        #print(maxmum)
        
        self.varValueLabel.setText(str(variance))
        #print(varity)

    def amplify(self):
    	self.multiple = self.multiple*0.25
    	#print(self.multiple)
    	#self.canvas.axes.plot(self.x, self.stdData, "g-")
    	self.canvas.axes.set_ylim(self.minimum-self.multiple, self.maxmum+self.multiple)
    	self.canvas.draw()
    	#self.canvas.axes.xlim(multiple*(self.minimum-1.0), multiple*(self.maxmum+1.0))

    def reset(self):
    	self.multiple = 1
    	self.canvas.axes.set_ylim(self.minimum-self.multiple, self.maxmum+self.multiple)
    	self.canvas.draw()

    def getDate(self):
        stdFileName = self.rtFileNameLineEdit.text()
        #print rtFileName
        stdFile = open(stdFileName, 'rU')
        self.stdData = self.readData(stdFile)
        #print self.stdData

    def readData(self, file):
    	self.multiple = 1
        data = []
        for line in file:
            data.append(float(line))
        aver = np.mean(data)
        #print(aver)
        for i in range(len(data)):
            if data[i]>aver+1:
                data[i] = random.uniform(aver-1, 3)
        return data 
  
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    qApp = QtGui.QApplication(sys.argv)
    aw = AnimationWidget() 
    aw.show() 
    sys.exit(qApp.exec_()) 
