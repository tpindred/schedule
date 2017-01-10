from schedule import Employee

users = [{}]

def main():

    for user in users:
        employee = Employee(user)
        employee.update_schedule(employee.login())
        employee.send_email()

main()

    
