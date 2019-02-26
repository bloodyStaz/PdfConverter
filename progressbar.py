import sys
import os
import subprocess
import shutil
import ftplib
from PyQt5 import QtWidgets, QtCore
from functools import partial


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 800, 640)
        self.setWindowTitle("Pdf Converter")
        QtWidgets.QApplication.setStyle("Fusion")
        btn1=QtWidgets.QPushButton("Click",self)
        btn1.clicked.connect(self.tmp)
        self.show()
    def tmp(self):
        session=ftplib.FTP()
        sessionip="192.168.2.100"
        sessionhost=1026
        sessionuser="admin"
        sessionpwd="brandmefy"
        
        session.connect(sessionip,sessionhost)
        session.login(sessionuser,sessionpwd)
        print(session.getwelcome())
        print("opening file")
        
        file=open("topleft.mp4","rb")
        totalSize = os.path.getsize("topleft.mp4")
        uploadTracker = FtpUploadTracker(int(totalSize))
        
        #session.storbinary('STOR {}.mp4'.format("topleft.mp4"),file,1024,uploadTracker.handle)
        file.close()
        print(session.dir())
        uploadTracker.show()
        session.quit()
        uploadTracker.show()
class FtpUploadTracker(QtWidgets.QWidget):
    sizeWritten = 0
    totalSize = 0
    lastShownPercent = 0

    def __init__(self, totalSize):
        super(FtpUploadTracker,self).__init__()
        self.setGeometry(250,220,300,200)
        self.setWindowTitle("Progress Box")
        self.lbl=QtWidgets.QLabel(self)
        self.lbl.setText("0 Percent")
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.lbl)
        btn1=QtWidgets.QPushButton("Click",self)
        self.setLayout(mainLayout)
        
        self.totalSize = totalSize
        self.show()

    def handle(self, block):
        self.sizeWritten += 1024
        percentComplete = round((self.sizeWritten / self.totalSize) * 100)

        if (self.lastShownPercent != percentComplete):
            self.lastShownPercent = percentComplete
            print(str(percentComplete) + " percent Complete")
        self.show()
session=ftplib.FTP()
app = QtWidgets.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())