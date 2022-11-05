from email import encoders
from email.mime.base import MIMEBase
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_sender = "pycodersfenyx@gmail.com"
email_password = "rvpqrzownkvhyvqz"
email_receiver =  "rama_nahawandi@outlook.com"

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
