def fixedXor(ip1, ip2):
    if(len(ip1) != len(ip2)):
        print("Error: length of inputs not same")
        return null
    
    result = [0]*len(ip1)

    for i in range(len(ip1)):
        result[i] = ip1[i] ^ ip2[i]

    result = bytes(result)
    return result


def main():
    ip1 = input("First ip: ")
    ip2 = input("Second ip: ")
    ip1 = bytes.fromhex(ip1)
    ip2 = bytes.fromhex(ip2)
    result = fixedXor(ip1, ip2)
    print(result)

if __name__ == "__main__":
    main() 
