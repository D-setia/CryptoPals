import sys
sys.path.insert(1, "../")
import chall_1.hexTobase64 as hexTobase64

def repeatingKeyXor(ip, key):
    result = [None for i in range(len(ip))]
    for i in range(len(ip)):
        result[i] = ip[i] ^ key[i%len(key)]
    result = bytes(result)
    result = result.hex()
    return result

def main():
    ip = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = "ICE"
    
    ip = hexTobase64.asciiToHexString(ip)
    key = hexTobase64.asciiToHexString(key)

    ip = hexTobase64.hexStringToBytes(ip)
    key = hexTobase64.hexStringToBytes(key)

    enc = repeatingKeyXor(ip, key)
    print(enc)

if __name__ == "__main__":
    main()
