import base64
import random
import sys
sys.path.insert(1, "../../")
import set1.chall_7.aesInEcbMode as AES_ECB
import set2.chall_9.implementPKCS7 as PKCS7
import set2.chall_11.detectionOracle as detectionOracle

GLOBAL_KEY = None
GLOBAL_DICT = None
UNKNOWN_STRING = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

def getRandBytes(noOfBytes):
    randBytes = []
    for i in range(noOfBytes):
        randBytes.append(random.randrange(0, 256))
    randBytes = bytes(randBytes)
    return randBytes


def encryptionOracle(ptByteArray):
    global GLOBAL_KEY
    global UNKNOWN_STRING
    unknownString = base64.b64decode(UNKNOWN_STRING)
    if GLOBAL_KEY == None:
        GLOBAL_KEY = getRandBytes(16)
    ptInput = PKCS7.PKCS7(ptByteArray+unknownString, 16)
    ct = AES_ECB.AESencrypt(ptInput, GLOBAL_KEY)
    return ct

def detectBlockSize(encFunc):
    initialLen = None
    for i in range(100):
        ptInput = 'a'*i
        ptInput = bytes(ptInput.encode('utf-8'))
        ct = encFunc(ptInput)
        newLen = len(ct)
        
        if i == 0:
            initialLen = newLen
        else:
            if newLen != initialLen:
                blockSize = newLen - initialLen
                return blockSize, initialLen

    return None, None


def generateDict(initialBytes):
    dictionary =[]
    for i in range(256):
        newByte = bytes([i])
        ct = encryptionOracle(initialBytes+newByte)
        ctBlock = ct[:16]
        dictionary.append(ctBlock)
    return dictionary


def detectUnknownString():
    blockSize, initialLen = detectBlockSize(encryptionOracle)
    secret = []
    for i in range(initialLen):
        payloadLen = blockSize-1-i%blockSize
        payload = 'a'*payloadLen
        payload = bytes(payload.encode('utf-8'))
        ct = encryptionOracle(payload)
        ctBlockWithNewLastByte = ct[(i//16)*16:(i//16 + 1)*16]
        payloadForDict = bytes(''.encode('utf-8'))
        try:
            if i < blockSize:
                payloadForDict += payload
                for j in range(i):
                    payloadForDict += bytes([secret[j]])
            else:
                for j in range(i-15, i):
                    payloadForDict += bytes([secret[j]])
        except:
            break
        else:
            dictionary = generateDict(payloadForDict)
            for j in range(len(dictionary)):
                if ctBlockWithNewLastByte == dictionary[j]:
                    secret.append(j)
                    break
    secret = secret[:len(secret)-1]
    return bytes(secret)


def main():
    secret = detectUnknownString()
    print(secret.decode('utf-8'))


if __name__ == "__main__":
    main()
