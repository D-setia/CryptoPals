import random
import sys
sys.path.insert(1, "../../")
import set2.chall_9.implementPKCS7 as PKCS7
import set2.chall_10.implementCbcMode as AES_CBC

GLOBAL_KEY = None
IV = None

def getRandBytes(noOfBytes):
    randBytes = []
    for i in range(noOfBytes):
        randBytes.append(random.randrange(0,256))
    randBytes = bytes(randBytes)
    return randBytes

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


def encrypt(userInputString):
    global GLOBAL_KEY
    global IV
    if GLOBAL_KEY == None:
        GLOBAL_KEY = getRandBytes(16)
    if IV == None:
        IV = getRandBytes(16)
    
    userInputString = quoteMetachars(userInputString)
    stringToPrepend = "comment1=cooking%20MCs;userdata="
    stringToAppend = ";comment2=%20like%20a%20pound%20of%20bacon"
    finalString = stringToPrepend + userInputString + stringToAppend
    
    ipBytes = bytes(finalString.encode('utf-8'))
    ct = AES_CBC.AES_CBCencrypt(PKCS7.PKCS7(ipBytes, 16), GLOBAL_KEY, IV)
    return ct



def checkForAdminTuple(ptString):
    isPresent = False
    pairs = ptString.split(';')
    for x in pairs:
        touple = x.split('=')
        if touple[0] == "admin":
            isPresent = True

    return isPresent


def decryptAndCheckForAdmin(ctBytes):
    pt = AES_CBC.AES_CBCdecrypt(ctBytes, GLOBAL_KEY, IV)
    isValidPadding = PKCS7.PKCS7validate(pt, 16)
    if isValidPadding:
        pad = pt[len(pt)-1]
        pt = pt[:len(pt)-pad]
        isAdminTuplePresent = checkForAdminTuple(pt.decode('latin1'))
        #TODO: find how to change to pt.decode('utf-8')
        return isAdminTuplePresent
    else:
        return None


def getAdminAccess():
    payload = 'a'*16 
    payload += 'aa'+'x'+'admin'+'y'+'true'+'x'+'aa'
    ct = encrypt(payload)
    modifiedCt = ct[:34]
    modifiedCt += bytes([120^59^ct[34]])
    modifiedCt += ct[35:40]
    modifiedCt += bytes([121^61^ct[40]])
    modifiedCt += ct[41:45]
    modifiedCt += bytes([120^59^ct[45]])
    modifiedCt += ct[46:]

    isAdmin = decryptAndCheckForAdmin(modifiedCt)
    print(isAdmin)


def main():
    getAdminAccess()
    

if __name__ == "__main__":
    main()

