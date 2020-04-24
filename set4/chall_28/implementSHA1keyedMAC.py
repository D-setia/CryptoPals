import hashlib

def SHA1MAC(key, ipBytes):
    mac = hashlib.sha1(key+ipBytes)
    mac = mac.hexdigest()
    return mac


def main():
    key = bytes('aaaa'.encode('utf-8'))
    mac = SHA1MAC(key, key)
    print(mac.encode('utf-8'))


if __name__ == "__main__":
    main()

