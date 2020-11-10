import socket
from Crypto.Cipher import AES
from mode_implementation import *

client_socket = socket.socket()
host = '127.0.0.1'
port = 2345
key3 = b'ABCDEF0123456789'
aes = AES.new(key3, AES.MODE_ECB)

# Preparing client for connection with Server (KEY MANAGER)
print('Waiting for connection')
try:
    client_socket.connect((host, port))
except socket.error as error:
    print(str(error))

to_send = input('Choose your mode (ECB/CBC): ').upper()
client_socket.send(to_send.encode('utf-8'))
encrypted_response = client_socket.recv(2048)
encoded_the_key = ecb_decryption(encrypted_response)
# print(encoded_the_key)

# the_key = encoded_the_key.decode('utf-8')

message_from_B = client_socket.recv(2048)
if message_from_B.decode('utf-8') == 'Ready!':
    print('READY!')

with open("some_text.txt", "rb") as file:
    b_text = file.read()
    if to_send == 'ECB':
        b_text = ecb_encryption(b_text)
    else:
        # print("original: ", b_text)
        b_text = cbc_encryption(b_text)
        # print("crypted: ", b_text)

    for index in range(0, len(b_text), 16):
        # print(b_text[index:index+16])
        client_socket.send(b_text[index:index + 16])
    # print('all good')

