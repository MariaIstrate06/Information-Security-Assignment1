from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor

# from Crypto.Util.Padding import pad, unpad

key1 = b'0123456789ABCDEF'
key2 = b'ABCDEFGHIJKLMNOP'
key3 = b'ABCDEF0123456789'
iv = b'cristosuma-tiiSI'

aes_ecb = AES.new(key3, AES.MODE_ECB)
aes_cbc = AES.new(key3, AES.MODE_CBC, iv)


def pad(text_to_pad):
    if type(text_to_pad) is str:
        text_to_pad = text_to_pad.encode("utf-8")
    # function for padding
    # if the to_encrypt block is not a multiple of 16 bytes
    # add empty spaces until the dimensions are okay
    blocks = (16 - len(text_to_pad) % 16) % 16
    text_to_pad += chr(0).encode('utf-8') * blocks
    return text_to_pad


# def unpad(text_to_unpad):
#     # nimic lasa


def ecb_encryption(string_to_encode):
    # string_to_encode = string_to_encode.decode('utf-8')
    encoded_string = b''
    my_list_of_blocks = []
    while string_to_encode:
        my_list_of_blocks.append(string_to_encode[:16])
        string_to_encode = string_to_encode[16:]
    my_list_of_blocks[len(my_list_of_blocks) - 1] = pad(my_list_of_blocks[len(my_list_of_blocks) - 1])
    for i in my_list_of_blocks:
        # print("i type: ", type(i))
        encoded_string = encoded_string + aes_ecb.encrypt(i)
    return encoded_string


def cbc_encryption(string_to_encode):
    init = b'cristosuma-tiiSI'
    encoded_string = b''
    my_list_of_blocks = []
    while string_to_encode:
        my_list_of_blocks.append(string_to_encode[:16])
        string_to_encode = string_to_encode[16:]
    my_list_of_blocks[len(my_list_of_blocks) - 1] = pad(my_list_of_blocks[len(my_list_of_blocks) - 1])
    for i in my_list_of_blocks:
        block = aes_cbc.encrypt(strxor(bytes(i, 'utf-8'), init))
        init = block
        encoded_string = encoded_string + block
    return encoded_string


def ecb_decryption(string_to_decode):
    decoded_string = ''
    list_of_blocks = []
    while string_to_decode:
        list_of_blocks.append(string_to_decode[:16])
        string_to_decode = string_to_decode[16:]
    for i in list_of_blocks:
        decoded_string = decoded_string + aes_ecb.decrypt(i).decode('utf-8')
    # decoded_string = unpad(decoded_string)
    return decoded_string


def cbc_decryption(string_to_decode):
    decoded_string = ''
    list_of_blocks = []
    while string_to_decode:
        list_of_blocks.append(string_to_decode[:16])
        string_to_decode = string_to_decode[16:]
    for i in list_of_blocks:
        decoded_string = decoded_string + aes_ecb.decrypt(i).decode('utf-8')
    # decoded_string = unpad(decoded_string)
    return decoded_string

# the_string = 'pavalistratemariateodora'
# the_encoded_string = ecb_encryption(the_string)
# print("encoded: ", the_encoded_string)
# the_decoded_string = ecb_decryption(the_encoded_string)
# print("decoded: ", the_decoded_string)
# the_cbc = cbc_encryption(the_string)
# print("encoded with cbc: ", the_cbc)
# the_cbc_decoded = cbc_decryption(the_cbc)
# print("decoded with cbc: ", the_cbc_decoded)
