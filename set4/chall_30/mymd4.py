import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers

def addMD4padding(ipBytes, prefixLenInBytes = 0):
    length = (len(ipBytes) + prefixLenInBytes)*8
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

    pad += lenPad[4:]
    pad += lenPad[:4]

    paddedIp = ipBytes+pad
    return paddedIp

def changeEndianness(a):
    res = ((a & 0xff) << 24) | ((a & 0xff00) << 8) | ((a & 0xff0000) >> 8) |((a & 0xff000000) >> 24)
    return res


def F(x, y, z):
    return ((x & y) | ((~x) & z)) & 0xffffffff

def G(x, y, z):
    return ((x & y) | (x & z) | (y & z)) & 0xffffffff

def H(x, y, z):
    return (x^y^z) & 0xffffffff

def md4(ipBytes, prefixLenInBytes=0, A_i=0x01234567, B_i=0x89abcdef, C_i=0xfedcba98, D_i=0x76543210):
    
    #67452301  01234567
    #efcdab89  89abcdef
    #98badcfe  fedcba98
    #10325476  76543210
    A = changeEndianness(A_i)
    B = changeEndianness(B_i)
    C = changeEndianness(C_i)
    D = changeEndianness(D_i)

    paddedIp = addMD4padding(ipBytes, prefixLenInBytes)
    X = [0 for i in range(16)]

    for i in range(len(paddedIp)//64):
        chunk = paddedIp[i*64: (i+1)*64]
        for j in range(16):
            temp = chunk[j*4 : (j+1)*4]
            X[j] = int((temp.hex()).zfill(8), 16)
            if i*64+j*4 < len(paddedIp)-8:
                X[j] = changeEndianness(X[j])

        
        AA = A
        BB = B
        CC = C
        DD = D
        
        #Round 1
        for k in range(16):
            # [abcd k s]
            s = (k%4)*4 + 3
            if s == 15:
                s += 4

            if k%4 == 0:
                temp = (A + F(B, C, D) + X[k]) & 0xffffffff
                A = helpers.leftRotate(temp , s)
            if k%4 == 1:
                temp = (D + F(A, B, C) + X[k]) & 0xffffffff
                D = helpers.leftRotate(temp, s)
            if k%4 == 2:
                temp = (C + F(D, A, B) + X[k]) & 0xffffffff
                C = helpers.leftRotate(temp, s)
            if k%4 == 3:
                temp = (B + F(C, D, A) + X[k]) & 0xffffffff
                B = helpers.leftRotate(temp, s)

        #Round 2
        for j in range(4):
            for k in range(4):
                s = (k+1)*4 - 3
                if s == 1:
                    s = 3

                #9979825a 
                if k%4 == 0:
                    temp = (A + G(B, C, D) + X[k*4+j] + 0x5a827999) & 0xffffffff
                    A = helpers.leftRotate(temp , s)
                if k%4 == 1:
                    temp = (D + G(A, B, C) + X[k*4+j] + 0x5a827999) & 0xffffffff
                    D = helpers.leftRotate(temp, s)
                if k%4 == 2:
                    temp = (C + G(D, A, B) + X[k*4+j] + 0x5a827999) & 0xffffffff
                    C = helpers.leftRotate(temp, s)
                if k%4 == 3:
                    temp = (B + G(C, D, A) + X[k*4+j] + 0x5a827999) & 0xffffffff
                    B = helpers.leftRotate(temp, s)
       
        #Round 3
        for j in range(4):
            if j == 1: 
                j1 = 2
            elif j == 2:
                j1 = 1
            else:
                j1 = j

            for k in range(4):
                if k == 1:
                    k1 = 2
                elif k == 2:
                    k1 = 1
                else:
                    k1 = k
                
                s = (k+1)*4 - 1
                if s == 7:
                    s = 9

                if k%4 == 0:
                    temp = (A + H(B, C, D) + X[k1*4+j1] + 0x6ed9eba1) & 0xffffffff
                    A = helpers.leftRotate(temp , s)
                if k%4 == 1:
                    temp = (D + H(A, B, C) + X[k1*4+j1] + 0x6ed9eba1) & 0xffffffff
                    D = helpers.leftRotate(temp, s)
                if k%4 == 2:
                    temp = (C + H(D, A, B) + X[k1*4+j1] + 0x6ed9eba1) & 0xffffffff
                    C = helpers.leftRotate(temp, s)
                if k%4 == 3:
                    temp = (B + H(C, D, A) + X[k1*4+j1] + 0x6ed9eba1) & 0xffffffff
                    B = helpers.leftRotate(temp, s)
       
        A = (A + AA) & 0xffffffff
        B = (B + BB) & 0xffffffff
        C = (C + CC) & 0xffffffff
        D = (D + DD) & 0xffffffff


    A_B = bytes.fromhex((hex(changeEndianness(A))[2:]).zfill(8))
    B_B = bytes.fromhex((hex(changeEndianness(B))[2:]).zfill(8))
    C_B = bytes.fromhex((hex(changeEndianness(C))[2:]).zfill(8))
    D_B = bytes.fromhex((hex(changeEndianness(D))[2:]).zfill(8))

    #finalHashBytes = A_B[::-1] + B_B[::-1] + C_B[::-1] + D_B[::-1]
    finalHashBytes = A_B + B_B + C_B + D_B
    #finalHashBytes = D_B + C_B + B_B + A_B
    return finalHashBytes



def main():
    testCases = [('', '31d6cfe0d16ae931b73c59d7e0c089c0'), ('a', 'bde52cb31de33e46245e05fbdbd6fb24'), ('abc', 'a448017aaf21d8525fc10ae87aa6729d')]
    for x in testCases:
        ip = x[0]
        ip = bytes(ip.encode('latin1'))
        myHash = md4(ip)
        print(myHash.hex() == x[1])


if __name__ == "__main__":
    main()

