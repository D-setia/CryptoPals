import random
import time
import sys
sys.path.insert(1, "../../")
import set3.chall_21.implementMT19937 as MT19937

def crackSeed():
    seed = 0
    randWait = random.randrange(40, 1001)
    time.sleep(randWait)
    realSeed = int(time.time())
    print(realSeed)
    MT19937.seed_mt(realSeed)
    randWait = random.randrange(40, 1001)
    time.sleep(randWait)
    
    val = MT19937.extract_number()
    currTime = int(time.time())
    rangeOfVals = 0
    while seed == 0:
        for i in range(rangeOfVals, rangeOfVals+100000):
            testSeed = currTime - i
            MT19937.seed_mt(testSeed)
            firstVal = MT19937.extract_number()
            if firstVal == val:
                seed = testSeed
                break
        if seed !=0:
            return seed
        rangeOfVals += 100000
        print('NewVals')
    return None


def main():
    seed = crackSeed()
    print(seed)


if __name__ == "__main__":
    main()

