from random import randint
import smtplib
class MailInterface:
    host = "smtp.gmail.com"
    who = "andrijlupov@gmail.com" # TODO: ВСТАВЬ СЮДА СВОЙ EMAIL СУКА!
    def __init__(self):
        self.smtp = smtplib.SMTP_SSL(self.host, 465)
        self.smtp.login(self.who, "postgres")
    def SendCode(self, email: str) -> int:
        i = randint(100000, 999999)
        Body = f"From: {self.who}\r\nTo: {email}\r\nSubject: Code confirmation\r\n\r\nPlease, send this code to our site: {i}\r\n"
        print(self.smtp.sendmail(self.who, email, Body))
        return i
    def Close(self):
        self.smtp.quit()