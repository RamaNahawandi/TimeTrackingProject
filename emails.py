from email import encoders
from email.mime.base import MIMEBase
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#I need to make it a function and pass self parameter here, so insstead of RIMA i can pass self.user_id 
with open("json.json", "r+") as jsonFile:
    data = json.load(jsonFile)
    receivers_list=data["User"]["rima"]["Recipents"]



email_sender = "pycodersfenyx@gmail.com"
email_password = "rvpqrzownkvhyvqz"
email_receiver =  receivers_list
msg = MIMEMultipart()
msg['From'] = email_sender
msg['To'] = email_receiver

html = open("design.html")
msg = MIMEText(html.read(), 'html')
msg['Subject'] = 'Pomodoro Session Summary'


server = smtplib.SMTP('smtp.gmail.com', 587 )
server.starttls()
server.login(email_sender,email_password)
server.sendmail(email_sender, email_receiver, msg.as_string())
server.quit()
