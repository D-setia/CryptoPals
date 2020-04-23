import base64
import random
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set3.chall_18.implementCtrMode as AES_CTR

GLOBAL_KEY = None
GLOBAL_NONCE = None

def encryptUnknownPt():
    global GLOBAL_NONCE
    global GLOBAL_KEY 
    ipFile = open("input.txt", 'r')
    contents = ipFile.read().replace('\n', '')
    pt = base64.b64decode(contents)
    ipFile.close()

    if GLOBAL_KEY == None:
        GLOBAL_KEY = helpers.getRandBytes(16)
    if GLOBAL_NONCE == None:
        GLOBAL_NONCE = random.randrange(0, pow(2,64))

    ct = AES_CTR.AES_CTR(pt, GLOBAL_KEY, GLOBAL_NONCE)
    return ct, pt


def edit(ctBytes, offset, newText):
    global GLOBAL_KEY
    global GLOBAL_NONCE
    modifiedCt = AES_CTR.AES_CTR_edit(ctBytes, GLOBAL_KEY, GLOBAL_NONCE, offset, newText)
    return modifiedCt


def breakRandAccessRW_AES_CTR(ct):
    offset = 0
    payloadLen = len(ct)
    payload = 'a'*payloadLen
    payload = bytes(payload.encode('latin1'))

    newCt = edit(ct, offset, payload)
    pt = []
    for i in range(offset, len(newCt)):
        keyStreamByte = payload[i-offset]^newCt[i]
        originalPtByte = keyStreamByte^ct[i]
        pt.append(originalPtByte)

    pt = bytes(pt)
    return pt


def main():
    ct, ptOrg = encryptUnknownPt()
    pt = breakRandAccessRW_AES_CTR(ct)
    print(pt == ptOrg)


if __name__ == "__main__":
    main()

