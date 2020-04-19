import base64
import sys
sys.path.insert(1, "../../")
import helperFunctions as helper
import set1.chall_6.breakRepeatingKeyXor as Vigenere
import set1.chall_3.singleByteXor as SingleByteXor
import set3.chall_18.implementCtrMode as AES_CTR


def generateCts(ipFile):
    key = helper.getRandBytes(16)
    nonce = 0
    cts = []
    for line in ipFile:
        pt = line[:len(line)-1]
        pt = base64.b64decode(pt)
        ct = AES_CTR.AES_CTR(pt, key, nonce)
        cts.append(ct)
    return cts


def breakEnc(cts):
    minLen = 1000
    lines = 0
    pts = []
    for x in cts:
        if len(x) < minLen:
            minLen = len(x)
    vigenereInput = bytes(''.encode('utf-8'))
    for x in cts:
        vigenereInput += x[:minLen]
        lines += 1
    vigenerePt = Vigenere.breakRepeatingKeyXor(vigenereInput)

    for i in range(lines):
        known = bytes("Known: ".encode('utf-8'))
        unknown = bytes(" Unknown: ".encode('utf-8'))
        ct = cts[i]
        pt = known + vigenerePt[i*16:(i+1)*16] + unknown + ct[minLen:]
        pts.append(pt)

    return pts


def breakEnc2(cts):
    maxLen = -1
    noOfCts = len(cts)
    for x in cts:
        if len(x) > maxLen:
            maxLen = len(x)
    pts = [bytes(''.encode('latin1')) for i in range(noOfCts)]
    for i in range(maxLen):
        ctInput = bytes(''.encode('latin1'))
        for j in range(noOfCts):
            if i < len(cts[j]):
                ctInput += bytes([cts[j][i]])
        ptOutput = SingleByteXor.identifySingleByteXor(ctInput.hex())
        ptIndex = 0
        for j in range(noOfCts):
            if i < len(cts[j]):
                if ptOutput[0][1][ptIndex] == 0:
                    pts[j] += bytes(' '.encode('latin1'))
                else:
                    pts[j] += bytes([ptOutput[0][1][ptIndex]])
                ptIndex += 1
    return pts


def main():
    ipFile = open("input.txt", 'r')
    cts = generateCts(ipFile)
    ipFile.close()
    pts = breakEnc2(cts)
    for x in pts:
        print(x)





if __name__ == "__main__":
    main()

