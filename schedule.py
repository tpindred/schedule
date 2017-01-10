import requests
from bs4 import BeautifulSoup
import re
import smtplib
import certifi

class Employee(object):

    def __init__(self, user_info): # user_info is a dict containing name, pass number, and email
        self.name = user_info['name']
        self.pass_number = user_info['pass_number']
        self.password = 'GCT123'
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
            get = session.get(get_url, cookies=jar, verify=False)# THIS IS INSECURE, ONLY USE 'verify=False' FOR TESTING
            #jar.set(session.cookies)
            post = session.post(post_url, cookies=jar, data=payload, verify=False) # THIS IS INSECURE, ONLY USE 'verify=False' FOR TESTING
            return post

    def update_schedule(self, post_response):
        soup = BeautifulSoup(post_response.text, 'lxml')
        schedule_text = soup.find(id='schedule')
        rows = schedule_text.find_all(class_=re.compile('^row'))
        for row in rows:
            self.schedule.append({})
            for count, child in enumerate(row.children):
                # really need to find more pythonic way than a series of ifs
                if count == 0:
                    self.schedule[-1]['date'] = child.string
                elif count == 1:
                    self.schedule[-1]['hours'] = child.string
                elif count == 2:
                    self.schedule[-1]['activity'] = child.string
        
    def send_email(self):
        username = 'ted.pindred'
        password = 'Kuystad14645%'
        sender = 'ted.pindred@gmail.com'
        message = 'Hello {},\n\nToday you are scheduled for {}.\n\nYou were recorded for {} hours in {}.'.format(self.name, self.schedule[0]['activity'], 'test', 'test')
        
        
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(sender, self.email, message)         
        print ("Successfully sent email")
        server.quit()
        
        
        
        
    
