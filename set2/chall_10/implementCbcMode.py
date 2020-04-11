import base64
import sys
sys.path.insert(1, "../../")
import set1.chall_2.fixedXor as xorEnc
import set1.chall_7.aesInEcbMode as AES_ECB
import set2.chall_9.implementPKCS7 as PKCS7

def AES_CBCencrypt(ptByteArray, key, IV):
    paddedPt = PKCS7.PKCS7(ptByteArray, 16)
    prevCt = IV
    ct = [] 
    for i in range(len(paddedPt)//16):
        ptInput = xorEnc.fixedXor(paddedPt[i*16:(i+1)*16], prevCt)
        newCtBlock = AES_ECB.AESencrypt(ptInput, key)
        for j in range(len(newCtBlock)):
            ct.append(newCtBlock[j])
        prevCt = newCtBlock
    
    ct = bytes(ct)
    return ct

def AES_CBCdecrypt(ctByteArray, key, IV):
    pt = []
    for i in range(len(ctByteArray)//16):
        ctInputBlock = ctByteArray[len(ctByteArray)-(i+1)*16 : len(ctByteArray) - i*16]
        temp = AES_ECB.AESdecrypt(ctInputBlock, key)
        
        newPtBlock = 0
        if i == (len(ctByteArray)//16 -1):
            newPtBlock = xorEnc.fixedXor(temp, IV)
        else:
            prevCtBlock = ctByteArray[len(ctByteArray)-(i+2)*16 : len(ctByteArray) - (i+1)*16]
            newPtBlock = xorEnc.fixedXor(temp, prevCtBlock)

        for j in range(len(newPtBlock)):
            pt.append(newPtBlock[len(newPtBlock) -j -1])

    pt = pt[::-1]
    
    pad = pt[len(pt)-1]
    isValidPad = True
    for i in range(pad):
        if pt[len(pt) -1 -i] != pad:
            isValidPad = False

    if isValidPad:
        pt = pt[:len(pt)-pad]
        pt = bytes(pt)
        return pt
    else:
        print("Invalid Pad")
        return None


def main():
    key = "YELLOW SUBMARINE"
    ipFile = open("input.txt", 'r')
    contents = ''
    for line in ipFile:
        contents += line[:len(line)-1]
    ipFile.close()

    key = bytes(key.encode('utf-8'))
    contents = base64.b64decode(contents)
    IV = '\x00'*16
    IV = bytes(IV.encode('utf-8'))
    ct = AES_CBCdecrypt(contents, key, IV)
    if ct != None:
        ct = ct.decode('utf-8')
        print(ct)
        #pt = AES_CBCencrypt(ct.encode('utf-8'), key, IV)
        #print(pt)
    #print(contents)



if __name__ == "__main__":
    main()
