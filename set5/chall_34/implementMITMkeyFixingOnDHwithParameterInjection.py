import hashlib
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set2.chall_9.implementPKCS7 as PKCS7
import set2.chall_10.implementCbcMode as AES_CBC
import set5.chall_33.implementDiffieHellman as DiffieHellman


def keyExchangeProtocol():
    p_A, g_A = DiffieHellman.p, DiffieHellman.g

    keyPairA = DiffieHellman.generateKeyPair(p_A, g_A)
    A = keyPairA[1]
    print("A to B: p, g, A")
    keyPairB = DiffieHellman.generateKeyPair(p_A, g_A)
    B = keyPairB[1]
    print("B to A: B")

    secretKeyA = DiffieHellman.DH(B, keyPairA, p_A)
    secretKeyB = DiffieHellman.DH(A, keyPairB, p_A)

    messageA = 'This is my message suckerr.\nYour\'s Sincerely\nA'
    messageA = bytes(messageA.encode('latin1'))
    secretKeyA_bytes = bytes.fromhex(hex(secretKeyA)[2:])
    AESkeyA = hashlib.sha1(secretKeyA_bytes).digest()[:16]
    IV_A = helpers.getRandBytes(16)
    ct = AES_CBC.AES_CBCencrypt(PKCS7.PKCS7(messageA, 16), AESkeyA, IV_A)

    secretKeyB_bytes = bytes.fromhex(hex(secretKeyB)[2:])
    AESkeyB = hashlib.sha1(secretKeyB_bytes).digest()[:16]
    pt = AES_CBC.AES_CBCdecrypt(ct, AESkeyB, IV_A)
    if PKCS7.PKCS7validate(pt, 16):
        pt = PKCS7.PKCS7unpad(pt)
    else:
        raise Exception('Something is wrong')

    IV_B = helpers.getRandBytes(16)
    ct_BtoA = AES_CBC.AES_CBCencrypt(PKCS7.PKCS7(pt, 16), AESkeyB, IV_B)

    messageA2 = AES_CBC.AES_CBCdecrypt(ct_BtoA, AESkeyA, IV_B)
    if PKCS7.PKCS7validate(messageA2, 16):
        messageA2 = PKCS7.PKCS7unpad(messageA2)
    else:
        raise Exception('Something is wrong')

    if messageA == messageA2:
        print('Connection established')
    else:
        print('No connection')


def MITM():
    p_A, g_A = DiffieHellman.p, DiffieHellman.g

    keyPairA = DiffieHellman.generateKeyPair(p_A, g_A)
    A = keyPairA[1]
    print("A to B: p, g, A")
    print("Intercepted by M")
    keyPairB = DiffieHellman.generateKeyPair(p_A, g_A)
    B = keyPairB[1]
    print("M to B: p, g, p")
    print("B to M: B")
    print("M to A: p")

    secretKeyA = DiffieHellman.DH(p_A, keyPairA, p_A)
    secretKeyB = DiffieHellman.DH(p_A, keyPairB, p_A)

    messageA = 'This is my message suckerr.\nYour\'s Sincerely\nA'
    messageA = bytes(messageA.encode('latin1'))
    secretKeyA_bytes = bytes.fromhex(hex(secretKeyA)[2:] if len(hex(secretKeyA)[2:])%2 == 0 else '0'+hex(secretKeyA)[2:])
    AESkeyA = hashlib.sha1(secretKeyA_bytes).digest()[:16]
    IV_A = helpers.getRandBytes(16)
    ct = AES_CBC.AES_CBCencrypt(PKCS7.PKCS7(messageA, 16), AESkeyA, IV_A)

    secretKeyB_bytes = bytes.fromhex(hex(secretKeyB)[2:] if len(hex(secretKeyB)[2:])%2 == 0 else '0'+hex(secretKeyB)[2:])
    AESkeyB = hashlib.sha1(secretKeyB_bytes).digest()[:16]
    pt = AES_CBC.AES_CBCdecrypt(ct, AESkeyB, IV_A)
    if PKCS7.PKCS7validate(pt, 16):
        pt = PKCS7.PKCS7unpad(pt)
    else:
        raise Exception('Something is wrong')

    IV_B = helpers.getRandBytes(16)
    ct_BtoA = AES_CBC.AES_CBCencrypt(PKCS7.PKCS7(pt, 16), AESkeyB, IV_B)

    messageA2 = AES_CBC.AES_CBCdecrypt(ct_BtoA, AESkeyA, IV_B)
    if PKCS7.PKCS7validate(messageA2, 16):
        messageA2 = PKCS7.PKCS7unpad(messageA2)
    else:
        raise Exception('Something is wrong')

    if messageA == messageA2:
        print('Connection established')
    else:
        print('No connection')

    AESkeyM = hashlib.sha1(bytes.fromhex('00')).digest()[:16]
    messageA = 'Message 1'
    messageA = bytes(messageA.encode('latin1'))
    IV_A = helpers.getRandBytes(16)
    ct = AES_CBC.AES_CBCencrypt(PKCS7.PKCS7(messageA, 16), AESkeyA, IV_A)
    print('A:', messageA)
    messageM = AES_CBC.AES_CBCdecrypt(ct, AESkeyM, IV_A)
    if PKCS7.PKCS7validate(messageM, 16):
        messageM = PKCS7.PKCS7unpad(messageM)
        print('M:', messageM)
    else:
        raise Exception('Something is wrong')
    messageB = AES_CBC.AES_CBCdecrypt(ct, AESkeyB, IV_A)
    if PKCS7.PKCS7validate(messageB, 16):
        messageB = PKCS7.PKCS7unpad(messageB)
        print('B:', messageB)
    else:
        raise Exception('Something is wrong')




def main():
    MITM()
    #keyExchangeProtocol()


if __name__ == "__main__":
    main()

