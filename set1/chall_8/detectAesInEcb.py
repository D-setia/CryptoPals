
def checkForAesInEcb(ctString):
    repetitions = 0
    ctString = ctString[:len(ctString)-len(ctString)%16]
    temp = [False for i in range(len(ctString)//16)]
    for i in range(len(ctString)//16):
        if temp[i] == False:
            temp[i] = True
            for j in range(i+1, len(ctString)//16):
                if ctString[i*16 : (i+1)*16] == ctString[j*16 : (j+1)*16]:
                    temp[j] = True
                    repetitions += 1
    if repetitions > 0:
        return True
    else:
        return False


def main():
    ipFile = open("input.txt", 'r')
    for line in ipFile:
        ct = line[:len(line)-1]
        isAesInEcb = checkForAesInEcb(ct)
        if isAesInEcb :
            print(ct)


if __name__ == "__main__":
    main()
