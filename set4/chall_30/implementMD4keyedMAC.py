import hashlib


def MD4MAC(ipBytes, key):
    md4Input = key+ipBytes
    hashAlgo = hashlib.new('md4')
    hashAlgo.update(md4Input)
    mac = hashAlgo.digest()
    return mac


def main():
    key = bytes(''.encode('latin1'))
    mac = MD4MAC(key, key)
    print(mac.hex())


if __name__ == "__main__":
    main()

