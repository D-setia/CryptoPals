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


def main():
    andString = binaryStringXor('01001100', '00101010')
    print(andString)
    randBytes = getRandBytes(16)
    print(randBytes)
    print(pow(2,32)-1)
    print(leftRotate(pow(2,32)-1, 30))


if __name__ == "__main__":
    main()
