import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers


def addSHApadding(ipBytes, prefixLenInBytes = 0):
    length = (len(ipBytes) + prefixLenInBytes)*8
    padLenInBits = 448 - length%512
    if padLenInBits <= 0:
        padLenInBits += 512
    padLen = padLenInBits//8
    pad = '\x80'+'\x00'*(padLen-1)
    pad = bytes(pad.encode('latin1'))

    messageLenPad = (bin(length)[2:]).zfill(64)
    messageLenPad = messageLenPad[len(messageLenPad)-64:]
    for i in range(8):
        pad += bytes([int(messageLenPad[i*8 : (i+1)*8], 2)])

    paddedIp = ipBytes+pad
    return paddedIp


def sha1(ipBytes, prefixLenInBytes=0, h0_i=0x67452301, h1_i=0xEFCDAB89, h2_i=0x98BADCFE, h3_i=0x10325476, h4_i=0xC3D2E1F0):
    h0 = h0_i
    h1 = h1_i
    h2 = h2_i
    h3 = h3_i
    h4 = h4_i

    paddedIp = addSHApadding(ipBytes, prefixLenInBytes)
    
    words = [0 for i in range(80)]
    for i in range((len(paddedIp)*8)//512):
        chunk = paddedIp[i*64: (i+1)*64]
        for j in range(16):
            temp = chunk[j*4: (j+1)*4]
            words[j] = int(temp.hex(), 16)
             
        for j in range(16, 80):
            temp = words[j-3] ^ words[j-8] ^ words[j-14]^ words[j-16]
            words[j] = helpers.leftRotate(temp, 1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for j in range(80):
            if j in range(20):
                f = (b & c) | ((~b) & d)
                k = 0x5a827999
            elif j in range(20, 40):
                f = b ^ c ^ d
                k = 0x6ed9eba1
            elif j in range(40, 60):
                f = (b & c) | (b & d) | (c & d)
                k = 0x8f1bbcdc
            elif j in range(60, 80):
                f = b ^ c ^ d
                k = 0xca62c1d6

            temp = (helpers.leftRotate(a, 5) + f + e + k + words[j]) & 0xffffffff
            e = d
            d = c
            c = helpers.leftRotate(b, 30)
            b = a
            a = temp

        h0 = (h0+a) & 0xffffffff
        h1 = (h1+b) & 0xffffffff
        h2 = (h2+c) & 0xffffffff
        h3 = (h3+d) & 0xffffffff
        h4 = (h4+e) & 0xffffffff

    finalHashInt = (h0 << 128) | (h1 << 96)  | (h2 << 64) | (h3 << 32) | h4
    
    h0B = bytes.fromhex((hex(h0)[2:]).zfill(8))
    h1B = bytes.fromhex((hex(h1)[2:]).zfill(8))
    h2B = bytes.fromhex((hex(h2)[2:]).zfill(8))
    h3B = bytes.fromhex((hex(h3)[2:]).zfill(8))
    h4B = bytes.fromhex((hex(h4)[2:]).zfill(8))
    
    finalHashBytes = h0B + h1B + h2B + h3B + h4B 
    #print(bytes.fromhex(hex(finalHashInt)[2:]))
    
    return finalHashBytes




def main():
    ip = bytes(('a'*7).encode('latin1'))
    paddedIp = addSHApadding(ip, 60)
    myHash = sha1(ip)
    print(myHash)



if __name__ == "__main__":
    main()

