import random
import sys
sys.path.insert(1, "../../")
import set2.chall_12.byteAtATimeEcbDec_simple as EncFunctions
import set2.chall_9.implementPKCS7 as PKCS7

PADDED_CTS = []

def encryptionOracle(ptBytes, shouldPrint):
    blockSize = 16
    noOfBytes = random.randrange(5,11)    
    randBytes = EncFunctions.getRandBytes(noOfBytes)
    randPaddedPt = randBytes+ptBytes
    if shouldPrint:
        print(noOfBytes)
        print(randPaddedPt[16:32])
    ct = EncFunctions.encryptionOracle(randPaddedPt)
    return ct


def determineStrLen():
    payload = ''
    payload = bytes(payload.encode('utf-8'))
    ct = encryptionOracle(payload, False)
    strLen = len(ct)
    return strLen


def addToGlobalCts(ct):
    global PADDED_CTS
    alreadyPresent = False
    for i in range(len(PADDED_CTS)):
        if ct == PADDED_CTS[i]:
            alreadyPresent = True
    if not alreadyPresent:
        PADDED_CTS.append(ct)


def generatePaddedCts():
    global PADDED_CTS
    payload = 'a'*16+'b'
    payload = payload*11
    payload = bytes(payload.encode('utf-8'))
    for i in range(50):
        ct = encryptionOracle(payload, False)
        ct = ct[16:]
        addToGlobalCts(ct)


def sortPaddedCts():
    global PADDED_CTS
    pairs = []
    order = []
    for i in range(len(PADDED_CTS)):
        for j in range(i):
            if PADDED_CTS[i][16:32] == PADDED_CTS[j][:16]:
                pairs.append((i,j))
            elif PADDED_CTS[i][:16] == PADDED_CTS[j][16:32]:
                pairs.append((j,i))
    
    for i in range(len(pairs)):
        isFirst = True
        for j in range(len(pairs)):
            if pairs[i][0] == pairs[j][1]:
                isFirst = False
        if isFirst:
            order.append(pairs[i][0])
            break
    
    for i in range(len(PADDED_CTS)-1):
        for j in range(len(pairs)):
            if order[i] == pairs[j][0]:
                order.append(pairs[j][1])
                break
    
    tempPaddedPts = PADDED_CTS
    PADDED_CTS = []
    for i in range(len(order)):
        PADDED_CTS.append(tempPaddedPts[order[i]])


def generateDict(initialBytes):
    global PADDED_CTS
    dictionary = []
    for i in range(256):
        newByte = bytes([i])
        pt = initialBytes+newByte
        payload = 'a'*16+'b'+'a'*10
        payload = bytes(payload.encode('utf-8'))
        payload = payload+pt
        ct = PADDED_CTS[1]
        while ct[16:32] != PADDED_CTS[0][:16]:
            ct = encryptionOracle(payload, False)
        dictionary.append(ct[32:48])
    return dictionary


def determineUnknownString():
    blockSize = 16
    strLen = determineStrLen()
    secret = []
    generatePaddedCts()
    sortPaddedCts()
    for i in range(strLen):
        payloadLen = blockSize-1-i%blockSize
        payload = 'a'*16+'b'+'a'*10
        payload += 'a'*payloadLen
        payload = bytes(payload.encode('utf-8'))

        ct = encryptionOracle(payload, False)
        while ct[16:32] != PADDED_CTS[0][:16]:
            ct = encryptionOracle(payload, False)

        startIndex = 32 + (i//16)*16
        ctBlockWithNewLastByte = ct[startIndex: startIndex+16]
        
        payloadForDict = bytes(''.encode('utf-8'))
        try:
            if i < blockSize:
                string = 'a'*payloadLen
                payloadForDict += bytes(string.encode('utf-8'))
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
    string = determineUnknownString()
    string = string.decode('utf-8')
    print(string)


if __name__ == "__main__":
    main()

