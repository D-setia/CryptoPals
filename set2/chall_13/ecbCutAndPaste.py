import random
import sys
sys.path.insert(1, "../../")
import set1.chall_7.aesInEcbMode as AES_ECB
import set2.chall_9.implementPKCS7 as PKCS7

GLOBAL_KEY = None

def parse(string):
    myDict = {}
    maps = string.split('&')
    for x in maps:
        temp = x.split('=')
        myDict[temp[0]] = temp[1]
    return myDict

def getRandBytes(noOfBytes):
    randBytes = []
    for i in range(noOfBytes):
        randBytes.append(random.randrange(0,256))
    randBytes = bytes(randBytes)
    return randBytes


def checkForMetachars(string):
    hasMetaChars = False
    for char in string:
        if char == '=' or char == '&':
            hasMetaChars = True
    return hasMetaChars


def profile_for(email):
    hasMetaChars = checkForMetachars(email)
    if hasMetaChars:
        print("Invalid Id")
        return None
    else:
        global GLOBAL_KEY
        if GLOBAL_KEY == None:
            GLOBAL_KEY = getRandBytes(16)

        uid = random.randrange(100,1001)
        uid = str(uid)
        encodedUser = "email="+email+"&uid="+uid+"&role=user"
        encodedUser = bytes(encodedUser.encode('utf-8'))
        ct = AES_ECB.AESencrypt(PKCS7.PKCS7(encodedUser, 16),GLOBAL_KEY)
        return ct

def decrypt(ctBytes):
    global GLOBAL_KEY
    pt = AES_ECB.AESdecrypt(ctBytes, GLOBAL_KEY)
    pad = pt[len(pt)-1]
    isValidPad = True
    for i in range(pad):
        if pt[len(pt)-1-i] != pad:
            isValidPad = False

    if isValidPad:
        pt = pt[:len(pt)-pad]
        return pt
    else:
        return None


def generateAdminProfile():
    payload = "ab@gmail.com"
    ct1 = profile_for(payload)
    payload = 'a'*10+'admin'+'\x0b'*11+"@gmail.com"
    ct2 = profile_for(payload)
    customCt = ct1[:32]+ct2[16:32]

    return customCt



def main():
    ct = generateAdminProfile()
    pt = decrypt(ct)
    pt = pt.decode('utf-8')
    userObj = parse(pt)
    print(userObj)

    #ct = profile_for("foorbar@gmail.com")
    #pt = decrypt(ct)
    #userObj = parse(pt.decode('utf-8'))
    #print(userObj)



if __name__ == "__main__":
    main()
