import math
import random
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set3.chall_21.implementMT19937 as MT19937


def MT19937cipher(ipBytes, seed):
    seedSizeInBits = 16 
    seed = (bin(abs(seed))[2:]).zfill(seedSizeInBits)
    seed = int(seed[len(seed)-seedSizeInBits:], 2)
    MT19937.seed_mt(seed)

    output = []
    for i in range(len(ipBytes)):
        randNo = MT19937.extract_number()
        randNo = randNo%256
        output.append(randNo^ipBytes[i])
    output = bytes(output)
    return output


def encrypt(ptBytes, seed=None):
    if seed == None:
        seed = random.randrange(0, pow(2,20))
    #print(seed%pow(2,16))
    noOfRandBytes = random.randrange(10, 20)
    ipBytes = helpers.getRandBytes(noOfRandBytes) + ptBytes
    ct = MT19937cipher(ipBytes, seed)
    return ct


def decrypt(ctBytes, seed):
    pt = MT19937cipher(ctBytes, seed)
    return pt



def main():
    for i in range(20):
        seed = random.randrange(0, pow(2,20))
        a = encrypt(bytes('abcde'.encode('latin1')), seed)
        b = decrypt(a, seed)
        if b[len(b)-5:] != bytes('abcde'.encode('latin1')):
            print('Error!')


if __name__ == "__main__":
    main()

