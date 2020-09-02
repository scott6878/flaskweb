import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

import os

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('indiflex1@gmail.com', os.environ['GMAIL_PASSWD'])

msg = MIMEMultipart()
msg['Subject'] = 'Test Title'
content = MIMEText('SMTP로 메일 보내기 본문 메시지입니다.')
msg.attach(content)

filepath = "./indiflex.png"
with open(filepath, 'rb') as f:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(f.read())  
    encoders.encode_base64(part) 
    part.add_header('Content-Disposition', 'attachment', filename=filepath)
    msg.attach(part)

addr = "jeonseongho@naver.com"
msg["To"] = addr
smtp.sendmail("indiflex1@gmail.com", addr, msg.as_string())

smtp.quit()
