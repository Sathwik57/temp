import os
import psycopg2
from hasher import decrypt_hash, encrypt_hash


def connect():
    try:
        connection = psycopg2.connect(
            user= os.environ.get('POSTGRES_USER'), 
            password= os.environ.get('POSTGRES_PASSWORD'), 
            database=os.environ.get('POSTGRES_DB'),
            host = os.environ.get('POSTGRES_HOST'),
            port = os.environ.get('POSTGRES_PORT')    
        )
        return connection
    except Exception as error:
        print(error)


def store_pswd(pswd, email, url, app_name, username = 'Vicky'):
    try:
        connection = connect()
        cursor = connection.cursor()
        
        query = """INSERT INTO ACCOUNTS(password, email, url, app_name, username) 
        VALUES(%s, %s, %s, %s, %s)"""
        os.system(f'echo {pswd}|clip')
        pswd = encrypt_hash(pswd, key = os.environ.get('KEY'))
        record = (pswd, email, url, app_name, username)
        cursor.execute(query, record)
        connection.commit()
        print('Password Stored and copied to clipboard')
        
    except (Exception, psycopg2.Error) as e:
        print(f'Error {e} occured')


def find_password(app_name, search_var):
    try:
        connection = connect()
        cursor = connection.cursor()
        
        query = f"SELECT password,email FROM accounts WHERE lower({search_var}) like %s"
        cursor.execute(query, (f'%{app_name.lower()}%',))
        connection.commit()
        
        result = cursor.fetchall()
        if len(result) == 0:
            print('No data present for given details')
        else:
            print('-'*30)
            print ("{:<8} | {:<20} | {:<30}".format('Row','Email','Password'))        
            decrypted_pass = []
            for i, val in enumerate(result):
                temp = decrypt_hash(val[0], os.environ.get('KEY'))
                decrypted_pass.append(temp)
                print(
                    "{:<8} | {:<20} | {:<25}".format(i + 1, val[1], temp)
                )  
            print('-'*30)
            ch = 1
            if len(result) > 1:
                try:
                    ch = int(input(
                        'Enter the row number for to copy or 0 if not required: '
                    ))
                except KeyError:
                    ch = 0
            
            if ch != 0:
                os.system(f'echo {decrypted_pass[ch-1]}|clip')
                print('Password copied to clipboard\n')

    except (Exception, psycopg2.Error) as error:
        print(error)