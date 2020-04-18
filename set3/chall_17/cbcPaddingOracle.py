import base64
import random
import sys
sys.path.insert(1, "../../")
import helperFunctions as helper
import set2.chall_9.implementPKCS7 as PKCS7
import set2.chall_10.implementCbcMode as AES_CBC

GLOBAL_KEY = None
BLOCK_SIZE = 16

def encryptRandString():
    global GLOBAL_KEY
    if GLOBAL_KEY == None:
        GLOBAL_KEY = helper.getRandBytes(16)
    IV = helper.getRandBytes(16)

    ipFile = open("input.txt", 'r')
    choice = random.randrange(1,11)
    randString = ''
    for i in range(choice):
        randString = ipFile.readline()
    randString = randString[:len(randString)-1]
    randString = base64.b64decode(randString)

    ptInput = PKCS7.PKCS7(randString, 16)
    ct = AES_CBC.AES_CBCencrypt(ptInput, GLOBAL_KEY, IV)
    return IV, ct


def decryptAndValidate(IV, ct):
    global GLOBAL_KEY
    global BLOCK_SIZE
    pt = AES_CBC.AES_CBCdecrypt(ct, GLOBAL_KEY, IV)
    #print(pt[len(pt)-2:len(pt)])
    isValidPadding = PKCS7.PKCS7validate(pt, BLOCK_SIZE)
    return isValidPadding


def determineEncString():
    IV, ct = encryptRandString()
    blockSize = 16
    noOfBlocks = len(ct)//blockSize
    secret = []
    for i in range(len(ct)):
        #print(i)
        ctToDec = ct[:len(ct)-(i//blockSize)*blockSize]
        if len(ctToDec) > 2*blockSize:
            ctLen = len(ctToDec)
            added = False
            for j in range(256):
                if j != i%blockSize+1:
                    modifiedCt = ctToDec[:ctLen-2*blockSize]
                    modifiedCt += ctToDec[ctLen-2*blockSize: ctLen-blockSize-i%blockSize-1]
                    modifiedCt += bytes([ctToDec[ctLen-blockSize-i%blockSize-1]^j^(i%blockSize +1)])
                    for k in range(i%blockSize):
                        modifiedCt += bytes([secret[len(secret)-1-k]^ctToDec[ctLen-blockSize-i%blockSize+k]^(i%blockSize +1)])

                    modifiedCt += ctToDec[len(ctToDec)-16:len(ctToDec)]
                
                    isValid = decryptAndValidate(IV, modifiedCt)
                    if isValid:
                        secret.append(j)
                        added = True
                        break
            if not added:
                secret.append(i%blockSize +1)
        elif len(ctToDec) == 2* blockSize:
            ctLen = len(ctToDec)
            added = False
            for j in range(256):
                modifiedCt = bytes(''.encode('utf-8'))
                if j != i%blockSize+1:
                    modifiedCt += ctToDec[: ctLen-blockSize-i%blockSize-1]
                    modifiedCt += bytes([ctToDec[ctLen-blockSize-i%blockSize-1]^j^(i%blockSize +1)])
                    for k in range(i%blockSize):
                        modifiedCt += bytes([secret[len(secret)-1-k]^ctToDec[ctLen-blockSize-i%blockSize+k]^(i%blockSize +1)])

                    modifiedCt += ctToDec[len(ctToDec)-16:len(ctToDec)]
                
                    isValid = decryptAndValidate(IV, modifiedCt)
                    if isValid:
                        secret.append(j)
                        added = True
                        break
            if not added:
                secret.append(i%blockSize +1)
        elif len(ctToDec) == blockSize:
            ivLen = len(IV)
            added = False
            for j in range(256):
                modifiedIV = bytes(''.encode('utf-8'))
                if j != i%blockSize+1:
                    modifiedIV += IV[: blockSize-i%blockSize-1]
                    modifiedIV += bytes([IV[blockSize-i%blockSize-1]^j^(i%blockSize +1)])
                    for k in range(i%blockSize):
                        modifiedIV += bytes([secret[len(secret)-1-k]^IV[blockSize-i%blockSize+k]^(i%blockSize +1)])
                    isValid = decryptAndValidate(modifiedIV, ctToDec)
                    if isValid:
                        secret.append(j)
                        added = True
                        break
            if not added:
                secret.append(i%blockSize +1)

    secret = secret[::-1]
    secret = bytes(secret)
    print(secret)



def main():
    determineEncString()
    #string = "abcdefghi"
    #print(len(string))
    #print(string[:3])
    #print(string[3:3])
    #print(string[6])


if __name__ == "__main__":
    main()

