import sys
from PyQt5 import QtWidgets,QtCore

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
        self.pdf.toggled.connect(lambda:self.optionState(self.images))
        self.pdf.toggled.connect(lambda:self.optionState(self.video))
        self.hLayout=QtWidgets.QHBoxLayout() #Setting Radio Layout
        self.hLayout.setSpacing(20)
        self.hLayout.addWidget(self.pdf)
        self.hLayout.addWidget(self.images)
        self.hLayout.addWidget(self.video)
        self.hLayout.addStretch()

        #Main Layout
        self.layout=QtWidgets.QGridLayout()
        self.layout.addWidget(self.heading,0,0)
        self.layout.addWidget(self.optionHeading,1,0)
        self.layout.addLayout(self.hLayout,2,0)
        
        

        vspacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding) 
        self.layout.addItem(vspacer)
        self.setLayout(self.layout)

        self.show()
    def optionState(self,option):
        if option.text()=="Pdf":
            if option.isChecked()==True:
                print(option.text())
        if option.text()=="images":
            if option.isChecked()==True:
                print(option.text())
        if option.text()=="Already have a video":
            if option.isChecked()==True:
                print(option.text())

app=QtWidgets.QApplication(sys.argv)
gui=Windows(1)
sys.exit(app.exec_())