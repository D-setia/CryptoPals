import math

def hexToBytes(ip):
    byteArr = bytes.fromhex(ip)
    return byteArr

def xorStringWithByte(byteString, byte):
    result = [byteString[i]^byte for i in range(len(byteString))]
    result = bytes(result)
    return result

def isValidPlaintext(ip):
    chars = 0
    for i in range(len(ip)):
        if (ip[i] in range(65, 91)) or (ip[i] in range(97,123)):
            chars += 1
    
    if chars/len(ip) > 0.6:
        return True
    else:
        return False

def scorePlaintext(pt):
    english_freq = [
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,  # A-G
        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,  # H-N
        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,  # O-U
        0.00978, 0.02360, 0.00150, 0.01974, 0.00074]                    # V-Z
    
    chars = 0
    freq = [0 for i in range(26)]
    for i in range(len(pt)):
        if(pt[i] in range(65, 91)):
            freq[pt[i]-65] += 1
            chars += 1
        elif(pt[i] in range(97, 123)):
            freq[pt[i]-97] += 1
            chars += 1

    chi = 0
    for i in range(26):
        freq[i] = freq[i]/chars
        chi += math.pow((freq[i]-english_freq[i]), 2)/english_freq[i]

    return chi

def checkAndAdd(validPts, scoreNew, ptNew):
    validPtsNew = []
    if len(validPts) == 0:
        validPts.append((scoreNew, ptNew))
        validPtsNew = validPts
    elif len(validPts) == 1:
        if(validPts[0][0] < scoreNew):
            validPts.append((scoreNew, ptNew))
            validPtsNew = validPts
        else:
            validPtsNew.append((scoreNew, ptNew))
            validPtsNew.append(validPts[0])
    elif len(validPts) == 2:
        if validPts[0][0]  > scoreNew:
            validPtsNew.append((scoreNew, ptNew))
            validPtsNew.append(validPts[0])
            validPtsNew.append(validPts[1])
        elif validPts[1][0] > scoreNew:
            validPtsNew.append(validPts[0])
            validPtsNew.append((scoreNew, ptNew))
            validPtsNew.append(validPts[1])
        else:
            validPts.append((scoreNew, ptNew))
            validPtsNew = validPts
    else:
        if validPts[0][0]  > scoreNew:
            validPtsNew.append((scoreNew, ptNew))
            validPtsNew.append(validPts[0])
            validPtsNew.append(validPts[1])
        elif validPts[1][0] > scoreNew:
            validPtsNew.append(validPts[0])
            validPtsNew.append((scoreNew, ptNew))
            validPtsNew.append(validPts[1])
        elif validPts[2][0] > scoreNew:
            validPtsNew.append(validPts[0])
            validPtsNew.append(validPts[1])
            validPtsNew.append((scoreNew, ptNew))
        else:
            validPtsNew = validPts

    return validPtsNew

def identifySingleByteXor(ct):
    ciphertext = hexToBytes(ct)
    validPts = []
    
    for i in range(256):
        pt = xorStringWithByte(ciphertext, i)
    
        if(isValidPlaintext(pt)):
            score = scorePlaintext(pt)
            validPts = checkAndAdd(validPts, score, pt)

    return validPts

            
def main():
    ip = input('Give your input: ')
    validPts = identifySingleByteXor(ip)
    print(validPts[0])
    print(validPts[1])
    print(validPts[2])



if __name__ == "__main__":
    main()
