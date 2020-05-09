import random

def getRandBytes(noOfBytes):
    randBytes = []
    for i in range(noOfBytes):
        randBytes.append(random.randrange(0,256))
    randBytes = bytes(randBytes)
    return randBytes


def binaryStringXor(binStr1, binStr2):
    if len(binStr1) != len(binStr2):
        print("Error. Give strings of same length")
        return None
    else:
        xoredString = ''
        for i in range(len(binStr1)):
            if (binStr1[i] == '0' or binStr1[i] == '1') and (binStr2[i] == '0' or binStr2[i] == '1'):
                if binStr1[i] == binStr2[i]:
                    xoredString += '0'
                else:
                    xoredString += '1'
            else:
                print("Error. String contains non-binary characters")
                return None
        return xoredString


def binaryStringAnd(binStr1, binStr2):
    if len(binStr1) != len(binStr2):
        print("Error. Give strings of same length")
        return None
    else:
        andString = ''
        for i in range(len(binStr1)):
            if (binStr1[i] == '0' or binStr1[i] == '1') and (binStr2[i] == '0' or binStr2[i] == '1'):
                if binStr1[i] == binStr2[i] == '1':
                    andString += '1'
                else:
                    andString += '0'
            else:
                print("Error. String contains non-binary characters")
                return None
        return andString


def binaryStringOr(binStr1, binStr2):
    if len(binStr1) != len(binStr2):
        print("Error. Give strings of same length")
        return None
    else:
        orString = ''
        for i in range(len(binStr1)):
            if (binStr1[i] == '0' or binStr1[i] == '1') and (binStr2[i] == '0' or binStr2[i] == '1'):
                if binStr1[i] == binStr2[i] == '0':
                    orString += '0'
                else:
                    orString += '1'
            else:
                print("Error. String contains non-binary characters")
                return None
        return orString


def leftRotate(n, d):
    return ((n << d)|(n >> (32-d))) & 0xffffffff


def rightRotate(n, d):
    return ((n >> d)|(n << (32-d))) & 0xffffffff


def changeEndianness(a):
    res = ((a & 0xff) << 24) | ((a & 0xff00) << 8) | ((a & 0xff0000) >> 8) |((a & 0xff000000) >> 24)
    return res

def modInv(x, N):
    a = []
    b = []
    q = []
    r = []

    A = N
    B = x
    Q = A//B
    R = A%B
    a.append(A)
    b.append(B)
    q.append(Q)
    r.append(R)

    while R != 0:
        A = B 
        B = R
        Q = A//B
        R = A%B
        a.append(A)
        b.append(B)
        q.append(Q)
        r.append(R)
    
    if B != 1:
        return None
    else:
        a.pop()
        b.pop()
        q.pop()
        r.pop()
        inv = 0
        while len(q) > 1:
            q2 = q.pop()
            q1 = q.pop()
            r2 = r.pop()
            r1 = r.pop()
            a2 = a.pop()
            a1 = a.pop()
            b2 = b.pop()
            b1 = b.pop()

            r.append(0-r2)
            b.append(b1)
            q.append(q1*q2 + a2//b1)
            a.append(a1*q2)

        if len(q) == 0:
            inv = 1
        else:
            R = r.pop()
            Q = q.pop()
            if R > 0:
                inv = 0-Q
            else:
                inv = Q
            inv = inv%N

        return inv


def main():
    andString = binaryStringXor('01001100', '00101010')
    #print(andString)
    randBytes = getRandBytes(16)
    #print(randBytes)
    #print(pow(2,32)-1)
    #print(leftRotate(pow(2,32)-1, 30)) 
    for j in range(20, 100):
        for i in range(1, j):
            inv = modInv(i, j)
            if inv != None:
                print((i*inv)%j)

        print('')
    


if __name__ == "__main__":
    main()
