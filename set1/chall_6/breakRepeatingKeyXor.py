import base64
import sys
sys.path.insert(1, "../..")
import set1.chall_3.singleByteXor as singleByteXor

def stringToBitString(string):
    bitString = ''.join(format(ord(x), 'b').zfill(8) for x in string)
    return bitString

def getHammingDistance(string1, string2):
    if len(string1) != len(string2):
        print("Give inputs of equal length!")
        return None
    else:
        hammingDist = 0
        bitString1 = stringToBitString(string1)
        bitString2 = stringToBitString(string2)
        for i in range(len(bitString1)):
            if bitString1[i] != bitString2[i]:
                hammingDist += 1
        return hammingDist
    

def determineKeySize(byteArr):
    keysize = 1
    minHammingDist = 100
    blocks = [None for i in range(4)]
    for i in range(2,41):
        for j in range(4):
            blocks[j] = byteArr[j*i:(j+1)*i]
        
        avgHammingDist = 0
        for j in range(4):
            for k in range(j):
                #getHammingDistance('hello', 'abcde')
                avgHammingDist += getHammingDistance(blocks[j].decode('latin1'), blocks[k].decode('latin1'))

        avgHammingDist /= 6
        normalisedAvgHammingDist = avgHammingDist/i
        if normalisedAvgHammingDist < minHammingDist:
            minHammingDist = normalisedAvgHammingDist
            keysize = i

    return keysize


def breakRepeatingKeyXor(byteArr):
    keysize = determineKeySize(byteArr)
    result = [None for i in range(len(byteArr))]
    for i in range(keysize):
        j = 0
        singleByteXoredString = []
        while (j*keysize + i) < len(byteArr):
            singleByteXoredString.append(byteArr[j*keysize + i])
            j += 1

        singleByteXoredString = bytes(singleByteXoredString).hex()
        decryptionResults = singleByteXor.identifySingleByteXor(singleByteXoredString)
        
        j = 0
        while (j*keysize + i) < len(byteArr):
            result[j*keysize+i] = decryptionResults[0][1][j]
            j += 1

    for i in range(len(result)):
        if result[i] == 0:
            result[i] = 32
    result = bytes(result)
    return result



def main():
    ipFile = open("input.txt", 'r')
    contents = ''
    for line in ipFile:
        contents += line[:len(line)-1]
    contents = base64.b64decode(contents)
    dec = breakRepeatingKeyXor(contents)
    print(dec)
    #keysize = determineKeySize(contents)
    #print(keysize)
    #print(contents)


if __name__ == "__main__":
    main()
