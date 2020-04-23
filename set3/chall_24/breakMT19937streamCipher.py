import sys
sys.path.insert(1, "../../")
import set3.chall_21.implementMT19937 as MT19937
import set3.chall_24.implementMT19937streamCipher as MT19937cipher


def breakMT19937cipher():
    seedLenInBits = 16 
    payloadLen = 14
    payload = 'a'*payloadLen
    payload = bytes(payload.encode('latin1'))
    ct = MT19937cipher.encrypt(payload)
    
    seed = None
    for i in range(pow(2, seedLenInBits)):
        pt = MT19937cipher.decrypt(ct, i)
        if pt[len(pt)-payloadLen:] == payload:
            seed = i
            break

    return seed


def main():
    seed = breakMT19937cipher()
    print(seed)


if __name__ == "__main__":
    main()

