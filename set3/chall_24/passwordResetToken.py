import sys
import time
sys.path.insert(1, "../../")
import set3.chall_21.implementMT19937 as MT19937


def generatePasswordToken():
    tokenLen = 13
    token = []
    MT19937.seed_mt(int(time.time()))
    for i in range(tokenLen):
        randNo = MT19937.extract_number()
        randNo = randNo%256
        token.append(randNo)
    token = bytes(token)
    return token


def testIfTokenGenByMT19937(token):
    timestamp = int(time.time())
    for i in range(10000):
        testSeed = timestamp-i
        MT19937.seed_mt(testSeed)
        isSeed = True
        for j in range(len(token)):
            if token[j] != MT19937.extract_number()%256:
                isSeed = False
        if isSeed:
            return True
            
    return False



def main():
    token = generatePasswordToken()
    wasGen = testIfTokenGenByMT19937(token)
    print(wasGen)

    token = bytes(('a'*15).encode('latin1')) 
    wasGen = testIfTokenGenByMT19937(token)
    print(wasGen)

    #print(token)


if __name__ == "__main__":
    main()

