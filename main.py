import time
import datetime
from datetime import date
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTime, QTimer
import sys
import json
from email_validator import validate_email, EmailNotValidError


from passlib.context import CryptContext
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication


#the 2 if are to solve the small ui problem
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


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
		self.loginPassword.setEchoMode(QtWidgets.QLineEdit.Password)
		self.signupPassword.setEchoMode(QtWidgets.QLineEdit.Password)
		self.signupPasswordconfirm.setEchoMode(QtWidgets.QLineEdit.Password)
		

	def log_in(self):
		context = CryptContext(
	schemes=["pbkdf2_sha256"],
	default="pbkdf2_sha256",
	pbkdf2_sha256__default_rounds=50000)

		self.user_id=self.emailInputLogin.text()
		self.user_password=self.loginPassword.text()
		LoginUI.user_id=self.user_id
		if self.user_id in self.user_names.keys():
			if context.verify(self.user_password, self.users["userNames"][self.user_id] ):
				self.go_main_menu()
			else:
				self.errorTextLogin.setText('Check your pasword please')
				
		else:
			self.errorTextLogin.setText('Check your username or sign up please')
			
	def sign_up(self):
		context = CryptContext(
	schemes=["pbkdf2_sha256"],
	default="pbkdf2_sha256",
	pbkdf2_sha256__default_rounds=50000)
		
		self.user_id=self.nameInputSignUp.text()
		self.user_password=self.signupPassword.text()
		self.user_confirm_password=self.signupPasswordconfirm.text()
		hashed_password=context.hash(self.user_confirm_password)
		
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
					self.errorTextSignUp.setText('This email is already exist')
				else:
					if len(self.user_password)==0:
						self.errorTextSignUp.setText('Please assign a password')
					else:  
						if context.verify(self.user_password,hashed_password):                               
							with open("json.json", "r+") as jsonFile:
								data = json.load(jsonFile)   
								data["userEmails"].append(self.user_email)
								data["userNames"][self.user_id]=hashed_password
								user_dict={"userName":self.user_id,"useremail":self.user_email,"Recipents":[self.user_email],"projects":{}}
								data["User"][self.user_id]=user_dict
								jsonFile.seek(0)  
								json.dump(data, jsonFile)
								jsonFile.truncate()
							LoginUI.user_id=self.user_id                    
							self.go_main_menu()
						else:
							self.errorTextSignUp.setText('Check password please they do not match')
															
			except EmailNotValidError :
				self.errorTextSignUp.setText('Check email please, that is not a valid email')
					   
	def go_main_menu(self):    
		main_menu = MainMenuUI()
		widget.addWidget(main_menu)
		widget.setCurrentIndex(widget.currentIndex()+1)

class MainMenuUI(QDialog):
	project=""
	subject=''
	
	def __init__(self):
		super(MainMenuUI,self).__init__()
		loadUi("./UI/mainMenu.ui",self)
		# widget.setWindowTitle(f'{LoginUI.user_id} Time Tracking App')
		self.user_id=LoginUI.user_id
		with open('json.json', 'r') as f:
			self.users = json.load(f)
			self.user_dict=self.users["User"][self.user_id]
		self.errorTextRecipientsEmailLabel.setText('')
		self.errorTextProjectLabel.setText('')
		self.errorTextSubjectLabel.setText('')
		self.addRecipientButton.clicked.connect(self.add_reciept)
		self.deleteRecipientButton.clicked.connect(self.delete_reciept)
		self.projectDeleteButton.clicked.connect(self.delete_project)
		self.addProjectButton.clicked.connect(self.add_project)
		self.addSubjectButton.clicked.connect(self.add_subject)
		self.button_start_pomodoro.clicked.connect(self.start_pomodoro)
		self.sellectProjectComboDeleteSubject.currentIndexChanged.connect(self.show_subject)
		self.combo_sellect_project.currentIndexChanged.connect(self.show_subject_pomodoro)
		self.showSummaryProjectCombo.currentIndexChanged.connect(self.show_subject_history)
		self.subjectDeleteButton_2.clicked.connect(self.delete_subject)
		self.combo_set()
		self.showSummaryButton.clicked.connect(self.show_summary)
		self.subject1={'task1':[{'date':"24-10-2022",'session_startTime':"10:00","session_endTime":'10:10','success':False},
                       {'date':"24-10-2022",'session_startTime':"10:00","session_endTime":'10:10','success':False},
                       {'date':"30-10-2022",'session_startTime':"10:30","session_endTime":'10:40','success':False},
                       {'date':"30-10-2022",'session_startTime':"11:40","session_endTime":'12:10','success':True}],
              		'task2':[{'date':"22-10-2022",'session_startTime':"09:00","session_endTime":'10:10','success':False},
                       {'date':"24-10-2022",'session_startTime':"10:00","session_endTime":'10:10','success':False},
                       {'date':"30-10-2022",'session_startTime':"10:00","session_endTime":'10:10','success':False},
                       {'date':"30-10-2022",'session_startTime':"10:40","session_endTime":'10:50','success':True}]}

	def show_summary(self):
		project = self.showSummaryProjectCombo.currentText()
		subject = self.showSummarySubjectCombo.currentText()
		period = self.showSummaryPeriodCombo.currentText()
		today = date.today()
		today_date=str(today)
		week_ago = today - datetime.timedelta(days=7)
		print(week_ago)

		print("Today date is: ", today_date)
		row=0
		dict={}
		if project=='All':
			for i,j in self.user_dict["projects"].items():
				for p in j.values():
					for l,m in p.items():
						dict[l]=m
		else:
			if subject=='All':
				for i in self.user_dict["projects"][project].values():
					for l,m in i.items():
						dict[l]=m
			else:
				dict=self.user_dict["projects"][project][subject]

		dict2={}
		if period=='Today':
			
			for i,j in dict.items():
				list=[]
				
				for k in j:	
					for l,m in k.items():
						if m==today_date:
							list.append(k)
				dict2[i]=list
          
		elif period=='This week':
			pass
        
				
			
		self.summaryTableValuesWidget.setRowCount(len(self.subject1.keys()))
		for i in self.subject1.keys():
			self.summaryTableValuesWidget.setItem(row,1,QtWidgets.QTableWidgetItem(i))
			row+=1

		


	
	def start_pomodoro(self):
		project=self.combo_sellect_project.currentText()
		subject=self.combo_sellect_subject.currentText()
		MainMenuUI.project=project
		MainMenuUI.subject=subject
		with open("json.json", "r+") as jsonFile:
			data = json.load(jsonFile)   
			data["User"][self.user_id]=self.user_dict
			jsonFile.seek(0)  
			json.dump(data, jsonFile)
			jsonFile.truncate()
		self.go_pomodoro()
  
	def go_pomodoro(self):
		main_menu = PomodoroUI()        
		widget.addWidget(main_menu)
		widget.setCurrentIndex(widget.currentIndex()+1)
		   
	def add_project(self):
		project=self.addProjectInput.text()
		if project in self.user_dict["projects"]:
			self.errorTextProjectLabel.setStyleSheet("color: rgb(255, 0, 0);")
			self.errorTextProjectLabel.setText('This project is already exist')
		else:
			self.errorTextProjectLabel.setStyleSheet("color: rgb(0, 255, 0);")
			self.errorTextProjectLabel.setText('This project is added')
			self.user_dict["projects"][project]={}
			self.projectDeleteCombo.addItem(project)    
			self.sellectProjectComboSubjectMenu.addItem(project)    
			self.combo_sellect_project.addItem(project)    
			self.sellectProjectComboDeleteSubject.addItem(project)    
			self.showSummaryProjectCombo.addItem(project)    

	def add_subject(self):
		project=self.sellectProjectComboSubjectMenu.currentText()
		subject=self.addSubjectInput.text()
		if subject in self.user_dict["projects"][project]:
			self.errorTextSubjectLabel.setStyleSheet("color: rgb(255, 0, 0);")
			self.errorTextSubjectLabel.setText('This subject is already exist')
			
		else:
			self.user_dict["projects"][project][subject]={}
			self.errorTextSubjectLabel.setStyleSheet("color: rgb(0, 255, 0);")
			self.errorTextSubjectLabel.setText('This subject is added')
			   
		
	def show_subject_history(self):
		content = self.showSummaryProjectCombo.currentText()
		self.showSummarySubjectCombo.clear()
		if len(content)>0:
			
			if content!="All":   
				for i in self.user_dict["projects"][content].keys():
					self.showSummarySubjectCombo.addItem(i)
				self.showSummarySubjectCombo.addItem("All")
			else:
				self.showSummarySubjectCombo.addItem("All")

			   
	def show_subject_pomodoro(self):
		content = self.combo_sellect_project.currentText()
		self.combo_sellect_subject.clear()
		if len(content)>0:    
			for i in self.user_dict["projects"][content].keys():
				self.combo_sellect_subject.addItem(i)
		
		
	def show_subject(self):
		content = self.sellectProjectComboDeleteSubject.currentText()
		self.subjectDeleteCombo.clear()
		if len(content)>0:    
			for i in self.user_dict["projects"][content].keys():
				self.subjectDeleteCombo.addItem(i)
	
	def combo_set(self):
		for i in self.user_dict['Recipents']:
			self.deleteRecipientCombo.addItem(i)
			
		for i in self.user_dict["projects"].keys():
			self.projectDeleteCombo.addItem(i)
			self.sellectProjectComboSubjectMenu.addItem(i)
			self.sellectProjectComboDeleteSubject.addItem(i)
			self.combo_sellect_project.addItem(i)
			self.showSummaryProjectCombo.addItem(i)
			
		self.showSummaryProjectCombo.addItem("All")
		self.showSummaryPeriodCombo.addItem("All")
		self.showSummaryPeriodCombo.addItem("Today")
		self.showSummaryPeriodCombo.addItem("This week")
			   
	def add_reciept(self):         
		self.email=self.addRecipientInput.text()
		try:
			v = validate_email(self.email)
			self.email = v["email"] 
			if self.email in self.user_dict['Recipents']:
				self.errorTextRecipientsEmailLabel.setStyleSheet("color: rgb(255, 0, 0);")
				self.errorTextRecipientsEmailLabel.setText('This mail is already exist')
				
			else:
				self.errorTextRecipientsEmailLabel.setStyleSheet("color: rgb(0, 255, 0);")
				self.errorTextRecipientsEmailLabel.setText('This mail is added')
				self.user_dict['Recipents'].append(self.email)
				self.deleteRecipientCombo.addItem(self.email)                                          
		except EmailNotValidError:
			self.errorTextRecipientsEmailLabel.setStyleSheet("color: rgb(255, 0, 0);")
			self.errorTextRecipientsEmailLabel.setText('Check email please, that is not a valid email')
			
	def delete_reciept(self):
		content = self.deleteRecipientCombo.currentText()
		index = self.deleteRecipientCombo.findText(content)
		self.user_dict['Recipents'].remove(content)
		self.deleteRecipientCombo.removeItem(index)
		
	def delete_project(self):
		content = self.projectDeleteCombo.currentText()
		index = self.projectDeleteCombo.findText(content)
		self.user_dict["projects"].pop(content)
		self.projectDeleteCombo.removeItem(index)
		self.sellectProjectComboSubjectMenu.removeItem(index)
		self.sellectProjectComboDeleteSubject.removeItem(index)
		self.combo_sellect_project.removeItem(index)
		index=self.showSummaryProjectCombo.findText(content)
		self.showSummaryProjectCombo.removeItem(index)
			
		
	def delete_subject(self):
		content1 = self.sellectProjectComboDeleteSubject.currentText()
		content=self.subjectDeleteCombo.currentText()
		index = self.subjectDeleteCombo.findText(content)
		self.user_dict["projects"][content1].pop(content)
		self.subjectDeleteCombo.removeItem(index)
		self.showSummarySubjectCombo.removeItem(index)
		self.combo_sellect_subject.removeItem(index)
		
class ShortBreakUI(QDialog):
	def __init__(self):
		super(ShortBreakUI,self).__init__()
		loadUi("./UI/shortBreak.ui",self)
		# widget.setWindowTitle(f'{LoginUI.user_id} Time Tracking App')
		self.count = 300
		self.component()
		self.skipButton.pressed.connect(self.skip)
		self.startButton.pressed.connect(self.start)
		self.goToMainMenuButton.clicked.connect(self.go_main_menu)
	
	def component(self):
		text=time.strftime('%M:%S', time.gmtime(self.count))
		self.timeLabel.display(text)
		self.flag = False
		self.timer = QTimer(self)
		self.timer.start(1000)
		self.timer.timeout.connect(self.showTime)
  
	def shadow_execute(self):
		self.shadow(self.skipButton)
		self.shadow(self.startButton)
		self.shadow(self.goToMainMenuButton)
		self.shadow(self.timeLabel)
  
	def showTime(self):
		if self.flag:
			self.count-= 1
		text=time.strftime('%M:%S', time.gmtime(self.count))
		self.timeLabel.display(text)
  
	def start(self):
		self.flag = True

	def shadow(self,widget):
		shadow = QGraphicsDropShadowEffect()
		shadow.setBlurRadius(15)
		widget.setGraphicsEffect(shadow)

	def skip(self):
		main_menu = PomodoroUI()
		widget.addWidget(main_menu)
		widget.setCurrentIndex(widget.currentIndex()+1)
  
	def go_main_menu(self):
		main_menu = MainMenuUI()
		widget.addWidget(main_menu)
		widget.setCurrentIndex(widget.currentIndex()+1)	
				 

class PomodoroUI(ShortBreakUI,QDialog):
	def __init__(self):
		super(PomodoroUI,self).__init__()
		loadUi("./UI/pomodoro.ui",self)
		# widget.setWindowTitle(f'{LoginUI.user_id} Time Tracking App')
		self.user_id=LoginUI.user_id
		self.project=MainMenuUI.project
		self.subject=MainMenuUI.subject
		self.count = 1500
		print('hello')
		self.shadow_execute()
		self.pauseButton.pressed.connect(self.pause)
		self.startButton.pressed.connect(self.start)
		self.goToMainMenuButton.clicked.connect(self.go_main_menu)
  
	def shadow_execute(self):
		self.shadow(self.startButton)
		self.shadow(self.goToMainMenuButton)
		self.shadow(self.timeLabel)
		self.shadow(self.pauseButton)
		self.shadow(self.doneButton)
		self.shadow(self.addTaskWidget)
		self.shadow(self.notFinishedButton)
		
	def pause(self):
		self.flag = False


class LongBreakUI(ShortBreakUI,QDialog):
	def __init__(self):
		super(LongBreakUI,self).__init__()
		loadUi("./UI/longBreak.ui",self)
		# widget.setWindowTitle(f'{LoginUI.user_id} Time Tracking App')
		self.count = 1800
		self.shadow_execute()
		self.skipButton.pressed.connect(self.skip)
		self.startButton.pressed.connect(self.start)
		self.goToMainMenuButton.clicked.connect(self.go_main_menu)


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
widget.setWindowTitle(f'{LoginUI.user_id} Time Tracking App')
widget.show()
sys.exit(app.exec_())
