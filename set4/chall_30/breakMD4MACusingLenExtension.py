import random
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set4.chall_30.mymd4 as myMD4
import set4.chall_30.implementMD4keyedMAC as MD4keyedMAC

KEY_LEN = None
GLOBAL_KEY = None

def generateMAC(ipBytes):
    global KEY_LEN
    global GLOBAL_KEY

    if KEY_LEN == None:
        KEY_LEN = random.randrange(7,20)
        #print(KEY_LEN)
    if GLOBAL_KEY == None:
        GLOBAL_KEY = helpers.getRandBytes(KEY_LEN)

    mac = MD4keyedMAC.MD4MAC(ipBytes, GLOBAL_KEY)
    return mac


def addGluePadding(ipBytes, keySizeInBytes):
    length = (len(ipBytes) + keySizeInBytes)*8
    padLenInBits = 448 - length%512
    if padLenInBits <= 0:
        padLenInBits += 512
    padLen = padLenInBits//8
    pad = '\x80'+'\x00'*(padLen-1)
    pad = bytes(pad.encode('latin1'))

    messageLenPad = (bin(length)[2:]).zfill(64)
    messageLenPad = messageLenPad[len(messageLenPad)-64:]
    lenPad = bytes(''.encode('latin1'))
    for i in range(8):
        lenPad += bytes([int(messageLenPad[i*8 : (i+1)*8], 2)])

    pad += (lenPad[4:])[::-1]
    pad += (lenPad[:4])[::-1]
    paddedIp = ipBytes+pad
    return paddedIp


def forgeHash(originalTextString, newTextString):
    ip = originalTextString
    ip = bytes(ip.encode('latin1'))
    legitMac = generateMAC(ip)

    h = [0 for i in range(4)]
    for i in range(4):
        h[i] = int((legitMac[i*4: (i+1)*4]).hex(), 16)

    keySize = 0
    for i in range(5, 33):
        paddedIp = addGluePadding(ip, i)
        payload = bytes(newTextString.encode('latin1'))
        prefixLenInBytes = len(paddedIp) + i

        legitMac2 = generateMAC(paddedIp+payload)
        forgedMac = myMD4.md4(payload, prefixLenInBytes, h[0], h[1], h[2], h[3])
        
        if legitMac2 == forgedMac:
            keySize = i
            validText = paddedIp + payload
            return validText, forgedMac, keySize

    return None, None, None
    


def main():
    originalText = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    newText = ";admin=true"
    validText, forgedHash, keySize = forgeHash(originalText, newText)
    legitHash = generateMAC(validText)
    print(legitHash)
    print(forgedHash)
    #print(keySize)


if __name__ == "__main__":
    main()

