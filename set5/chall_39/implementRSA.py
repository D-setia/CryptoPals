from Crypto.Util import number
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers

def stringToInt(string):
    strHex = string.encode('latin1').hex()
    Int = int(strHex, 16)
    return Int

def intToStr(integer):
    hexStr = hex(integer)[2:]
    if len(hexStr)%2 == 1:
        hexStr = '0' + hexStr
    byteStr = bytes.fromhex(hexStr)
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
    m = stringToInt(ptString)
    ctInt = encryptInt(m, publicKey)
    ctStr = intToStr(ctInt)
    return ctStr


def decrypt(ctString, privateKey):
    ctInt = stringToInt(ctString)
    ptInt = decryptInt(ctInt, privateKey)
    ptStr = intToStr(ptInt)
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

