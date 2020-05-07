import hashlib
import sys
sys.path.insert(1, "../../")
import set4.chall_31.hmac as HMAC


def breakSRPwithZeroKey(email):
    A = 0
    print('A:', A)

    salt = input('Salt: ')
    salt = int(salt)
    saltH = hex(salt)[2:]
    if len(saltH)%2 == 1:
        saltH = '0'+saltH

    S = 0
    S_H = '00'
    K = hashlib.sha256(bytes.fromhex(S_H)).digest()
    hashFunc = hashlib.new('sha256')
    ctReq = HMAC.hmac(bytes.fromhex(saltH), K, hashFunc, hashFunc.block_size, hashFunc.digest_size)

    print("\nCT: "+ctReq.hex()+"\n")



def main():
    email = input("Email: ")
    breakSRPwithZeroKey(email)


if __name__ == "__main__":
    main()

