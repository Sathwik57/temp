from dotenv import load_dotenv
import os
import getpass
from hasher import verify_hash
from menu import menu,commands

load_dotenv()

if __name__ == '__main__':
    pswd = getpass.getpass("Please enter secret key to continue:")

    try:
        master = os.environ['MASTER']
        print(master)
    except KeyError:
        print('App is not configured yet..')
        exit()

    if not verify_hash(master, pswd):
        print('Incorrect Credentials')
        exit()

    print('Welcome, you are logged in')

    choice = menu()
    while choice not in ('Q', 'q', 'X', 'x'):
        try:
            commands[choice]()
        except:
            print('\nError Occured ,Retry')
        finally:
            choice = menu()
