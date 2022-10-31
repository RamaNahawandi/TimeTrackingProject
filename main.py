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
    user_id=""
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)
        with open('json.json', 'r') as f:
            self.users = json.load(f)
            self.user_names=self.users["userNames"]
            self.user_emails=self.users["userEmails"]
        self.errorTextLogin.setText('')
        self.errorTextSignUp.setText('')
        self.loginButton.clicked.connect(self.log_in)
        self.signUpButton.clicked.connect(self.sign_up)

    def log_in(self):
        self.user_id=self.emailInputLogin.text()
        LoginUI.user_id=self.user_id
        if self.user_id in self.user_names:
            self.go_main_menu()
        else:
            self.errorTextLogin.setText('Check your username or sign up please')
            
    def sign_up(self):
        self.user_id=self.nameInputSignUp.text()
        LoginUI.user_id=self.user_id
        if len(self.user_id)==0:
            self.errorTextSignUp.setText('Please write your name')
        elif self.user_id in self.user_names:
            self.errorTextSignUp.setText('This username is already exist')
            
        else:        
            self.user_email=self.emailInputSignUp.text()
            try:
                v = validate_email(self.user_email)
                self.user_email = v["email"] 
                if self.user_email in self.user_emails:
                    self.errorTextSignUp.setText('This username is already exist')
                else:                                
                    with open("json.json", "r+") as jsonFile:
                        data = json.load(jsonFile)   
                        data["userEmails"].append(self.user_email)
                        data["userNames"].append(self.user_id)
                        data["User"][self.user_id]={}
                        jsonFile.seek(0)  # rewind
                        json.dump(data, jsonFile)
                        jsonFile.truncate()                    
                    self.go_main_menu()                                    
            except EmailNotValidError :
                self.errorTextSignUp.setText('Check email please, that is not a valid email')
                       
    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

class MainMenuUI(QDialog):
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)
        self.user_id=LoginUI.user_id
        with open('json.json', 'r') as f:
            self.users = json.load(f)
            self.user_dict=self.users["User"][self.user_id]
        self.error_reciepts_email_label.setText('')
        self.error_project_label.setText('')
        self.error_subject_label.setText('')
        self.button_add_reciept.clicked.connect(self.add_reciept)
        self.list=[]
        
    def add_reciept(self):
        if 'Recipents' not in self.user_dict.keys():
            self.user_dict['Recipents']=[]            
        self.email=self.line_add_reciept.text()
        try:
            v = validate_email(self.email)
            self.email = v["email"] 
            if self.email in self.user_dict['Recipents']:
                self.error_reciepts_email_label.setText('This mail is already exist')
            else:
                self.list.append(self.email)
                self.error_reciepts_email_label.setText('')
                              
        except EmailNotValidError:
            self.error_reciepts_email_label.setText('Check email please, that is not a valid email')
    
       

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
