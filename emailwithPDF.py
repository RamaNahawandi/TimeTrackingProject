from email.mime.application import MIMEApplication
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
def send_email(self):
    with open("json.json", "r+") as jsonFile:
        data = json.load(jsonFile)
        receivers_list=data["User"][self.user_id]["Recipents"]

    email_sender = "pycodersfenyx@gmail.com"
    email_password = "rvpqrzownkvhyvqz"
    email_receiver =  receivers_list



    with open('pomodoroSummary.pdf' , "rb") as pdf:
        pdfAttachment = MIMEApplication(pdf.read(),_subtype="pdf")
        pdfAttachment.add_header('Content-Disposition','attachment',filename = ('utf-8', '', 'pomodoroSummary.pdf'))

        text = MIMEMultipart('alternative')
        text.attach(MIMEText("Some plain text", "plain", _charset="utf-8"))
        html = open("emailbody.html")
        text.attach(MIMEText(html.read(), 'html'))
    
    message = MIMEMultipart('mixed')
    message.attach(text)
    message.attach(pdfAttachment)
    message['Subject'] = 'Pomodoro Session Summary'
    #I dont know the use of these 3 lines to be honest
    # f = open("message.msg", "wb")
    # f.write(bytes(message.as_string(), 'utf-8'))
    # f.close()

    server = smtplib.SMTP('smtp.gmail.com', 587 )
    server.starttls()
    server.login(email_sender,email_password)
    server.sendmail(email_sender, email_receiver, message.as_string())
    server.quit()

    

