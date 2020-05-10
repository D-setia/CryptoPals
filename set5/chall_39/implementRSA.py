import base64
from Crypto.Util import number
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers

def stringToInt(string, doB64encode):
    if doB64encode:
        byteStr = string.encode('latin1')
        b64ByteStr = base64.b64encode(byteStr)
        strHex = b64ByteStr.hex()
    else:
        strHex = string.encode('latin1').hex()
    Int = int(strHex, 16)
    return Int

def intToStr(integer, doB64Decode):
    hexStr = hex(integer)[2:]
    if len(hexStr)%2 == 1:
        hexStr = '0' + hexStr
    byteStr = bytes.fromhex(hexStr)
    if doB64Decode:
        b64str = byteStr.decode('latin1')
        string = base64.b64decode(b64str)
        string = string.decode('latin1')
    else:
        string = byteStr.decode('latin1')
    return string


def generateKeyPair(primeLenInBits = 512):
    d = None
    while d == None:
        p = number.getPrime(primeLenInBits)
        q = number.getPrime(primeLenInBits)
        n = p*q
        et = (p-1)*(q-1)
        e = 3
        d = helpers.modInv(e, et)
    privateKey = (d, n)
    publicKey = (e, n)
    keyPair = (privateKey, publicKey)
    return keyPair

def encryptInt(pt, publicKey):
    e = publicKey[0]
    n = publicKey[1]
    ct = pow(pt, e, n)
    return ct

def decryptInt(ct, privateKey):
    d = privateKey[0]
    n = privateKey[1]
    pt = pow(ct, d, n)
    return pt

def encrypt(ptString, publicKey):
    m = stringToInt(ptString, True)
    ctInt = encryptInt(m, publicKey)
    ctStr = intToStr(ctInt, False)
    return ctStr


def decrypt(ctString, privateKey):
    ctInt = stringToInt(ctString, False)
    ptInt = decryptInt(ctInt, privateKey)
    ptStr = intToStr(ptInt, True)
    return ptStr

def main():
    (privateKey, publicKey) = generateKeyPair()
    pt = 'Helashdgoalhdfasdilfhajlo my dear friend'
    #print(publicKey)
    #print(privateKey)
    ct = encrypt(pt, publicKey)
    ptR = decrypt(ct, privateKey)
    #print(pt, end = '\n\n')
    #print(ct, end = '\n\n')
    #print(ptR)
    print(pt == ptR)


if __name__ == "__main__":
    main()

