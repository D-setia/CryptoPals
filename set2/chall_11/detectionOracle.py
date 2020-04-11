import encryptionBlackBox as EncBlackBox
import sys
sys.path.insert(1, "../..")
import set1.chall_8.detectAesInEcb as AES_detect
import set1.chall_7.aesInEcbMode as AES_ECB


def main():
    payload = 'a'*48
    payload = bytes(payload.encode('utf-8'))
    key = "YELLOW SUBMARINE"
    key = bytes(key.encode('utf-8'))

    #ct = AES_ECB.AESencrypt(payload, key)
    #isEcb = AES_detect.checkForAesInEcb(ct)
    #if isEcb:
    #    print("ECB")


    for i in range(10):
        ct = EncBlackBox.blackBox(payload)
        
        isEcb = AES_detect.checkForAesInEcb(ct)
        if isEcb:
            print("Guess: ECB", end = '\n\n')
        else:
            print("Guess: CBC", end = '\n\n')



if __name__ == "__main__":
    main()
