import random
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set3.chall_18.implementCtrMode as AES_CTR

GLOBAL_KEY = None
GLOBAL_NONCE = None

def quoteMetachars(string):
    safeString = ""

    for i in range(len(string)):
        if string[i] == '=':
            safeString += '%3D'
        elif string[i] == ';':
            safeString += '%3B'
        else:
            safeString += string[i]

    return safeString


def checkForAdminTuple(ptString):
    isPresent = False
    pairs = ptString.split(';')
    for x in pairs:
        touple = x.split('=')
        if touple[0] == "admin":
            isPresent = True

    return isPresent


def encrypt(ipString):
    global GLOBAL_KEY
    global GLOBAL_NONCE
    stringToPrepend = "comment1=cooking%20MCs;userdata="
    stringToAppend = ";comment2=%20like%20a%20pound%20of%20bacon"
    
    if GLOBAL_KEY == None:
        GLOBAL_KEY = helpers.getRandBytes(16)
    if GLOBAL_NONCE == None:
        GLOBAL_NONCE = random.randrange(0, pow(2,64))
    
    modifiedIp = quoteMetachars(ipString)
    modifiedIp = stringToPrepend + modifiedIp + stringToAppend
    ipBytes = bytes(modifiedIp.encode('latin1'))

    ct = AES_CTR.AES_CTR(ipBytes, GLOBAL_KEY, GLOBAL_NONCE)
    return ct


def decryptAndCheckForAdmin(ctBytes):
    pt = AES_CTR.AES_CTR(ctBytes, GLOBAL_KEY, GLOBAL_NONCE)
    ptString = pt.decode('latin1')
    isAdmin = checkForAdminTuple(ptString)
    return isAdmin


def getAdminAccess():
    payload = 'a_admin_true'
    ct = encrypt(payload)
    
    modifiedCt = ct[:33]
    modifiedCt += bytes([ct[33]^95^59])
    modifiedCt += ct[34:39]
    modifiedCt += bytes([ct[39]^95^61])
    modifiedCt += ct[40:]

    isAdmin = decryptAndCheckForAdmin(modifiedCt)
    return isAdmin

def main():
    isAdmin = getAdminAccess()
    print(isAdmin)


if __name__ == "__main__":
    main()

