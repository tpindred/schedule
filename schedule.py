import requests
from bs4 import BeautifulSoup
import re
import smtplib
import certifi
import json

class Employee(object):

    def __init__(self, user_info): # user_info is a dict containing name, pass number, and email
        self.name = user_info['name']
        self.pass_number = user_info['pass_number']
        self.password = user_info['password']
        self.email = user_info['email']
        self.schedule = []
        self.three_day_outlook = []
        self.yesterdays_hours = None

    def login(self):
        '''
        Logs into the RTP site with the user pass number. 
        Returns the post response object from the login. 
        '''

        get_url = 'https://secure.winterparkresort.com/WebInstructorTools/instructorTools/login.do'
        post_url = 'https://secure.winterparkresort.com/WebInstructorTools/instructorTools/processLogin.do'
        payload = {
            'passNumber' : self.pass_number,
            'password' : self.password,
            'loginBtn' : '[+Login+]'
        }
        cookie_1 = 'eComRtpOneId'
        cookie_2 = 'key=2121853-955741&id=resortx&store=resortx'

        with requests.Session() as session:
            jar = requests.cookies.RequestsCookieJar()
            jar.set(cookie_1, cookie_2, domain='secure.winterparkresort.com')
            get = session.get(get_url, cookies=jar, verify=False) #Try to find a workaround for verify=False
            post = session.post(post_url, cookies=jar, data=payload, verify=False) 
            return post

    def update_schedule(self, post_response):
        soup = BeautifulSoup(post_response.text, 'lxml')
        schedule_text = soup.find(id='schedule')
        rows = schedule_text.find_all(class_=re.compile('^row'))
        for row in rows:
            self.schedule.append({})
            for count, child in enumerate(row.children):
                if count == 0:
                    self.schedule[-1]['date'] = child.string
                elif count == 1:
                    self.schedule[-1]['hours'] = child.string
                elif count == 2:
                    self.schedule[-1]['activity'] = child.string
        
    def send_email(self):
        message = 'Hello {},\n\nToday you are scheduled for {}.'.format(self.name, self.schedule[0]['activity'])
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(senderinfo["username"],senderinfo["password"])
            server.sendmail(senderinfo["sender"], self.email, message)         
            print ("Successfully sent email")
            server.quit()
        except SMTPException:
            print ("Error: unable to send email")
        
    
