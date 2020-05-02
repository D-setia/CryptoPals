import hashlib
import sys
import time
sys.path.insert(1, "../../")
import set1.chall_2.fixedXor as ENC

def hmac(ipBytes, key, hashFunc, blockSize, outputSize):
    opad = bytes(('\x5c'*blockSize).encode('latin1'))
    ipad = bytes(('\x36'*blockSize).encode('latin1'))

    if len(key) > blockSize:
        h = hashFunc.copy()
        h.update(key)
        key = h.digest()
   
    keyPad = '\x00'*(blockSize - len(key))
    keyPad = bytes(keyPad.encode('latin1'))
    key = key + keyPad

    o_key_pad = ENC.fixedXor(key, opad)
    i_key_pad = ENC.fixedXor(key, ipad)

    h = hashFunc.copy()
    h.update(i_key_pad+ipBytes)
    tempHash = h.digest()
    
    h = hashFunc.copy()
    h.update(o_key_pad+tempHash)
    finalHash = h.digest()

    return finalHash


def main():
    ip = 'abcde'
    ip = bytes(ip.encode('latin1'))
    key = 'b'*10
    key = bytes(key.encode('latin1'))
    hashFunc = hashlib.new('sha1')
    mac = hmac(ip, key, hashFunc, hashFunc.block_size, hashFunc.digest_size)
    print(mac)


if __name__ == "__main__":
    main()

