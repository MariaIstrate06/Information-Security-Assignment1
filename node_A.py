import socket
from Crypto.Cipher import AES

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


to_send = input('Choose your mode (ECB/CBC): ')
client_socket.send(str.encode(to_send))
encrypted_response = client_socket.recv(2048)
encoded_the_key = aes.decrypt(encrypted_response)

the_key = encoded_the_key.decode('utf-8')

message_from_B = client_socket.recv(2048)
# if message_from_B.decode('utf-8') == 'Ready!':
