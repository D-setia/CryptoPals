import sys
sys.path.insert(1, "../..")
import set1.chall_8.detectAesInEcb as AES_detect
import set1.chall_7.aesInEcbMode as AES_ECB
import set2.chall_11.encryptionBlackBox as EncBlackBox


def detectAESMode(func):
    payload = 'a'*48
    payload = bytes(payload.encode('utf-8'))

    ct = func(payload)
    
    isEcb = AES_detect.checkForAesInEcb(ct)
    if isEcb:
        return "ECB"
    else:
        return "CBC"
    

def main():
    for i in range(10):
        mode = detectAESMode(EncBlackBox.blackBox)
        print(mode)


if __name__ == "__main__":
    main() 

