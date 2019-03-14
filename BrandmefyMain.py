import sys
from PyQt5 import QtWidgets,QtCore
from BrandmefyUpload import MyThread,ProgressThread
import ftplib

class Windows(QtWidgets.QWidget):
    def __init__(self,state):
        super(Windows,self).__init__()
        self.resize(800,640)
        self.setWindowTitle("Brandmefy")
        QtWidgets.QApplication.setStyle("Fusion")
        styleSheet="include/BrandmefyStyleSheet.txt"
        with open(styleSheet, "r") as fh:
            self.setStyleSheet(fh.read())
        self.state=state
        self.fileOptionState=1
        self.logoPath=""
        self.logoTxt="Upload Logo"

        #main heading
        self.heading=QtWidgets.QLabel(self)
        self.heading.setObjectName("heading")
        if self.state==1:
            self.heading.setText("Brandmefy Admin Panel")
        if self.state==2:
            self.heading.setText("Brandmefy")
        self.heading.setAlignment(QtCore.Qt.AlignCenter)

        #Videos Option
        self.optionHeading=QtWidgets.QLabel(self)
        self.optionHeading.setText("Create video from?")
        self.optionHeading.setObjectName("subHeading")
        self.pdf=QtWidgets.QRadioButton("Pdf",self) #Creating Radio Buttons
        self.pdf.setChecked(True)
        self.images=QtWidgets.QRadioButton("images",self) 
        self.video=QtWidgets.QRadioButton("Already have a video",self)
        self.pdf.toggled.connect(lambda:self.optionState(self.pdf)) #Calling function on Radio toggle
        self.images.toggled.connect(lambda:self.optionState(self.images))
        self.video.toggled.connect(lambda:self.optionState(self.video))
        self.optionLayout=QtWidgets.QHBoxLayout() #Setting Radio Layout
        self.optionLayout.setSpacing(20)
        self.optionLayout.addWidget(self.pdf)
        self.optionLayout.addWidget(self.images)
        self.optionLayout.addWidget(self.video)
        self.optionLayout.addStretch()

        #Browse Grid
        self.browseLabel=QtWidgets.QLabel("Select input file for video",self)
        self.browseLabel.setObjectName("subHeading")
        self.browsePath=QtWidgets.QLineEdit(self)
        self.browsePath.setFixedWidth(600)
        self.browseLabel.setObjectName("browsePath")
        self.browsePath.setPlaceholderText("File Path")
        self.browseBtn=QtWidgets.QPushButton("Browse",self)
        self.browseBtn.clicked.connect(lambda:self.browseFile())
        self.browseBtn.setObjectName("browseBtn")
        self.browseLayout=QtWidgets.QHBoxLayout()
        self.browseLayout.setSpacing(20)
        self.browseLayout.addWidget(self.browsePath)
        self.browseLayout.addWidget(self.browseBtn)
        self.browseLayout.addStretch()

        #Delay box
        self.delayTxtBox=QtWidgets.QLineEdit(self)
        self.delayTxtBox.setFixedWidth(150)
        self.delayTxtBox.setPlaceholderText("Set delay max 30 sec")
        self.delayTxtBox.hide()
        self.delayLabel=QtWidgets.QLabel("Do you want to add custom add",self)
        self.delayLabel.setObjectName("subHeading")
        self.delayGrpBox = QtWidgets.QGroupBox()
        self.delayGrpBox.setObjectName("grpBox")
        self.delayYes = QtWidgets.QRadioButton("Yes")
        self.delayYes.toggled.connect(lambda:self.delayState(self.delayYes))
        self.delayYes.setObjectName("radiobtn")
        self.delayNo = QtWidgets.QRadioButton("No")
        self.delayNo.toggled.connect(lambda:self.delayState(self.delayNo))
        self.delayNo.setChecked(True)
        self.delayNo.setObjectName("radiobtn")
        vbox = QtWidgets.QHBoxLayout()
        vbox.setSpacing(20)
        vbox.addWidget(self.delayYes)
        vbox.addWidget(self.delayNo)
        vbox.addStretch()
        vbox.setContentsMargins(0, 0, 0, 0)
        self.delayGrpBox.setLayout(vbox)

        #Logo Box
        self.logoDropBox = QtWidgets.QComboBox(self)
        self.logoDropBox.addItem("Upload Logo")
        self.logoDropBox.addItem("Top Left")
        self.logoDropBox.addItem("Top Right")
        self.logoDropBox.addItem("Bottom Left")
        self.logoDropBox.setFixedWidth(150)
        self.logoDropBox.activated[str].connect(self.uploadLogo)
        

        self.logoLabel=QtWidgets.QLabel("Do you want to add logo")
        self.logoLabel.setObjectName("subHeading")

        self.logoGrpBox=QtWidgets.QGroupBox()
        self.logoGrpBox.setObjectName("grpBox")

        self.logoYes=QtWidgets.QRadioButton("Yes")
        self.logoYes.toggled.connect(lambda:self.logoState(self.logoYes))
        self.logoNo=QtWidgets.QRadioButton("No")
        
        self.logoNo.toggled.connect(lambda:self.logoState(self.logoNo))
        self.logoNo.setChecked(True)
        
        self.logoHBox=QtWidgets.QHBoxLayout()
        self.logoHBox.setSpacing(20)
        self.logoHBox.addWidget(self.logoYes)
        self.logoHBox.addWidget(self.logoNo)
        self.logoHBox.addStretch()
        self.logoHBox.setContentsMargins(0,0,0,0)
        self.logoGrpBox.setLayout(self.logoHBox)

        self.previewBtn=QtWidgets.QPushButton("Preview")
        self.previewBtn.setObjectName("browseBtn")
        self.previewBtn.clicked.connect(lambda:self.startConversion())
        self.previewBtn.setFixedWidth(103)


        #Ftp Options
        self.uploadLabel=QtWidgets.QLabel("Upload To System?")
        self.uploadLabel.setObjectName("subHeading")
        self.deleteLabel=QtWidgets.QLabel("Delete existing video")
        self.deleteLabel.setObjectName("subHeading")
        self.systemHBox=QtWidgets.QHBoxLayout()
        self.systemHBox.setSpacing(470)
        self.systemHBox.addWidget(self.uploadLabel)
        self.systemHBox.addWidget(self.deleteLabel)
        self.systemHBox.addStretch()
        self.systemHBox.setContentsMargins(0,0,0,0)

        self.uploadBtn=QtWidgets.QPushButton("Upload")
        self.uploadBtn.clicked.connect(lambda:self.login())
        self.uploadBtn.setObjectName("browseBtn")
        self.deleteBtn=QtWidgets.QPushButton("List videos")
        self.deleteBtn.setObjectName("browseBtn")
        self.systemBtnHBox=QtWidgets.QHBoxLayout()
        self.systemBtnHBox.setSpacing(515)
        self.systemBtnHBox.addWidget(self.uploadBtn)
        self.systemBtnHBox.addWidget(self.deleteBtn)
        self.systemBtnHBox.addStretch()
        self.systemBtnHBox.setContentsMargins(0,0,0,0)

        self.progressLabel=QtWidgets.QLabel(self)
        self.progressLabel.setObjectName("subHeading")
        #Main Layout
        self.layout=QtWidgets.QGridLayout()
        self.layout.addWidget(self.heading,0,0)
        self.layout.addWidget(self.optionHeading,1,0)
        self.layout.addLayout(self.optionLayout,2,0)
        self.layout.addWidget(self.browseLabel,3,0)
        self.layout.addLayout(self.browseLayout,4,0)
        self.layout.addWidget(self.delayLabel,5,0)
        self.layout.addWidget(self.delayGrpBox,6,0)
        self.layout.addWidget(self.delayTxtBox,7,0)
        self.layout.addWidget(self.logoLabel,8,0)
        self.layout.addWidget(self.logoGrpBox,9,0)
        self.layout.addWidget(self.logoDropBox,10,0)
        self.layout.addWidget(self.previewBtn,11,0)
        self.layout.addLayout(self.systemHBox,12,0)
        self.layout.addLayout(self.systemBtnHBox,13,0)
        self.layout.addWidget(self.progressLabel,14,0)
        self.layout.setVerticalSpacing(10)
        
        

        vspacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding) 
        self.layout.addItem(vspacer)
        self.setLayout(self.layout)

        self.show()
    def optionState(self,option):
        if option.text()=="Pdf":
            if option.isChecked()==True:
                self.browseLabel.setText("Select input file for video")
                self.fileOptionState=1
        elif option.text()=="images":
            if option.isChecked()==True:
                self.browseLabel.setText("Select input file for video")
                self.fileOptionState=2
        elif option.text()=="Already have a video":
            if option.isChecked()==True:
                self.browseLabel.setText("Select video file for input")
                self.fileOptionState=3
    def delayState(self,option):
        if option.text()=="Yes":
            if option.isChecked()==True:
                self.delayTxtBox.show()
        if option.text()=="No":
            if option.isChecked()==True:
                self.delayTxtBox.hide()
    def logoState(self,option):
        if option.text()=="Yes":
            if option.isChecked()==True:
                self.logoDropBox.show()
        if option.text()=="No":
            if option.isChecked()==True:
                self.logoDropBox.hide()
    def uploadLogo(self,text):
        filter="image (*.img *.jpg)"
        if len(text)>1 and text!="Upload Logo":
            self.logoTxt=text
            self.logoPath=QtWidgets.QFileDialog.getOpenFileName(self,"Browse logo",None,filter)
            if self.logoPath:
                self.logoPath=self.logoPath[0]
                
            
    def browseFile(self):
        if self.fileOptionState==1:
            filter = "pdf (*.pdf)"
            self.filePath=QtWidgets.QFileDialog.getOpenFileName(self,"Browse Pdf",None,filter)
            if self.filePath:
                self.filePath=self.filePath[0]
                self.browsePath.setText(self.filePath)
        elif self.fileOptionState==2:
            filter = "images (*.jpg *png)"
            self.filePath=QtWidgets.QFileDialog.getOpenFileNames(self,"Browse images",None,filter)
            if self.filePath:
                self.filePath=self.filePath[0]
                self.browsePath.setText(str(self.filePath))
        elif self.fileOptionState==3:
            filter = "videos (*.mp4)"
            self.filePath=QtWidgets.QFileDialog.getOpenFileNames(self,"Browse Mp4",None,filter)
            if self.filePath:
                self.filePath=self.filePath[0]
                self.browsePath.setText(str(self.filePath))
    def startConversion(self):
        QtWidgets.QPushButton.setDisabled(self,True)
        if len(self.delayTxtBox.text())>0:
            self.thread=MyThread(self.fileOptionState,self.filePath,self.logoTxt,self.logoPath,int(self.delayTxtBox.text()))
        else:
            self.thread=MyThread(self.fileOptionState,self.filePath,self.logoTxt,self.logoPath)
        self.thread.signal.connect(self.progress)
        self.thread.start()
        self.progressThread=ProgressThread()
        self.progressThread.progressSignal.connect(self.progressBar)
        self.progressThread.start()
        
    def progress(self,val):
        self.progressStatus=val
    def progressBar(self,val):
        if self.progressStatus!="Done":
            self.progressLabel.setText(val)
        else:
            QtWidgets.QPushButton.setEnabled(self,True)
            self.progressLabel.setText("Done")
            self.progressThread.terminate()

    def uploadTracker(self,block):
        
        
        self.sizeWritten += 1024
        percentComplete = round((self.sizeWritten / self.totalSize) * 100)


        if (self.lastShownPercent != percentComplete):
            self.lastShownPercent = percentComplete

            self.progresslbl.setText(str(percentComplete) + " percent Complete")
            QtWidgets.QApplication.processEvents()
            print(str(percentComplete) + " percent Complete")
            if percentComplete == 100 :
                self.progresslbl.setText(str(percentComplete) + " percent Complete \n Your file was send succesfully.")



    def login(self):
        
        try:
            session=ftplib.FTP()
            sessionip="192.168.2.100"
            sessionhost=1026
            sessionuser="admin"
            sessionpwd="brandmefy"
            
            session.connect(sessionip,sessionhost)
            session.login(sessionuser,sessionpwd)
        except:
            print("Failed to connect please try again later")
            return None
        print(session.getwelcome())
        print("opening file")
        #print(self.videopath)
        #self.videopath
        self.sizeWritten=0
        self.lastShownPercent=0
        file=open(self.videopath,"rb")
        self.totalSize = os.path.getsize(self.videopath)

        #self.txtBox3.text()
        session.storbinary('STOR {}.mp4'.format(self.txtBox3.text()),file,1024,self.uploadTracker)
        file.close()
        print(session.dir())
        session.quit()
        
                    
        

app=QtWidgets.QApplication(sys.argv)
gui=Windows(1)
sys.exit(app.exec_())