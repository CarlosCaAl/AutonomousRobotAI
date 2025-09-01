from Thread import Runner
from System import read

import smtplib as smtp
from colorama import Fore
import time

class Mail(Runner):
    def __init__(self):
        super(Mail,self).__init__(None)
    def init(self):
        try:
            self.addr,self.port,route = 'smtp.gmail.com',587,"data.json"
            data = read(route)
            self.Pass = data["pass"]
            self.mail = data["mail"]
            self.recv = data["recv"]
            self.server = smtp.SMTP(self.addr,self.port)
            self.server.starttls()
            self.server.login(self.mail,self.Pass)
        except Exception as e: 
            print(Fore.MAGENTA+"ERROR: "+Fore.WHITE+"Mail not authentified correctly")
    def send(self,subject,body,to=None):
        if to == None: to = self.recv 
        body = "Content-type: text/html \nSubject: {}\n\n <font color='#66AAFF'> {}</font>".format(subject,body)
        if self.server is not None: self.server.sendmail(self.mail,to,body.encode())
    def quit(self): self.server.quit()
    
if __name__ == "__main__":
    mailSender = Mail()
    mailSender.wait()
    mailSender.send(subject='Python mail',body=input("MAIL: "))
    mailSender.quit()