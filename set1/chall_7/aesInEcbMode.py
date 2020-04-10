import base64
from Cryptodome.Cipher import AES


def AESdecrypt(byteArray, key):
    cipher = AES.new(bytes(key.encode('utf-8')), AES.MODE_ECB)
    pt = cipher.decrypt(byteArray)
    return pt

def main():
    key = "YELLOW SUBMARINE"
    ipFile = open("input.txt", 'r')
    contents = ''
    for line in ipFile:
        contents += line[:len(line)-1]
    contents = base64.b64decode(contents)
    pt = AESdecrypt(contents, key)
    print(pt)
    #print(len(contents))


if __name__ == "__main__":
    main()
