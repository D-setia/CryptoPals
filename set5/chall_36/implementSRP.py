import random
import hashlib
import sys
sys.path.insert(1, "../../")
import set4.chall_31.hmac as HMAC
import set5.chall_33.implementDiffieHellman as DiffieHellman


USERS = []
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
    global k, N
    initUsers()
    op = 0

    keyPairB = DiffieHellman.generateKeyPair()
    while(op != 2):
        print("Enter 1 to connect")
        print("Enter 2 to exit")
        op = input()
        try:
            op = int(op)
        except:
            print('Invalid input')
            continue
        else:
            if op == 1:
                I = input('email: ')
                user = getUser(I)
                A = input('A: ')
                A = int(A)
                B = k*user.v + keyPairB[1]
                print('\nSalt:', user.salt)
                print('B:', B, end = '\n\n')

                A_H = hex(A)[2:]
                B_H = hex(B)[2:]
                ip = A_H + B_H
                if len(ip)%2 == 1:
                    ip = '0'+ip
                uH = hashlib.sha256(bytes.fromhex(ip)).hexdigest()
                u = int(uH, 16)
                
                S = pow(A*pow(user.v, u, N), keyPairB[0], N)
                S_H = hex(S)[2:]
                if len(S_H)%2 == 1:
                    S_H = '0'+S_H
                K = hashlib.sha256(bytes.fromhex(S_H)).digest()
                
                hashFunc = hashlib.new('sha256')
                saltH = hex(user.salt)[2:]
                if len(saltH)%2 == 1:
                    saltH = '0'+saltH
                ctReq = HMAC.hmac(bytes.fromhex(saltH), K, hashFunc, hashFunc.block_size, hashFunc.digest_size)
                
                ctIp = input('Enter required CT: ') 
                if ctIp == ctReq.hex():
                    print('\nOK\n\n')
                else:
                    print('\nctReq =', ctReq.hex())
                    print('IP:', ctIp)
                    print('Incorrect\n\n')


def main():
    initServer()


if __name__ == "__main__":
    main()

