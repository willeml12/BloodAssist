from email.message import EmailMessage
import ssl
import smtplib


sender = "jeanpython6@gmail.com"
password = "gbfd vjme zsye uack"
receiver = "simon.francois0912@gmail.com"

subject = "test"
body = """ ceci est un testttt
"""


em = EmailMessage()
em['From'] = sender
em['To' ] = receiver
em['Subject'] = subject
em.set_content(body)
context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    smtp.login(sender,password)
    smtp.sendmail(sender, receiver,em.as_string())

