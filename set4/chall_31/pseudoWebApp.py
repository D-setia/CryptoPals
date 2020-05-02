import hashlib
import sys
import time
from timeit import default_timer as timer
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set4.chall_31.hmac as HMAC

GLOBAL_KEY = None

def generateHMAC(ipBytes):
    global GLOBAL_KEY

    if GLOBAL_KEY == None:
        GLOBAL_KEY = helpers.getRandBytes(16)
    hashFunc = hashlib.new('sha1')
    calcMac = HMAC.hmac(ipBytes, GLOBAL_KEY, hashFunc, hashFunc.block_size, hashFunc.digest_size)
    
    return calcMac


def insecure_compare(fileName , hmac, doPrint):
    ipFile = open(fileName, 'r')
    contents = ipFile.read()
    ipFile.close()

    contents = bytes(contents.encode('latin1'))
    calcMac = generateHMAC(contents)
    if doPrint:
        print(calcMac)
    start = timer()
    for i in range(len(hmac)):
        if hmac[i] != calcMac[i]:
            #print(calcMac[i])
            time.sleep(0.07)
            end = timer()
            return False, (end-start)
        time.sleep(0.07)
    end = timer() 
    return True, (end-start)



def main():
    hmac = '\x5aalskdjaflsdk'
    hmac = bytes(hmac.encode('latin1'))
    res = insecure_compare("input.txt", hmac)
    print(res)



if __name__ == "__main__":
    main()

