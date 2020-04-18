import base64
import math
import sys
sys.path.insert(1, "../../")
import helperFunctions as helper
import set1.chall_2.fixedXor as ENC
import set1.chall_7.aesInEcbMode as AES_ECB
import set2.chall_9.implementPKCS7 as PKCS7

def get64BitLittleEndianBytes(a):
    a = bin(a)
    a = a[2:]
    a = a.zfill(64)
    a = a[len(a)-64:len(a)]

    bigEndianBytes = bytes(''.encode('utf-8'))
    for i in range(8):
        byte = a[i*8: (i+1)*8]
        byte = bytes([int(byte, 2)])
        bigEndianBytes += byte

    littleEndianBytes = bigEndianBytes[::-1] 
    return littleEndianBytes


def AES_CTR(ipBytes, key, nonce):
    blockSize = 16
    nonce = get64BitLittleEndianBytes(nonce)
    noOfBlocks = math.ceil(len(ipBytes)/blockSize)

    opBytes = bytes(''.encode('utf-8'))
    for i in range(noOfBlocks):
        ctr = get64BitLittleEndianBytes(i)
        ipToAes = nonce+ctr
        encryptedCtr = AES_ECB.AESencrypt(ipToAes, key)    
        if i == noOfBlocks-1:
            op = ENC.fixedXor(encryptedCtr[:len(ipBytes)%blockSize], ipBytes[i*blockSize: i*blockSize + len(ipBytes)%blockSize])
            opBytes += op
        else:
            op = ENC.fixedXor(encryptedCtr, ipBytes[i*blockSize: (i+1)*blockSize])
            opBytes += op

    return opBytes


def main():
    key = "YELLOW SUBMARINE"
    key = bytes(key.encode('utf-8'))
    nonce = 0
    ip = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    ip = base64.b64decode(ip)
    decrypted = AES_CTR(ip, key, nonce)
    print(decrypted)

if __name__ == "__main__":
    main()

