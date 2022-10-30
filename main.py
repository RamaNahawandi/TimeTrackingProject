from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys
import json
from email_validator import validate_email, EmailNotValidError


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)
        self.list=['sefasahan35@gmail.com']
        self.errorTextLogin.setText('')
        self.errorTextSignUp.setText('')

        # This is example of changing screen
        self.loginButton.clicked.connect(self.log_in)
        self.signUpButton.clicked.connect(self.sign_up)


    def log_in(self):
        self.email=self.emailInputLogin.text()
        if self.email in self.list:
            self.go_main_menu()
        else:
            self.errorTextLogin.setText('Check your email adress or sign up please')
            
    def sign_up(self):
        self.name=self.nameInputSignUp.text()
        self.email=self.emailInputSignUp.text()
        try:
            v = validate_email(self.email)
            self.email = v["email"] 
            if self.email in self.list:
                self.errorTextSignUp.setText('This mail is already exist')
            else:
                self.list.append(self.email)
                self.go_main_menu()
                
        except EmailNotValidError as e:
            self.errorTextSignUp.setText('Check email please, that is not a valid email')
           
            
    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class MainMenuUI(QDialog):
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)

class PomodoroUI(QDialog):
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("./UI/shortBreak.ui",self)

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("./UI/longBreak.ui",self)


app = QApplication(sys.argv)
UI = LoginUI() # This line determines which screen you will load at first

# You can also try one of other screens to see them.
    # UI = MainMenuUI()
    # UI = PomodoroUI()
    # UI = ShortBreakUI()
    # UI = LongBreakUI()
# this block is for make a pup.up message   
# self.messagebox=QtWidgets.QMessageBox()
# self.messagebox.setText(f"Check your email adress or sign up please")
# self.messagebox.setWindowTitle('log in problem')
# self.messagebox.exec_()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.setWindowTitle("Time Tracking App")
widget.show()
sys.exit(app.exec_())
