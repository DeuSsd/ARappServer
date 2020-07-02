from Cryptodome.Cipher import DES

file = open("Key.txt", "rb")
key = (file.read())
def pad(text):
    while len(text) % 8 != 0:
           text += b' '
    return text
#coding password
def coding(password):
    des = DES.new(key, DES.MODE_ECB)
    test_string = password
    text = bytes(test_string, 'utf-8')
    padded_text = pad(text)
    encrypted_text = des.encrypt(padded_text)
    print(encrypted_text)
    return encrypted_text
#дешифровка
def decoding(name):
    des = DES.new(key, DES.MODE_ECB)
    data = des.decrypt(name)
    print(data)
    return data