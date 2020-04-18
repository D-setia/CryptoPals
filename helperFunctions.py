import random

def getRandBytes(noOfBytes):
    randBytes = []
    for i in range(noOfBytes):
        randBytes.append(random.randrange(0,256))
    randBytes = bytes(randBytes)
    return randBytes


def main():
    randBytes = getRandBytes(16)
    print(randBytes)


if __name__ == "__main__":
    main()
