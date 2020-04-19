import sys
sys.path.insert(1, "../../")
import set3.chall_19.breakFixedNonceCtrUsingSubstitutions as BreakCTR


def main():
    ipFile = open("input.txt", 'r')
    cts = BreakCTR.generateCts(ipFile)
    ipFile.close()
    pts = BreakCTR.breakEnc2(cts)
    for pt in pts:
        print(pt)



if __name__ == "__main__":
    main()

