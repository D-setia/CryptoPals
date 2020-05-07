import hashlib
import random
import sys
sys.path.insert(1, "../../")
import set4.chall_31.hmac as HMAC
import set5.chall_33.implementDiffieHellman as DiffieHellman

USERS = []
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


class User:

    def __init__(self, email, password):
        global k, g, N
        self.email = email
        self.salt = random.randrange(100, 1000)
        x = getPasswordHash(password, self.salt)
        self.v = pow(g, x, N)


def initUsers():
    USERS.append(User('abc', 'password1'))
    USERS.append(User('def', 'password2'))
    USERS.append(User('ghi', 'password3'))
    USERS.append(User('jkl', 'password4'))
    USERS.append(User('same1', 'password'))
    USERS.append(User('same2', 'password'))


def getUser(email):
    global USERS
    for i in range(len(USERS)):
        if USERS[i].email == email:
            return USERS[i]
    raise Exception('Invalid User')


def initServer():
    global N, g
    initUsers()

    keyPairB = DiffieHellman.generateKeyPair()
    b = keyPairB[0]
    B = keyPairB[1]
    I = input("Email: ")
    user = getUser(I)
    A = input("A: ")
    A = int(A)
    u = random.randrange(0, pow(2, 128))
    print("\nSalt:", user.salt)
    print("B:", B)
    print("\nu:", u, end = "\n\n")

    S = pow(A*pow(user.v, u, N), b, N)
    S_H = hex(S)[2:]
    if len(S_H)%2 == 1:
        S_H = '0'+S_H
    K = hashlib.sha256(bytes.fromhex(S_H)).digest()

    saltH = hex(user.salt)[2:]
    if len(saltH)%2 == 1:
        saltH = '0'+saltH
    hashFunc = hashlib.new('sha256')
    secHash = HMAC.hmac(bytes.fromhex(saltH), K, hashFunc, hashFunc.block_size, hashFunc.digest_size)

    hashIp = input("Hash: ")
    if hashIp == secHash.hex():
        print("\nOK\n")
    else:
        print("\nHashReq:", secHash.hex())
        print("HashIp:", hashIp)
        print("Incorrect\n")


def main():
    initServer()


if __name__ == "__main__":
    main()

