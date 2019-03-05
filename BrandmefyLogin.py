from PyQt5 import QtWidgets ,QtCore,QtGui
import sys
#Login Panel
class LoginPanel(QtWidgets.QWidget):
    def __init__(self):
        super(LoginPanel,self).__init__()
        self.resize(400,350)
        self.setWindowTitle("Login Panel")
        QtWidgets.QApplication.setStyle("Fusion")

        styleSheet="include/BrandmefyStyleSheet.txt"
        with open(styleSheet, "r") as fh:
            self.setStyleSheet(fh.read())

        self.loginHeading=QtWidgets.QLabel(self)
        self.loginHeading.setObjectName("loginHeading")
        self.loginHeading.setText("Brandmefy")
        self.loginHeading.setAlignment(QtCore.Qt.AlignCenter)

        #UserName
        self.userHeadgin=QtWidgets.QLabel(self)
        self.userHeadgin.setObjectName("loginTxt")
        self.userHeadgin.setText("UserName")
        #UserName Text Box
        self.userNameTxtBox=QtWidgets.QLineEdit(self)
        self.userNameTxtBox.setObjectName("loginTxtBox")

        #Password
        self.passwordHeading=QtWidgets.QLabel(self)
        self.passwordHeading.setObjectName("loginTxt")
        self.passwordHeading.setText("Password")
        #PassWord Text Box
        self.passwordTxtBox=QtWidgets.QLineEdit(self)
        self.passwordTxtBox.setObjectName("loginTxtBox")

        #Login Button
        self.loginBtn=QtWidgets.QPushButton(self)
        self.loginBtn.clicked.connect(self.loginCheck)
        self.loginBtn.setObjectName("loginBtn")
        self.loginBtn.setText("Login")
        
        #Setting the Layout
        self.loginLayout=QtWidgets.QGridLayout()
        self.loginLayout.addWidget(self.loginHeading,0,0)
        self.loginLayout.addWidget(self.userHeadgin,1,0)
        self.loginLayout.addWidget(self.userNameTxtBox,2,0)
        self.loginLayout.addWidget(self.passwordHeading,3,0)
        self.loginLayout.addWidget(self.passwordTxtBox,4,0)
        self.loginLayout.addWidget(self.loginBtn,5,0,1,0)
        vspacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding) 

        self.loginLayout.addItem(vspacer)
        self.setLayout(self.loginLayout)
        self.show()

    #Login Function
    def loginCheck(self):
        userName=self.userNameTxtBox.text()
        passWord=self.passwordTxtBox.text()
        if(userName.lower()=="admin" and passWord=="123"):
            print("admin")
        elif(userName=="user" and passWord=="123"):
            print("user")
        else:
            self.userNameTxtBox.setText("")
            self.userNameTxtBox.setPlaceholderText("Incorrect Username")
            self.passwordTxtBox.setText("")
            self.passwordTxtBox.setPlaceholderText("Incorrect Password")

app=QtWidgets.QApplication(sys.argv)
Gui=LoginPanel()
sys.exit(app.exec_())
