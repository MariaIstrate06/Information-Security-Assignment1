import socket
from Crypto.Cipher import AES

# keys and initialization vector
key1 = b'0123456789ABCDEF'
key2 = b'ABCDEFGHIJKLMNOP'
key3 = b'ABCDEF0123456789'
iv = b'cristosuma-tiiSI'

# socket variables
server_socket = socket.socket()
host = '127.0.0.1'
port = 2345


def pad(text_to_pad):
    # function for padding
    # if the to_encrypt block is not a multiple of 16 bytes
    # add empty spaces until the dimensions are okay
    blocks = (16 - len(text_to_pad) % 16) % 16
    text_to_pad += chr(0).encode("utf8") * blocks
    return text_to_pad


# connection, preparing the server for listening
try:
    server_socket.bind((host, port))
except socket.error as error:
    print(str(error))
print('Waiting for a connection...')
server_socket.listen(1)

# prepping the aes variable for encryption
aes_ecb = AES.new(key3, AES.MODE_ECB)
aes_cbc = AES.new(key3, AES.MODE_CBC, iv)

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
    encrypted_key1 = aes_ecb.encrypt(key1)
    node_A.send(encrypted_key1)
    node_B.send(b'ECB')  # sending the encryption mode to B


elif crypto_mode_from_A.decode('utf-8') == 'CBC':
    pad(key2)
    encrypted_key2 = aes_ecb.encrypt(key2)
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
    encrypted_for_b_key1 = aes_ecb.encrypt(key1)
    node_B.send(encrypted_for_b_key1)

if b_key_request.decode('utf-8') == 'ECB':
    pad(key1)
    encrypted_for_b_key2 = aes_ecb.encrypt(key2)
    node_B.send(encrypted_for_b_key2)

message_from_B = node_B.recv(2048)
node_A.send(message_from_B)









# def thread_client(connection):
#     connection.send(str.encode('Welcome to the server\n'))
#     while True:
#         data = connection.recv(2046)
#         reply = 'Server Says: ' + data.decode('utf-8')
#         if not data:
#             break
#         connection.sendall(str.encode(reply))
#     connection.close()

# while True:
#     client, address = server_socket.accept()
#     print('Connected to: ' + address[0] + ':' + str(address[1]))
#     start_new_thread(thread_client, (client,))
#     thread_count += 1
#     print('Thread Number: ' + str(thread_count))


# server_socket.close()

# HOST = '127.0.0.1'
# PORT = 2345
#
# with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn_A, addr_A = s.accept()
#     conn_B, addr_B = s.accept()
#     with conn_A:
#         print('Connected by', addr_A)
#         while True:
#             data = conn_A.recv(1024)
#             if not data:
#                 break
#             conn_A.sendall(data)
#     with conn_B:
#         print('Connected by', addr_B)
#         while True:
#             data = conn_B.recv(1024)
#             if not data:
#                 break
#             conn_B.sendall(data)
