import socket
from Crypto.Cipher import AES
from mode_implementation import *

client_socket = socket.socket()
host = '127.0.0.1'
port = 2345
key3 = b'ABCDEF0123456789'
iv = b'somestring123456'
aes_ecb = AES.new(key3, AES.MODE_ECB)

print('Waiting for connection')
try:
    client_socket.connect((host, port))
except socket.error as error:
    print(str(error))

encrypting_mode_received_from_a = client_socket.recv(2048)

if encrypting_mode_received_from_a.decode('utf') == 'ECB':
    # we have to send a message to the server
    # in which we request k1
    print('Okay, we are working with ECB!')
    client_socket.send(str.encode('ECB'))
elif encrypting_mode_received_from_a.decode('utf-8') == 'CBC':
    # we have to send a message to the server
    # in which we request k2
    print('Okay, we are working with CBC!')
    client_socket.send(str.encode('CBC'))

key_received_from_server = client_socket.recv(2048)
the_key = aes_ecb.decrypt(key_received_from_server)

client_socket.send(str.encode('Ready!'))

to_decrypt = b''
from_A = client_socket.recv(16)
while from_A:
    to_decrypt += from_A
    from_A = client_socket.recv(16)
# print(to_decrypt)
if encrypting_mode_received_from_a == 'ECB':
    final = ecb_decryption(to_decrypt)
else:
    final = cbc_decryption(to_decrypt)

print(final)
