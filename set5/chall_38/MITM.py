import hashlib
import random
import sys
sys.path.insert(1, "../../")
import set4.chall_31.hmac as HMAC
import set5.chall_33.implementDiffieHellman as DiffieHellman

g = DiffieHellman.g
N = DiffieHellman.p

def getPasswordHash(passwordString, salt):
    saltedPassword = hex(salt)[2:] + passwordString
    passBytes = bytes(saltedPassword.encode('latin1'))
    hashString = hashlib.sha256(passBytes).hexdigest()
    if len(hashString)%2 == 1:
        hashString = '0'+hashString
    passHashInt = int(hashString, 16)
    return passHashInt


def doMITMattack():
    keyPairB = DiffieHellman.generateKeyPair()
    b = keyPairB[0]
    B = keyPairB[1]
    email = input("Email: ")
    A = input("A: ")
    A = int(A)

    salt = 0
    u = 1
    print("\nSalt:", salt)
    print("B:", B)
    print("\nu:", u)

    secHash = input("\nHash: ")

    passDict = open("dict.txt", 'r')
    for line in passDict:
        password = line[: len(line)-1]
        x = getPasswordHash(password, salt)
        v = pow(g, x, N)
        S = pow(A*pow(v, u, N), b, N)
        S_H = hex(S)[2:]
        if len(S_H)%2 == 1:
            S_H = '0'+S_H
        K = hashlib.sha256(bytes.fromhex(S_H)).digest()

        saltH = hex(salt)[2:]
        if len(saltH)%2 == 1:
            saltH = '0'+saltH
        hashFunc = hashlib.new('sha256')
        generatedHash = HMAC.hmac(bytes.fromhex(saltH), K, hashFunc, hashFunc.block_size, hashFunc.digest_size)

        if generatedHash.hex() == secHash:
            print("\nPassword is:      ", password)
            break




def main():
    doMITMattack()


if __name__ == "__main__":
    main()

