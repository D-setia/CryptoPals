import base64
import pprint

def asciiToHexString(ip):
    ip = ip.encode('utf-8')
    hexString = ip.hex()
    return hexString

def hexStringToBytes(ip):
    byteArray = bytes.fromhex(ip)
    return byteArray

def bytesTob64(ip):
    b64String = base64.b64encode(ip)
    return b64String

def hexStringToAscii(ip):
    string = bytearray.fromhex(ip).decode()
    return string

def main():
    ip = input("Give your input: ")
    #print(hexStringToAscii(asciiToHexString(ip)))


if __name__ == "__main__":
    main()
