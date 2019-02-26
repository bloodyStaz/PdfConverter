import sys
import os
import subprocess
import shutil
import ftplib
from PyQt5 import QtWidgets, QtCore
from functools import partial

class Popup(QtWidgets.QWidget):
    def __init__(self):
        super(Popup,self).__init__()
        self.setGeometry(250, 220, 300, 200)
        self.setWindowTitle("Remove File")

        
class FtpUploadTracker(QtWidgets.QWidget):
    sizeWritten = 0
    totalSize = 0
    lastShownPercent = 0

    def __init__(self, totalSize):
        super(FtpUploadTracker,self).__init__()
        self.setGeometry(250,220,300,200)
        self.setWindowTitle("Progress Box")
        
        self.totalSize = totalSize

    def handle(self, block):
        self.sizeWritten += 1024
        percentComplete = round((self.sizeWritten / self.totalSize) * 100)

        if (self.lastShownPercent != percentComplete):
            self.lastShownPercent = percentComplete
            print(str(percentComplete) + " percent Complete")
            
        

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 800, 640)
        self.setWindowTitle("Pdf Converter")
        QtWidgets.QApplication.setStyle("Fusion")
        qss = "style.txt"
        with open(qss, "r") as fh:
            self.setStyleSheet(fh.read())
        self.home()

    def home(self):
        # Delay Box
        self.delaytxtbox = QtWidgets.QLineEdit(self)
        self.delaytxtbox.setPlaceholderText("Delay Duration Max 30s")
        self.delaytxtbox.setMaximumSize(200, 50)
        # images check Box
        self.checkbox = QtWidgets.QCheckBox("Do you want to use images", self)

        # Logo Combo Box
        self.dropbox = QtWidgets.QComboBox(self)
        self.dropbox.addItem("Upload Logo")
        self.dropbox.addItem("Top Left")
        self.dropbox.addItem("Top Right")
        self.dropbox.addItem("Bottom Left")
        self.dropboxtext="Upload Logo"

        

        self.dropbox.activated[str].connect(self.onActivated)

        # Heading
        self.Label1 = QtWidgets.QLabel(self)
        self.Label1.setText("Pdf/Images Converter")
        self.Label1.setAlignment(QtCore.Qt.AlignCenter)
        # pdf or image
        # pdf or img txtbox
        self.txtBox1 = QtWidgets.QLineEdit(self)
        self.txtBox1.setMaximumHeight(36)
        self.txtBox1.setPlaceholderText("Enter File Path")
        # self.txtBox1.setFixedSize(800,30)
        # pdf or img filebox
        btn1 = QtWidgets.QPushButton("Browse File", self)
        btn1.clicked.connect(self.filePath)
        btn1.setToolTip('Select pdf or images')
        btn1.move(10, 0)
        btn1.setFixedSize(150, 50)

        # Video Path
        # Video Path Label
        self.txtBox2 = QtWidgets.QLineEdit(self)
        self.txtBox2.setMaximumHeight(36)
        self.txtBox2.setPlaceholderText("Enter Video Path")
        # self.txtBox2.setFixedSize(900,30)
        # pdf or img filebox
        btn2 = QtWidgets.QPushButton("Browse Path", self)
        btn2.clicked.connect(self.videoPath)
        btn2.setToolTip('Select Video Path')
        btn2.move(10, 0)
        btn2.setFixedSize(150, 50)

        # Video Name
        self.txtBox3 = QtWidgets.QLineEdit(self)
        self.txtBox3.setMaximumHeight(40)
        self.txtBox3.setPlaceholderText("Enter Video Name")
        # self.txtBox3.setFixedSize(800,30)
        # main Button
        btn3 = QtWidgets.QPushButton("Convert", self)
        btn3.clicked.connect(self.sProcess)
        btn3.setToolTip("Click to start the process")
        btn3.setFixedSize(150, 50)
        #Send to ftp button
        btn4=QtWidgets.QPushButton("Send to Ftp",self)
        btn4.clicked.connect(self.login)
        btn4.setToolTip("Click to send the video")
        btn4.setFixedSize(150,50)

        #Delete fild
        btn5=QtWidgets.QPushButton("Remove File",self)
        btn5.clicked.connect(self.DeleteFile)
        btn5.setToolTip("Click to Remove the File")
        btn5.setFixedSize(150,50)

        # main Layout of the windows adding widget
        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(10)
        hbox.addWidget(self.delaytxtbox)
        hbox.addWidget(self.checkbox)
        hbox.addWidget(self.dropbox)
        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(self.Label1)
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(self.txtBox1, 0)
        mainLayout.addWidget(btn1)

        mainLayout.addWidget(self.txtBox2)
        mainLayout.addWidget(btn2)

        mainLayout.addWidget(self.txtBox3)
        
        hbox2=QtWidgets.QHBoxLayout()
        
        hbox2.addWidget(btn3)

        hbox2.addWidget(btn4)
        hbox2.addWidget(btn5)
        hbox2.addStretch(0)
        mainLayout.addLayout(hbox2)

        mainLayout.addStretch(0)
        mainLayout.setSpacing(15)
        # mainLayout.setContentsMargins(0,0,0,0)

        self.setLayout(mainLayout)
        self.show()

    def DeleteFile(self):
        session=ftplib.FTP()
        sessionip="192.168.2.100"
        sessionhost=1026
        sessionuser="admin"
        sessionpwd="brandmefy"
        
        session.connect(sessionip,sessionhost)
        session.login(sessionuser,sessionpwd)
        print(session.getwelcome())
        print(session.pwd())

        
        files=session.nlst()
        self.w=Popup()
        i=0
        dic={}
        self.deletefileName=[]
        for i in files:
            
            dic[i]=QtWidgets.QCheckBox(i,self.w)
        print(dic)
        print(files)
        poplayout = QtWidgets.QVBoxLayout()
        for x,y in dic.items():
            y.stateChanged.connect(partial(self.clickBox,x))
        for i in dic.values():
            poplayout.addWidget(i)
        self.deletebtn=QtWidgets.QPushButton("Delete Files",self.w)
        self.deletebtn.clicked.connect(self.DeleteFiles)
        self.deletebtn.setToolTip("Click to Remove the File")
        self.deletebtn.setFixedSize(150,50)
        poplayout.addWidget(self.deletebtn)

        self.w.setLayout(poplayout)
        self.w.show()



        session.quit()
        
    def clickBox(self,x,state):
        if state ==QtCore.Qt.Checked:
            self.deletefileName.append(x)
        else:
            self.deletefileName.remove(x)
    def DeleteFiles(self):
        session=ftplib.FTP()
        sessionip="192.168.2.100"
        sessionhost=1026
        sessionuser="admin"
        sessionpwd="brandmefy"
        
        session.connect(sessionip,sessionhost)
        session.login(sessionuser,sessionpwd)
        for i in self.deletefileName:
            session.delete(i)
            print(i+" Delete Succesfully")
        self.DeleteFile()
        self.deletebtn.text="Delete Succesfully"
        session.quit()


            

    def onActivated(self, text):
        if text != "Upload Logo":
            self.logopath = QtWidgets.QFileDialog.getOpenFileNames(
                self, "Brows Logo")
            self.logopath = self.logopath[0]
            self.logopath = str(self.logopath[0])
        self.dropboxtext = text
        print(self.dropboxtext)

    def login(self):
        session=ftplib.FTP()
        sessionip="192.168.2.100"
        sessionhost=1026
        sessionuser="admin"
        sessionpwd="brandmefy"
        
        session.connect(sessionip,sessionhost)
        session.login(sessionuser,sessionpwd)
        print(session.getwelcome())
        print("opening file")
        print(self.videopath)
        file=open(self.videopath,"rb")
        totalSize = os.path.getsize(self.videopath)
        uploadTracker = FtpUploadTracker(int(totalSize))
        self.uploadlabel=QtWidgets.QLabel(uploadTracker)
        self.uploadlabel.text="0 Percent"
        uploadTracker.show()
        session.storbinary('STOR {}.mp4'.format(self.txtBox3.text()),file,1024,uploadTracker.handle)
        file.close()
        print(session.dir())
        uploadTracker.show()
        session.quit()
        



    def filePath(self):
        if(self.checkbox.isChecked()):
            self.filePath = QtWidgets.QFileDialog.getOpenFileNames(
                self, "Browse File")
            if self.filePath:
                self.filePath = self.filePath[0]
                self.txtBox1.setText(str(self.filePath))
        else:
            self.filePath = QtWidgets.QFileDialog.getOpenFileName(
                self, "Browse File")
            if self.filePath:
                self.filePath = self.filePath[0]
                self.txtBox1.setText(self.filePath)

            '''
            pdftoimg = "include/poppler/bin/pdftoppm.exe"
            pdf = '"{}"'.format(fileName)
            process = subprocess.Popen(
                '"%s" -png %s tmp/out' % (pdftoimg, pdf))
            process.wait()
            '''

    def videoPath(self):
        self.videoPath = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Video Path")
        self.txtBox2.setText(self.videoPath)

    def sProcess(self):
        if self.checkbox.isChecked():
            print("True")

        if(self.txtBox1.text()):
            
            if self.checkbox.isChecked():
                self.clean()
                self.imgConvert()
                self.vidConvert()
                self.clean()
            else:
                self.clean()
                self.pdfConvert()
                self.vidConvert()
                self.clean()

        else:
            self.txtBox1.setText = ""
            QtWidgets.QMessageBox.about(
                self, "Error", "Please select a file with pdf format")

    def clean(self):
        for f in os.listdir("tmp/"):
            os.remove("tmp/" + f)

    def imgConvert(self):
        j = 00
        for i in self.filePath:
            shutil.copyfile(i, "tmp/out-" + str(j) + ".png")
            j = j + 1

    def pdfConvert(self):

        pdfToImg = ("include/poppler/bin/pdftoppm.exe")
        pdf = '"{}"'.format(self.txtBox1.text())
        process = subprocess.Popen('"%s" -png %s tmp/out' % (pdfToImg, pdf))
        process.wait()
        return True

    def vidConvert(self):
        video = '"{}/{}.mp4"'.format(self.txtBox2.text(), self.txtBox3.text())
        res = "1920:1080"
        images = []
        if len(self.delaytxtbox.text()) > 0:
            delay = int(self.delaytxtbox.text())
        else:
            delay = 10

        framelength = delay + 1
        for img in os.listdir("tmp\\"):
            if img.endswith(".png"):
                images.append(img)
        loop = ""
        for f in images:
            imgPath = os.path.join("tmp\\", f)
            loop += "-loop 1 -t {} -i {} ".format(framelength, imgPath)

        effect = ""
        lst = "[v0]"
        for i in range(1, len(images)):
            lst += "[v{}]".format(i)
            effect += '[{0}:v]scale={1}:force_original_aspect_ratio=decrease,pad={1}:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=in:st=0:d=1,fade=t=out:st={2}:d=1[v{0}];'.format(
                i, res, delay)

        process = subprocess.Popen('include\\ffmpeg\\bin\\ffmpeg.exe -y  \
        {} \
        -filter_complex \
        "[0:v]scale={}:force_original_aspect_ratio=decrease,pad={}:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=out:st={}:d=1[v0]; \
        {} \
        {} \
        concat=n={}:v=1:a=0,format=yuv420p[v]" -map "[v]" {}'.format(loop, res, res, delay, effect, lst, len(images), "tmp/tmp1.mp4"))
        process.wait()

        process = subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i include/logo.png -filter_complex \
"overlay=W-w-5:H-h-5" \
-codec:a copy {}'.format("tmp/tmp1.mp4", "tmp/tmp2.mp4"))
        process.wait()

        if(self.dropboxtext !="Upload Logo"):
            if(self.dropboxtext=="Top Left"):
                print("adding top left logo")
                process=subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i {} -filter_complex \
                        "overlay=5:5" -codec:a copy {}'.format("tmp/tmp2.mp4",self.logopath,"tmp/tmp3.mp4"))
                process.wait()
            if(self.dropboxtext=="Top Right"):
                process=subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i {} -filter_complex \
                        "overlay=W-w-5:5" -codec:a copy {}'.format("tmp/tmp2.mp4",self.logopath,"tmp/tmp3.mp4"))
                process.wait()
            if(self.dropboxtext=="Bottom Left"):
                process=subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i {} -filter_complex \
                        "overlay=5:H-h-5" -codec:a copy {}'.format("tmp/tmp2.mp4",self.logopath,"tmp/tmp3.mp4"))
                process.wait()


            process = subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -c:v libx264 -profile:v high -vf scale=1920:1080 -r 25 {}'.format("tmp/tmp3.mp4", video))
            process.wait()

        else:
            print("in else condtion")
            process = subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -c:v libx264 -profile:v high -vf scale=1920:1080 -r 25 {}'.format("tmp/tmp2.mp4", video))
            process.wait()
        self.videopath = '{}/{}.mp4'.format(self.txtBox2.text(), self.txtBox3.text())
        



        


app = QtWidgets.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())
