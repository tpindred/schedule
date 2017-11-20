from schedule import Employee
import json


def load_user_data(userinfo):
    with open(userinfo) as json_data:
        users_raw = json.load(json_data)
    users_clean = []
    for user in users_raw['users']:
        for key, value in user.iteritems():
            users_clean.append({'name' : key, 'passnumber' : value['passnumber'], 'email' : value['email']})

def load_sender_data(senderinfo):
    with open(senderinfo) as json_data:
        sender = json.load(json_data)
def main():
    users = load_user_data('userinfo.json','senderinfo.json')
    for user in users:
        
        employee = Employee(user)
        employee.update_schedule(employee.login())
        employee.send_email()

main()

    
