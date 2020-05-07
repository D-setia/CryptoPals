import hashlib
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


def initComm(email, password):
    keyPairA = DiffieHellman.generateKeyPair()
    a = keyPairA[0]
    A = keyPairA[1]
    print("\nA:", A)

    salt = input("\nSalt: ")
    salt = int(salt)
    B = input("B: ")
    B = int(B)
    u = input("\nu: ")
    u = int(u)
    
    x = getPasswordHash(password, salt)
    S = pow(B, a+u*x, N)
    
    S_H = hex(S)[2:]
    if len(S_H)%2 == 1:
        S_H = '0'+S_H
    K = hashlib.sha256(bytes.fromhex(S_H)).digest()

    saltH = hex(salt)[2:]
    if len(saltH)%2 == 1:
        saltH = '0'+saltH
    hashFunc = hashlib.new('sha256')
    secHash = HMAC.hmac(bytes.fromhex(saltH), K, hashFunc, hashFunc.block_size, hashFunc.digest_size)
    print("SecHash:", secHash.hex())


def main():
    email = input("Email: ")
    password = input("Password: ")
    initComm(email, password)


if __name__ == "__main__":
    main()

