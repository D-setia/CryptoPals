import random

p = "ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff"
p = int(p, 16)

g = 2

def generateKeyPair(p_1 = None, g_1 = None):
    global p, g
    p_used = p if p_1 == None else p_1
    g_used = g if g_1 == None else g_1
    privKey = random.randrange(0, p_used+1)
    pubKey = pow(g_used, privKey, p_used)
    return privKey, pubKey

def DH(pubKeyB, myKeyPair, p_1 = None):
    global p
    p_used = p if p_1 == None else p_1
    (privKeyA, pubKeyA) = myKeyPair
    secretKey = pow(pubKeyB, privKeyA, p_used)
    return secretKey

def main():
    privKeyB, pubKeyB = generateKeyPair()
    keyPairB = (privKeyB, pubKeyB)
    privKeyA, pubKeyA = generateKeyPair()
    keyPairA = (privKeyA, pubKeyA)

    secretKeyA = DH(pubKeyB, keyPairA)
    secretKeyB = DH(pubKeyA, keyPairB)
    print(secretKeyA == secretKeyB)
    



if __name__ == "__main__":
    main()

