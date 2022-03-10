import base64
from Crypto.Cipher import AES
import hashlib

salt = '$*&@%!$**@@@#@$$'

def calculate_hash(data_string):
    hashstring = hashlib.sha256(data_string.encode())
    hashstring = hashstring.hexdigest()
    return hashstring

def verify_hash(pswd, data):
    data = calculate_hash(data)
    print(data)
    return pswd == data

def encrypt_hash(hashed, key):
    alg =AES.new(key.encode('utf-8'), AES.MODE_CFB, salt.encode('utf-8'))
    input = alg.encrypt(hashed.encode())
    input = base64.b64encode(input)
    return input.decode("UTF-8")

def decrypt_hash(encrypted, key):
    encrypted = base64.b64decode(encrypted)
    alg = AES.new(key.encode('utf-8'), AES.MODE_CFB, salt.encode('utf-8'))
    output = alg.decrypt(encrypted)
    if type(output) == bytes:
        output = output.decode()
    return output
