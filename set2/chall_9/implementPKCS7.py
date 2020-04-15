
def PKCS7(ipByteArr, blockSize):
    noToAppend = blockSize - len(ipByteArr)%blockSize
    paddedResult = []
    for i in range(len(ipByteArr)+noToAppend):
        if i < len(ipByteArr):
            paddedResult.append(ipByteArr[i])
        else:
            paddedResult.append(noToAppend)
    
    paddedResult = bytes(paddedResult)
    return paddedResult


def PKCS7validate(paddedPtBytes):
    isValid = True
    pad = paddedPtBytes[len(paddedPtBytes)-1]
    for i in range(pad):
        if paddedPtBytes[len(paddedPtBytes)-1-i] != pad:
            isValid = False
    return isValid

def main():
    ip = "YELLOW SUBMARINE"
    blocksize = 16

    ip = bytes(ip.encode('utf-8'))
    paddedIp = PKCS7(ip, blocksize)
    isValid = PKCS7validate(paddedIp)
    print(isValid)
    print(paddedIp)


if __name__ == "__main__":
    main()
