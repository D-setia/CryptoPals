import random
import sys
sys.path.insert(1, "../..")
import set1.chall_7.aesInEcbMode as AES_ECB
import set2.chall_9.implementPKCS7 as PKCS7
import set2.chall_10.implementCbcMode as AES_CBC

def getRandBytes(noOfBytes):
    randBytes = []
    for i in range(noOfBytes):
        randBytes.append(random.randrange(0,256))
    randBytes = bytes(randBytes)
    return randBytes


def randPadPlaintext(ptByteArray, padBefore, padAfter):
    randPaddedPt = []
    for i in range(padBefore):
        randPaddedPt.append(random.randrange(0,256))
    for i in range(len(ptByteArray)):
        randPaddedPt.append(ptByteArray[i])
    for i in range(padAfter):
        randPaddedPt.append(random.randrange(0,256))
    
    randPaddedPt = bytes(randPaddedPt)
    return randPaddedPt


def blackBox(ptByteArray):
    padBefore = random.randrange(5,11)
    padAfter = random.randrange(5,11)
    randPaddedPt = randPadPlaintext(ptByteArray, padBefore, padAfter)
    key = getRandBytes(16)

    encMode = random.randrange(0,2)
    if encMode == 0:
        ptInput = PKCS7.PKCS7(randPaddedPt, 16)
        ct = AES_ECB.AESencrypt(ptInput, key)
        #print('Original: ECB')
        return ct
    else:
        ptInput = PKCS7.PKCS7(randPaddedPt, 16)
        IV = getRandBytes(16)
        ct = AES_CBC.AES_CBCencrypt(ptInput, key, IV)
        #print('Original: CBC')
        return ct


def main():
    length = random.randrange(10,51)
    pt = getRandBytes(length)
    ct = blackBox(pt)
    print(ct)


if __name__ == "__main__":
    main()
