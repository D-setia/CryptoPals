import hashlib
import sys
sys.path.insert(1, "../../")
import set5.chall_39.implementRSA as RSA

HASHES = []

def userMenu():
    print("\n1. Submit CT")
    print("2. Exit")
    op = input()
    op = int(op)
    if op != 1 and op != 2:
        raise Exception("Invalid input")
    return op

def initServer():
    global HASHES
    (privateKey, publicKey) = RSA.generateKeyPair()
    e = publicKey[0]
    n = publicKey[1]
    print("e:", e)
    print("n:", n)
    
    op = 0
    while op!=2:
        op = userMenu()
        if op == 1:
            ct = input("CT: ")
            newHash = hashlib.sha1(bytes(ct.encode('latin1'))).digest()
            isReplay = False
            for x in HASHES:
                if x == newHash:
                    isReplay = True
            if isReplay:
                print('\nCT already submitted\n')
            else:
                HASHES.append(newHash)
                ct = int(ct)
                pt = RSA.decryptInt(ct, privateKey)
                print("\nPT:", pt)


def main():
    initServer()


if __name__ == "__main__":
    main()

