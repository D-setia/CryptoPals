
def PKCS7(ipByteArr, blockSize):
    noToAppend = blockSize - len(ipByteArr)
    paddedResult = []
    for i in range(len(ipByteArr)+noToAppend):
        if i < len(ipByteArr):
            paddedResult.append(ipByteArr[i])
        else:
            paddedResult.append(noToAppend)
    
    paddedResult = bytes(paddedResult)
    return paddedResult

def main():
    ip = "YELLOW SUBMARINE"
    blocksize = 20

    ip = bytes(ip.encode('utf-8'))
    paddedIp = PKCS7(ip, blocksize)
    print(paddedIp)


if __name__ == "__main__":
    main()
