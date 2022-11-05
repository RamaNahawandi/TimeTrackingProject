from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_sender = "pycodersfenyx@gmail.com"
email_password = "rvpqrzownkvhyvqz"
email_receiver =  "rama_nahawandi@outlook.com"


pdf= './pomodoroSummary.pdf' 
pdfAttachment = MIMEApplication(pdf, _subtype = "pdf")
pdfAttachment.add_header('content-disposition', 'attachment', filename = ('utf-8', '', 'pomodoroSummary.pdf'))
text = MIMEMultipart('alternative')
text.attach(MIMEText("Some plain text", "plain", _charset="utf-8"))
html = open("design.html")
text.attach(MIMEText(html.read(), 'html'))
 

message = MIMEMultipart('mixed')
message.attach(text)
message.attach(pdfAttachment)
message['Subject'] = 'Subject Subject Subject'
f = open("message.msg", "wb")
f.write(bytes(message.as_string(), 'utf-8'))
f.close()


server = smtplib.SMTP('smtp.gmail.com', 587 )
server.starttls()
server.login(email_sender,email_password)
server.sendmail(email_sender, email_receiver, message.as_string())
server.quit()

 

