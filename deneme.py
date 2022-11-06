import time
# import datetime
# from datetime import  date
from datetime import datetime,timedelta,date
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTime, QTimer
import sys




dict2={'task1': [{'study_time': '00:10:00', 'session_startTime': '10:00', 'session_endTime': '10:10', 'session_date': '2022-10-04', 'success': False}, {'study_time': '00:10:00', 'session_startTime': '17:34', 'session_date': '2022-11-06', 'session_endTime': '17:34', 'success': True}], 'task2': [{'study_time': '00:10:00', 'session_startTime': '10:00', 'session_endTime': '10:10', 'session_date': '2022-11-04', 'success': False}], 'task3': [{'study_time': '00:10:00', 'session_startTime': '17:34', 'session_date': '2022-11-05', 'session_endTime': '17:34', 'success': True}], 'task4': [{'study_time': '00:10:00', 'session_startTime': '17:42', 'session_date': '2022-11-06', 'session_endTime': '17:42', 'success': True}]}
# dict={}
# 
# text='0:00:00:00'
# total_time=datetime.strptime(text,"%H:%M:%S")
# print(type(total_time))
# print(total_time)
# a='00:10:00'
# b=datetime.strptime(a,"%H:%M:%S")
# c=b+total_time


a=0
for i in dict2.values():
	for j in i:
		(h, m, s) = j['study_time'].split(':')
		result = int(h) * 3600 + int(m) * 60 + int(s)
		a+=result
text2=time.strftime('%d day :%H:%M:%S', time.gmtime(a))
print(text2)
	
# text1=time.strftime('%M:%S', time.gmtime(250))
# print(text1)
# text2=time.strftime('%M:%S', time.gmtime(200))
# text1='00:00'
# text2='10:00'
# time1 = datetime.strptime(text1,"%M:%S")
# print(time1)
# time2 = datetime.strptime(text2,"%M:%S")
# b=time1+timedelta(seconds=10)
# print(b)
