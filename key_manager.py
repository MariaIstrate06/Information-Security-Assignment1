import socket
from Crypto.Cipher import AES
from mode_implementation import *

# keys and initialization vector
key1 = b'0123456789ABCDEF'
key2 = b'ABCDEFGHIJKLMNOP'
key3 = b'ABCDEF0123456789'
iv = b'cristosuma-tiiSI'

aes_ecb = AES.new(key3, AES.MODE_ECB)
aes_cbc = AES.new(key3, AES.MODE_CBC, iv)


# socket variables
server_socket = socket.socket()
host = '127.0.0.1'
port = 2345


# connection, preparing the server for listening
try:
    server_socket.bind((host, port))
except socket.error as error:
    print(str(error))
print('Waiting for a connection...')
server_socket.listen(1)

# prepping the aes variable for encryption


# connecting node A
node_A, address_A = server_socket.accept()
print("Node A connected!")

# connecting node B
node_B, address_B = server_socket.accept()
print("Node B connected!")

crypto_mode_from_A = node_A.recv(2048)

# receiving encrypting mode from A
if crypto_mode_from_A.decode('utf-8') == 'ECB':
    pad(key1)
    encrypted_key1 = ecb_encryption(key1)
    node_A.send(encrypted_key1)
    node_B.send(b'ECB')  # sending the encryption mode to B


elif crypto_mode_from_A.decode('utf-8') == 'CBC':
    pad(key2)
    encrypted_key2 = ecb_encryption(key2)
    node_A.send(encrypted_key2)
    node_B.send(b'CBC')  # sending the encryption mode to B
else:
    node_A.send(b'Please run again and choose from ECB/CBC')

# some redundant code because we should send
# the key to B once we know it's ECB but oh
# well let's stick with the requirements

b_key_request = node_B.recv(2048)
if b_key_request.decode('utf-8') == 'ECB':
    pad(key1)
    key1 = key1.decode('utf-8')
    encrypted_for_b_key1 = ecb_encryption(key1)
    node_B.send(encrypted_for_b_key1)

if b_key_request.decode('utf-8') == 'ECB':
    pad(key1)
    encrypted_for_b_key2 = ecb_encryption(key2)
    node_B.send(encrypted_for_b_key2)

message_from_B = node_B.recv(2048)
node_A.send(message_from_B)
buff = node_A.recv(2048)
while buff:
    node_B.send(buff)
    buff = node_A.recv(2048)

