import hashlib
import sys
sys.path.insert(1, "../../")
import set4.chall_28.mysha1 as sha1


def SHA1MAC(ipBytes, key):
    shaInput = key+ipBytes
    mac = hashlib.sha1(shaInput).digest()
    #mac = bytes.fromhex(mac) 
    return mac


def main():
    key = bytes('aaajhjshafd.ka'.encode('latin1'))
    mac = SHA1MAC(key, key)
    print(mac)


if __name__ == "__main__":
    main()

