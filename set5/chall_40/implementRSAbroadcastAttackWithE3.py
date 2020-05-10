import math
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set5.chall_39.implementRSA as RSA


def coerceCts(ptString):
    keyPair1 = RSA.generateKeyPair()
    keyPair2 = RSA.generateKeyPair()
    keyPair3 = RSA.generateKeyPair()

    ct1 = RSA.encrypt(ptString, keyPair1[1])
    ct2 = RSA.encrypt(ptString, keyPair2[1])
    ct3 = RSA.encrypt(ptString, keyPair3[1])

    pairs = []
    pairs.append((ct1, keyPair1[1]))
    pairs.append((ct2, keyPair2[1]))
    pairs.append((ct3, keyPair3[1]))

    return pairs


def breakRSAusingCRT(pairs):
    (ct0, publicKey0) = pairs[0]
    (ct1, publicKey1) = pairs[1]
    (ct2, publicKey2) = pairs[2]
    n_0 = publicKey0[1]
    n_1 = publicKey1[1]
    n_2 = publicKey2[1]

    c_0 = RSA.stringToInt(ct0)
    c_1 = RSA.stringToInt(ct1)
    c_2 = RSA.stringToInt(ct2)

    m_s_0 = n_1*n_2
    m_s_1 = n_0*n_2
    m_s_2 = n_0*n_1
    N_012 = n_0*n_1*n_2

    result = (c_0 * m_s_0 * helpers.modInv(m_s_0, n_0))+(c_1 * m_s_1 * helpers.modInv(m_s_1, n_1))+(c_2 * m_s_2 * helpers.modInv(m_s_2, n_2))
    result = result%N_012
    pt = helpers.invPow(result, 3)
    pt = math.ceil(pt)
    pt = RSA.intToStr(pt)
    return pt


def main():
    pt = "I know what's wirtten here"
    pairs = coerceCts(pt)
    ptR = breakRSAusingCRT(pairs)
    print(ptR)


if __name__ == "__main__":
    main()

