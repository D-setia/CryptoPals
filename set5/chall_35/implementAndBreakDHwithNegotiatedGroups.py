import hashlib
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set2.chall_9.implementPKCS7 as PKCS7
import set2.chall_10.implementCbcMode as AES_CBC
import set5.chall_33.implementDiffieHellman as DiffieHellman


def DHwithNegotiatedGroups(p, g):
    print('g =', g, end = '\n\n')
    keyPairA = DiffieHellman.generateKeyPair(p, g)
    A = keyPairA[1]
    print("A to B: p, g")
    print("B to A: ACK")
    keyPairB = DiffieHellman.generateKeyPair(p, g)
    B = keyPairB[1]
    print("A to B: A")
    print("B to A: B")

    secretKeyA = DiffieHellman.DH(B, keyPairA, p)
    secretKeyA_hex = hex(secretKeyA)[2:]
    secretKeyA_hex = secretKeyA_hex if len(secretKeyA_hex)%2 == 0 else '0'+secretKeyA_hex
    secretKeyA_bytes = bytes.fromhex(secretKeyA_hex)
    AESkeyA = hashlib.sha1(secretKeyA_bytes).digest()[:16]

    secretKeyB = DiffieHellman.DH(A, keyPairB, p)
    secretKeyB_hex = hex(secretKeyB)[2:]
    secretKeyB_hex = secretKeyB_hex if len(secretKeyB_hex)%2 == 0 else '0'+secretKeyB_hex
    secretKeyB_bytes = bytes.fromhex(secretKeyB_hex)
    AESkeyB = hashlib.sha1(secretKeyB_bytes).digest()[:16]

    if g == 1:
        print(secretKeyA == 1, end = '\n\n\n')
    if g == DiffieHellman.p:
        print(secretKeyA == 0, end = '\n\n\n')
    if g == DiffieHellman.p -1:
        if A == DiffieHellman.p-1 and B == DiffieHellman.p-1:
            print(secretKeyA == DiffieHellman.p-1, end = '\n\n\n')
        else:
            print(secretKeyA == 1, end = '\n\n\n')


def main():
    DHwithNegotiatedGroups(DiffieHellman.p, 1)
    DHwithNegotiatedGroups(DiffieHellman.p, DiffieHellman.p)
    DHwithNegotiatedGroups(DiffieHellman.p, DiffieHellman.p-1)


if __name__ == "__main__":
    main()

