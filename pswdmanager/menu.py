from db import store_pswd, find_password
from hasher import calculate_hash

def create():
    app_name  = input('Enter the App/site name: ')
    email = input('Enter the email linked to the site: ')
    url =  input('Enter the App/site url: ')
    pswd = input('Enter the password: ')
    store_pswd(pswd, email, url, app_name)

def get_data_app():
    app_name  = input('Enter the App/site to get password for: ')
    find_password(app_name, 'app_name')

def get_data_email():
    mail  = input('Enter the email to get passwords for: ')
    find_password(mail, 'email')

def menu():
    options = [
        'Store New Creds',
        'Get Pswd of site or app',
        'Get all Sites/Apps linked to the Email',
        'Quit'
    ]
    print('/','*'*15,'Menu','*'*15,'/')
    for i,v in enumerate(options):
        print(f'{i+1}. {v}' if v!= 'Quit' else f'Q/x. {v}') 
    return input('Enter the option: ')

commands={
    '1' : create,
    '2' : get_data_app,
    '3' : get_data_email,
}