import hashlib
import random
import sys
sys.path.insert(1, "../../")
import set4.chall_31.hmac as HMAC
import set5.chall_33.implementDiffieHellman as DiffieHellman

k = 3
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
    global k, g, N

    keyPairA = DiffieHellman.generateKeyPair()
    a = keyPairA[0]
    A = keyPairA[1]
    print('Email:', email)
    print('A:', A)
    print('')
    salt = input('Salt: ')
    salt = int(salt)
    B = input('B: ')
    B = int(B)

    A_H = hex(A)[2:]
    B_H = hex(B)[2:]
    ip = A_H + B_H
    if len(ip)%2 == 1:
        ip = '0'+ip
    uH = hashlib.sha256(bytes.fromhex(ip)).hexdigest()
    u = int(uH, 16)
    #print('U:', u)

    x = getPasswordHash(password, salt)
    #print('X:', x)
    S = pow(B - k*pow(g, x, N), a+u*x, N)
    S_H = hex(S)[2:]
    if len(S_H)%2 == 1:
        S_H = '0'+S_H
    K = hashlib.sha256(bytes.fromhex(S_H)).digest()

    hashFunc = hashlib.new('sha256')
    saltH = hex(salt)[2:]
    if len(saltH)%2 == 1:
        saltH = '0'+saltH
    ctReq = HMAC.hmac(bytes.fromhex(saltH), K, hashFunc, hashFunc.block_size, hashFunc.digest_size)

    print('')
    print('CT:', ctReq.hex())
    print('')




def main():
    initComm('abc', 'password1')


if __name__ == "__main__":
    main()

