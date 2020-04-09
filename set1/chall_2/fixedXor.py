def fixedXor(ip1, ip2):
    if(len(ip1) != len(ip2)):
        print("Error: length of inputs not same")
        return null
    
    str1Bytes = bytes.fromhex(ip1)
    str2Bytes = bytes.fromhex(ip2)
    result = [0]*len(str1Bytes)

    for i in range(len(str1Bytes)):
        result[i] = str1Bytes[i] ^ str2Bytes[i]

    result = bytes(result).hex()
    return result


def main():
    ip1 = input("First ip: ")
    ip2 = input("Second ip: ")
    result = fixedXor(ip1, ip2)
    print(result)

if __name__ == "__main__":
    main() 
