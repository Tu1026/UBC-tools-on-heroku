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
from fbchat import Client
import fbchat


load_dotenv()
# use https://findmyfbid.in/#:~:text=Find%20your%20facebook%20ID%20in%20two%20easy%20steps&text=Your%20Facebook%20personal%20profile%20URL,profile.php%3Fid%3D100001533612613
# to find uid
def send_fb_message(word: str, uid: str):
    """print the given string one word at a time to fb friend
        Args: 
            a string that contain multiple words, the uid of the fb friend
            user input: username and password
    """
    uid = os.getenv("uid")
    username_fb = os.getenv("username2") 
    passwrod_fb = os.getenv("password1")
    username = str(input("Username: ")) 
    client = fbchat.Client(username_fb, passwrod_fb)
    client.send(fbchat.models.Message(word), uid)
    client.logout()



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
        # wait 15 seconds,
        print("No seats avaliable yet updating in 15 seconds")
        time.sleep(15)
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
            send_fb_message("register for " + course + "NOWWWWWWW")
            send_email(username, password)
            print("email notificaiton sent")
        except:
            print("something went wrong with emailing stuff or FB stuff")
        ctypes.windll.user32.MessageBoxW(0, course, 'Spot is now open for', course)
        winsound.MessageBeep()
        break
