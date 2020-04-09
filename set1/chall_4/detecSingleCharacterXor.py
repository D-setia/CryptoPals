import sys
sys.path.insert(1, "../")
import chall_3.singleByteXor as singleByteXor


def main():
    ip = open("input.txt", 'r')
    for x in ip:
        y = x[0 : len(x)-1]
        result = singleByteXor.identifySingleByteXor(y)
        if len(result) != 0:
            if result[0][0] < 3:
                for i in range(len(result)):
                    print(result[i])
                print('')


        
if __name__ == "__main__":
    main()
