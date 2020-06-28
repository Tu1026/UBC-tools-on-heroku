"""Monitors the given course and send update when a spot frees up

    Usage: change the url to the course, chagne the word looking for to however, many people is registered in the class
    , subscribe to the printed website to recieve notification
"""


from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
import ctypes
from notify_run import Notify
import smtplib
from configparser import ConfigParser 
from dotenv import load_dotenv
import os
import winsound


load_dotenv()
s = os.getenv("password")
#Reference from https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
def send_email(username, password):
    """send email to the person who wishes to recieve notification
    """
    sent_from = username
    to = [noti_email]
    subject = 'Course registeration for ' + course
    body = 'The course you want has a seat open!!'
    message ='Subject: {}\n\n{}'.format(subject, body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(username, password)
    server.sendmail(sent_from, to, message)
    server.close()


#get information from user
course = input("what course are you looking for?")
noti_email = input("what is your email that you want to get notificaition at?")
url = input("What is the 'section' specific url that you want to get in" +
"(ex: https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=BIOL&course=234&section=921)?")
registered = input("How many people are registered in this section so far(only enter number ex: 100)?")


## Create notification channel
notify = Notify()
print(notify.register())
print("go to this website if you want push notificaiton from browser")


## Keeps looping through the website until a spot is open
while True:
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    text_list = text.split()
    word_looking_for = "Registered:" + registered
    # if the amount of people registered has not changed keep looping
    if word_looking_for in text_list:
        # wait 30 seconds,
        print("No seats avaliable yet updating in 30 seconds")
        time.sleep(30)
        # continue with the script,
        continue
        
    # if the amout of people registered has changed do a pop up and send a notificaiton on the website
    else:
        notify.send("register for " + course + " NOW")
        try:
            # log into server account to send message
            config = ConfigParser()
            config.read('config.ini')
            username = os.getenv("username1")
            password = os.getenv("password")
            # username = config.get("email", "username")
            # password = config.get("email", "password")
            send_email(username, password)
            print("email notificaiton sent")
        except:
            print("something went wrong with emailing stuff")
        ctypes.windll.user32.MessageBoxW(0, course, 'Spot is now open for', course)
        winsound.MessageBeep()
        break

