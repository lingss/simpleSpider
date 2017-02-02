import smtplib
from email.mime.text import MIMEText
from email.header import Header


class MailFormat:
    sender = ''

    def __init__(self):
        self.server = smtplib.SMTP('', 25)
        self.server.starttls()
        self.server.set_debuglevel(1)
        self.server.login(self.sender, '')

    def setMessage(self, **msgcont):
        self.message = MIMEText(msgcont['cont'], msgcont['mimetype'], 'utf-8')
        self.message['From'] = self.sender
        self.message['Subject'] = msgcont['subject']

    def sendMessage(self, receivers):
        try:
            self.message['To'] = receivers
            self.server.sendmail(self.sender, receivers, self.message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as err:
            print("Error: 无法发送邮件", err)

