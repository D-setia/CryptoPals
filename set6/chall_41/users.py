import random
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set5.chall_39.implementRSA as RSA


def client(publicKey):
    pt = "This is top secret"
    pt = RSA.stringToInt(pt)
    ct = RSA.encryptInt(pt, publicKey)
    print("\nCT:", ct)

    ptR = input("\nPT_R: ")
    ptR = int(ptR)
    #ptR = RSA.intToStr(ptR)
    if pt == ptR:
        print("\nOK")

def attacker(publicKey):
    n = publicKey[1]
    print("\n\nAttacker Here!")
    capCt = input("CT: ")
    capCt = int(capCt)
    sInv = None
    while sInv == None:
        s = random.randrange(1, n)
        sInv = helpers.modInv(s, n)
    ctS = RSA.encryptInt(s, publicKey)
    ctMod = (ctS*capCt)%n
    print("\nMy CT:", ctMod)
    ptMod = input("\nPT: ")
    ptMod = int(ptMod)
    ptReal = (ptMod*sInv)%n
    ptReal = RSA.intToStr(ptReal)
    print('')
    print(ptReal)

def main():
    e = input("e: ")
    n = input("n: ")
    e = int(e)
    n = int(n)
    publicKey = (e, n)
    client(publicKey)
    attacker(publicKey)


if __name__ == "__main__":
    main()

