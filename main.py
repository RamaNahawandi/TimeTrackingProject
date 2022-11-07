import time
from datetime import datetime,timedelta,date
from PyQt5 import QtWidgets,QtCore,QtGui,QtPrintSupport
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTime, QTimer
import sys
import json
from email_validator import validate_email, EmailNotValidError
from passlib.context import CryptContext
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication



from emailwithPDF import send_email



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
		self.shadow_execute()

	def shadow_execute(self):
		self.shadow(self.signUpWidget)
		self.shadow(self.titleWidget)
		self.shadow(self.loginWidget)
		self.shadow(self.signUpButton)
		self.shadow(self.loginButton)
		self.shadow(self.image)
	
	def shadow(self,widget):
		shadow = QGraphicsDropShadowEffect()
		shadow.setBlurRadius(15)
		widget.setGraphicsEffect(shadow)	

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
		widget.setWindowTitle(f'{LoginUI.user_id} Time Tracking App')
		self.user_id=LoginUI.user_id
		self.summaryTableValuesWidget.setColumnWidth(0,123)
		self.summaryTableValuesWidget.setColumnWidth(1,150)
		self.summaryTableValuesWidget.setColumnWidth(2,90)
		self.summaryTableValuesWidget.setColumnWidth(3,90)
		self.summaryTableValuesWidget.setColumnWidth(4,90)
		self.summaryTableValuesWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section{"
            "border-bottom: 1px solid #4a4848;"
            "background-color:rgb(0, 255, 255);"
        "}")
		# self.summaryTableValuesWidget.setCornerButtonEnabled(True)
		self.summaryTableValuesWidget.setStyleSheet(" QTableCornerButton::section {"
    "background: rgb(0, 255, 255);"
    "border: 2px outset red;"
"}")
		self.summaryTableValuesWidget.verticalHeader().setStyleSheet(
      
            "QHeaderView::section{"
            "border-bottom: 1px solid #4a4848;"
            "background-color:rgb(0, 255, 255);"
        "}")
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
		self.sendEmailThisSummaryButton.clicked.connect(self.create_sendemail)
		self.subject1={}
		self.history_dict={}
  
	def print_widget(self):
		printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
		printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
		printer.setOutputFileName('history.pdf')
		painter = QtGui.QPainter(printer)
		xscale = printer.pageRect().width() * 1.0 / self.summaryTableValuesWidget.width()
		yscale = printer.pageRect().height() * 1.0 / self.summaryTableValuesWidget.height()
		scale = min(xscale, yscale)
		painter.translate(printer.paperRect().center())
		painter.scale(scale, scale)
		painter.translate(-self.summaryTableValuesWidget.width() / 2, -self.summaryTableValuesWidget.height() / 2)
		self.summaryTableValuesWidget.render(painter)
		painter.end()
  
	def create_sendemail(self):
		self.summaryTableValuesWidget.resize(579,1200)
		self.print_widget()

		send_email(self)

	def show_summary(self):
		project = self.showSummaryProjectCombo.currentText()
		subject = self.showSummarySubjectCombo.currentText()
		period = self.showSummaryPeriodCombo.currentText()
		today = date.today()
		today_date=str(today)
		week=datetime.strftime(today-timedelta(days=7),"%Y-%m-%d")
		week_ago=datetime.strptime(week, '%Y-%m-%d').date()
		text="00:10"
		self.total_time= datetime.strptime(text,"%M:%S")
	
		dict={}
		if project=='All':	
			for i,j in self.user_dict["projects"].items():
				for p in j.values():
					for k,l in p.items():
						dict[k]=l
					
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
			for i,j in dict.items():
				list=[]
				
				for k in j:	
					for l,m in k.items():
						if l=="session_date":
							date_time_obj = datetime.strptime(m, '%Y-%m-%d').date()
							if week_ago<date_time_obj<=today:
								list.append(k)
				dict2[i]=list
		
		else:
			dict2=dict
		a=0
		for i in dict2.values():
			for j in i:
				(h, m, s) = j['study_time'].split(':')
				result = int(h) * 3600 + int(m) * 60 + int(s)
				a+=result
		self.total_time=time.strftime('%H:%M:%S', time.gmtime(a))
		self.totalTrackedTimeTextLabel.setText(self.total_time)
        
		row=0				
		for i,j in dict2.items():
			for k in j:
					self.summaryTableValuesWidget.setItem(row,0,QtWidgets.QTableWidgetItem(str(k['session_date'])))
					self.summaryTableValuesWidget.setItem(row,1,QtWidgets.QTableWidgetItem(i))
					self.summaryTableValuesWidget.setItem(row,2,QtWidgets.QTableWidgetItem(k['session_startTime']))
					self.summaryTableValuesWidget.setItem(row,3,QtWidgets.QTableWidgetItem(k['session_endTime']))
					if k['success']:
						self.summaryTableValuesWidget.setItem(row,4,QtWidgets.QTableWidgetItem('True'))
					else:
						self.summaryTableValuesWidget.setItem(row,4,QtWidgets.QTableWidgetItem('False'))
					row+=1

	def start_pomodoro(self):
		project=self.combo_sellect_project.currentText()
		subject=self.combo_sellect_subject.currentText()
		MainMenuUI.project=project
		MainMenuUI.subject=subject
		self.go_pomodoro()
	
	def load_json(self):
		with open("json.json", "r+") as jsonFile:
			data = json.load(jsonFile)   
			data["User"][self.user_id]=self.user_dict
			jsonFile.seek(0)  
			json.dump(data, jsonFile)
			jsonFile.truncate()
  
	def go_pomodoro(self):
		main_menu = PomodoroUI()        
		widget.addWidget(main_menu)
		widget.setCurrentIndex(widget.currentIndex()+1)
		   
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
			self.load_json()

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
			if project==self.combo_sellect_project.currentText():
				self.combo_sellect_subject.addItem(subject)
			if project==self.sellectProjectComboDeleteSubject.currentText():
				self.subjectDeleteCombo.addItem(subject)
			if project==self.showSummaryProjectCombo.currentText():
				self.showSummarySubjectCombo.addItem(subject)
			self.load_json()
			   			   
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
				self.load_json()
		except EmailNotValidError:
			self.errorTextRecipientsEmailLabel.setStyleSheet("color: rgb(255, 0, 0);")
			self.errorTextRecipientsEmailLabel.setText('Check email please, that is not a valid email')
			
	def delete_reciept(self):
		content = self.deleteRecipientCombo.currentText()
		index = self.deleteRecipientCombo.findText(content)
		self.user_dict['Recipents'].remove(content)
		self.deleteRecipientCombo.removeItem(index)
		self.load_json()
		
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
		self.load_json()
		
	def delete_subject(self):
		content1 = self.sellectProjectComboDeleteSubject.currentText()
		content=self.subjectDeleteCombo.currentText()
		index = self.subjectDeleteCombo.findText(content)
		self.user_dict["projects"][content1].pop(content)
		self.subjectDeleteCombo.removeItem(index)
		self.showSummarySubjectCombo.removeItem(index)
		self.combo_sellect_subject.removeItem(index)
		self.load_json()

class ShortBreakUI(QDialog):
	def __init__(self):
		super(ShortBreakUI,self).__init__()
		loadUi("./UI/shortBreak.ui",self)
		widget.setWindowTitle(f'{LoginUI.user_id} Time Tracking App')
		self.count = 300
		self.component()
		self.check=0
		self.startButton.setText('Pause')
		self.skipButton.pressed.connect(self.skip)
		self.startButton.pressed.connect(self.start)
		self.goToMainMenuButton.clicked.connect(self.go_main_menu)
		self.shadow_execute()
	
	def component(self):
		text=time.strftime('%M:%S', time.gmtime(self.count))
		self.timeLabel.display(text)
		self.flag = True
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
		self.check +=1
		if self.check % 2!=0:
			self.flag= False
			self.startButton.setText('Start')
		else:
			self.flag= True
			self.startButton.setText('Pause')

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
	session_number=1
	def __init__(self):
		super(PomodoroUI,self).__init__()
		loadUi("./UI/pomodoro.ui",self)
		widget.setWindowTitle(f'{LoginUI.user_id} Time Tracking App')
		self.user_id=LoginUI.user_id
		self.project=MainMenuUI.project
		self.subject=MainMenuUI.subject
		with open('json.json', 'r') as jsonFile:
			data = json.load(jsonFile)
			self.task_dict=data["User"][self.user_id]["projects"][self.project][self.subject]
		self.flag = False
		self.taskComboEdit()
		self.session_date=''
		self.session_startTime=''	
		self.count = 1500
		self.shadow_pomodoro_execute()
		self.addTask.clicked.connect(self.addingTask)
		self.pauseButton.pressed.connect(self.Pomodoropause)
		self.startButton.pressed.connect(self.Pomodorostart)
		self.doneButton.clicked.connect(self.done)
		self.notFinishedButton.clicked.connect(self.notFinished)
		self.goToMainMenuButton.clicked.connect(self.go_main_menu)
		self.control_time=1500
		self.numberOfSession.setText(str(PomodoroUI.session_number))
		self.tableWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section{"
            "border-bottom: 1px solid #4a4848;"
            "background-color:rgb(203, 34, 79);"
        "}")
		self.tableWidget.verticalHeader().setStyleSheet(
            "QHeaderView::section{"
            "border-bottom: 1px solid #4a4848;"
            "background-color:rgb(203, 34, 79);"
        "}")
		self.tableWidget.setColumnWidth(0,150)
		self.tableWidget.setColumnWidth(1,70)
		self.tableWidget.setLineWidth(70)

	def taskComboEdit(self):
		list=[]
		row=0
		self.tasksCombo.clear()
		for i in self.task_dict:
			row+=1
			if len(self.task_dict[i])>0:
				for j in self.task_dict[i]:
					for k,l in j.items():
						if k=='success':
							if l==True:
								if i in list:
									list.remove(i)
							else:
									if i not in list:										
										list.append(i)							
			else:
				if i not in list:
					list.append(i)
	
		for i in list:
			self.tasksCombo.addItem(i)
		row=0
		self.tableWidget.setRowCount(len(self.task_dict.keys()))
		for i,j in self.task_dict.items():
			self.tableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(i))
			if len(j)==0:
				self.tableWidget.setItem(row,1,QtWidgets.QTableWidgetItem("False"))	
			else:	
				for k in j:
					for l,m in k.items():
						if l=='success':
							self.tableWidget.setItem(row,1,QtWidgets.QTableWidgetItem(str(m)))
			row+=1


	def showTime(self):
		if self.flag:
			self.count-= 1
		text=time.strftime('%M:%S', time.gmtime(self.count))
		self.timeLabel.display(text)
		if self.count==0:
			self.flag=False
			self.count=5
			self.notFinished()
			if PomodoroUI.session_number==4:
				PomodoroUI.session_number=1
				main_menu = LongBreakUI()
				widget.addWidget(main_menu)
				widget.setCurrentIndex(widget.currentIndex()+1)
			else:
				PomodoroUI.session_number+=1
				main_menu = ShortBreakUI()
				widget.addWidget(main_menu)
				widget.setCurrentIndex(widget.currentIndex()+1)	

	def addingTask(self):
		task_input = self.taskInput.text()
		if task_input in self.task_dict:
			self.taskMessage.setStyleSheet("color: rgb(255, 0, 0);")
			if len(self.task_dict[task_input])>0:
				for i in self.task_dict[task_input]:
					for k,l in i.items():
						if k=='success':
							if l==True:
								self.taskMessage.setText('This task already completed, choose another task')
							else:			
								self.taskMessage.setText('This task already exists')
			else:
				self.taskMessage.setText('This task already exists')
		else:
			self.tasksCombo.addItem(task_input)
			with open("json.json", "r+") as jsonFile:
				data = json.load(jsonFile)
				self.task_dict[task_input]=[]
				data["User"][self.user_id]["projects"][self.project][self.subject]=self.task_dict
				jsonFile.seek(0)  
				json.dump(data, jsonFile)
				jsonFile.truncate()
			self.taskMessage.setStyleSheet("color: rgb(0, 255, 0);")
			self.taskMessage.setText('This task is added')
		self.taskComboEdit()

	def done(self):		
		self.flag = False	
		with open("json.json", "r+") as jsonFile:
				data = json.load(jsonFile)
				self.task_input=self.tasksCombo.currentText()
				current_time = time.strftime("%H:%M", time.localtime())
				text1=time.strftime('%M:%S', time.gmtime(self.control_time))
				text2=time.strftime('%M:%S', time.gmtime(self.count))
				self.control_time-=self.control_time-self.count
				time1 = datetime.strptime(text1,"%M:%S")
				time2 = datetime.strptime(text2,"%M:%S")
				study_time=time1-time2
				session_dict= {"session_date":self.session_date,"session_startTime":self.session_startTime,"session_endTime":current_time,"study_time":str(study_time), "success": True}
				task_list=data["User"][self.user_id]["projects"][self.project][self.subject][self.task_input]
				task_list.append(session_dict)
				self.task_dict[self.task_input].append(session_dict)
				data["User"][self.user_id]["projects"][self.project][self.subject][self.task_input]=task_list
				jsonFile.seek(0)  
				json.dump(data, jsonFile)
				jsonFile.truncate()		
		self.taskMessage.setStyleSheet("color: rgb(0, 255, 0);")
		self.taskMessage.setText('task marked as Done')
		index = self.tasksCombo.findText(self.task_input)
		self.tasksCombo.removeItem(index) 
		self.messagebox=QtWidgets.QMessageBox()
		self.messagebox.setText(f"Choose another task please")
		self.messagebox.setWindowTitle('Task done')
		self.messagebox.exec_()
		self.taskComboEdit()

	def notFinished(self):
		self.flag = False
		with open("json.json", "r+") as jsonFile:
			data = json.load(jsonFile)
			self.task_input=self.tasksCombo.currentText()
			current_time = time.strftime("%H:%M", time.localtime())
			text1=time.strftime('%M:%S', time.gmtime(self.control_time))
			text2=time.strftime('%M:%S', time.gmtime(self.count))
			self.control_time-=self.control_time-self.count
			time1 = datetime.strptime(text1,"%M:%S")
			time2 = datetime.strptime(text2,"%M:%S")
			study_time=time1-time2
			session_dict= {"session_date":self.session_date,"session_startTime":self.session_startTime,"session_endTime":current_time,"study_time":str(study_time), "success": False}
			task_list=data["User"][self.user_id]["projects"][self.project][self.subject][self.task_input]
			task_list.append(session_dict)
			self.task_dict[self.task_input].append(session_dict)
			data["User"][self.user_id]["projects"][self.project][self.subject][self.task_input]=task_list
			jsonFile.seek(0)  
			json.dump(data, jsonFile)
			jsonFile.truncate()		
		self.taskMessage.setStyleSheet("color: rgb(0, 0, 0);")
		self.taskMessage.setText('task marked as Not done')
		self.taskComboEdit()
	
	def shadow_pomodoro_execute(self):
		self.shadow(self.startButton)
		self.shadow(self.goToMainMenuButton)
		self.shadow(self.timeLabel)
		self.shadow(self.pauseButton)
		self.shadow(self.doneButton)
		self.shadow(self.addTaskWidget)
		self.shadow(self.notFinishedButton)
		self.shadow(self.tableWidget)
		
	def Pomodoropause(self):
		self.flag = False

	def Pomodorostart(self):
		self.flag = True
		if len(self.session_startTime)==0:
			self.session_startTime = time.strftime("%H:%M", time.localtime())
			self.session_date = date.today().strftime("%Y-%m-%d")

class LongBreakUI(ShortBreakUI,QDialog):
	def __init__(self):
		super(LongBreakUI,self).__init__()
		loadUi("./UI/longBreak.ui",self)
		widget.setWindowTitle(f'{LoginUI.user_id} Time Tracking App')
		self.startButton.setText('Pause')
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
widget.setWindowIcon(QtGui.QIcon("UI/images/pomodoroIcon.png"))
widget.show()
sys.exit(app.exec_())
