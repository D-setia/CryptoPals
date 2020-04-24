import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set1.chall_2.fixedXor as ENC
import set2.chall_9.implementPKCS7 as PKCS7
import set2.chall_10.implementCbcMode as AES_CBC

GLOBAL_KEY = None
GLOBAL_IV = None

def encrypt(ipBytes):
    global GLOBAL_KEY
    global GLOBAL_IV

    if GLOBAL_KEY == None:
        GLOBAL_KEY = helpers.getRandBytes(16)
    if GLOBAL_IV == None:
        GLOBAL_IV = GLOBAL_KEY

    ct = AES_CBC.AES_CBCencrypt(PKCS7.PKCS7(ipBytes, 16), GLOBAL_KEY, GLOBAL_IV)
    return ct


def decrypt(ctBytes):
    pt = AES_CBC.AES_CBCdecrypt(ctBytes, GLOBAL_KEY, GLOBAL_IV)
    isValidPadding = PKCS7.PKCS7validate(pt, 16)

    if isValidPadding:
        pad = pt[len(pt)-1]
        pt = pt[:len(pt)-pad]
        try:
            pt.decode('utf-8')
        except:
            print('Error, high value ascii found')
            return pt
        else:
            return None

    else:
        return None
    

def recoverKey():
    payload = 'a'*64
    payload = bytes(payload.encode('latin1'))
    ct = encrypt(payload)

    modifiedCt = ct[:16]
    modifiedCt += bytes(('\x00'*16).encode('latin1'))
    modifiedCt += ct[:16]
    modifiedCt += ct[48:]

    modifiedPt = decrypt(modifiedCt)
    if modifiedPt != None:
        key = ENC.fixedXor(modifiedPt[:16], modifiedPt[32:48])
        return key
    else:
        print('Something went wrong :/')
        return None


def main():
    global GLOBAL_KEY
    key = recoverKey()
    print(key == GLOBAL_KEY)


if __name__ == "__main__":
    main()

