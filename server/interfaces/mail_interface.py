from random import randint
import smtplib


class MailInterface:
    host = "smtp.gmail.com"
    who = "andrijlupov@gmail.com"

    def __init__(self):
        self.smtp = smtplib.SMTP_SSL(self.host, 465)
        self.smtp.login(self.who, "postgres")

    def send_code(self, email: str) -> int:
        i = randint(100000, 999999)
        Body = f"From: {self.who}\r\nTo: {email}\r\nSubject: Code confirmation\r\n\r\nPlease, send this code to our site: {i}\r\n"
        print(self.smtp.sendmail(self.who, email, Body))
        return i

    def close(self):
        self.smtp.quit()