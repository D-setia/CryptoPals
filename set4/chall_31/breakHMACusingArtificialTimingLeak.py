import hashlib
import sys
from timeit import default_timer as timer
sys.path.insert(1, "../../")
import set4.chall_31.pseudoWebApp as WebApp


def breakHMACusingTimingLeak(fileName):
    hashFunc = hashlib.new('sha1')
    digestSize = hashFunc.digest_size

    zeroHmac = '\x00'*digestSize
    zeroHmac = bytes(zeroHmac.encode('latin1'))
    forgedMac = []
    for i in range(digestSize):
        print(i)
        timePassed = 0
        nextByte = 0
        for j in range(256):
            testHmac = []
            for k in range(len(forgedMac)):
                testHmac.append(forgedMac[k])
            testHmac.append(j)
            testHmac = bytes(testHmac)
            testHmac += zeroHmac[: digestSize - len(testHmac)]
            start = timer()
            res, timePassedS = WebApp.insecure_compare(fileName, testHmac, (i == digestSize-1)&  (j == 255))
            end = timer()
            if timePassedS > timePassed:
                nextByte = j
                timePassed = timePassedS

        forgedMac.append(nextByte)

    forgedMac = bytes(forgedMac)
    return forgedMac


def main():
    fileName = "input.txt"
    forgedMac = breakHMACusingTimingLeak(fileName)
    print(forgedMac)


if __name__ == "__main__":
    main()

