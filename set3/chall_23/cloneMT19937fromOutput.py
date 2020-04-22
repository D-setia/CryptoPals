import random
import sys
sys.path.insert(1, "../../")
import helperFunctions as helpers
import set3.chall_21.implementMT19937 as MT19937

(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
f = 1812433253
MT = []

index = n+1
lower_mask = pow(2,r) -1
upper_mask = ''

temp = (bin(lower_mask)[2:]).zfill(w)
for x in temp:
    if x == '0':
        upper_mask += '1'
    if x == '1':
        upper_mask += '0'

upper_mask = int(upper_mask[len(upper_mask)-w:], 2)



def reverseLeftShiftOp(output, shift, andWith):
    global w
    prev = output[w-shift:]
    i = 1
    while (i+1)*shift < w:
        temp = helpers.binaryStringAnd(andWith[w-(i+1)*shift:w-i*shift], prev[:shift])
        prev = helpers.binaryStringXor(output[w-(i+1)*shift:w-i*shift], temp) + prev
        i += 1
    temp = helpers.binaryStringAnd(andWith[:w-i*shift], prev[(i+1)*shift-w:shift])
    prev = helpers.binaryStringXor(output[:w-i*shift], temp) + prev

    return prev


def reverseRightShiftOp(output, shift, andWith):
    global w
    prev = output[:shift]
    i = 1
    while (i+1)*shift < w:
        temp = helpers.binaryStringAnd(andWith[i*shift:(i+1)*shift], prev[len(prev)-shift:])
        prev += helpers.binaryStringXor(output[i*shift:(i+1)*shift], temp)
        i +=1

    temp = helpers.binaryStringAnd(andWith[i*shift:], prev[len(prev)-shift:len(prev)-(i+1)*shift+w])
    prev += helpers.binaryStringXor(output[i*shift:], temp)
    
    return prev


def unTemper(y):
    global w,l,c,t,b,s,d,u,a
    binC = (bin(c)[2:]).zfill(w)
    binD = (bin(d)[2:]).zfill(w)
    binB = (bin(b)[2:]).zfill(w)
    
    binY = (bin(y)[2:]).zfill(w)
    prevY = binY[:l] + helpers.binaryStringXor(binY[l:],binY[:w-l])
  
    binY = prevY
    prevY = reverseLeftShiftOp(binY, t, binC)

    binY = prevY
    prevY = reverseLeftShiftOp(binY, s, binB)

    binY = prevY
    prevY = reverseRightShiftOp(binY, u, binD)

    y = int(prevY, 2)
    return y


def initialiseMT():
    global MT
    for i in range(n):
        output = MT19937.extract_number()
        number = unTemper(output)
        MT.append(number)


def twist_cracked():
    global n, index
    for i in range(n):
        x = (MT[i] & upper_mask)+(MT[(i+1)%n] & lower_mask)
        xA = x >> 1
        if x%2 != 0:
            xA = xA ^a
        MT[i] = MT[(i+m)%n] ^ xA
    index = 0


def extract_number_cracked():
    global index, n, u, s, t, l, d, b, c
    if index >= n:
        if index > n:
            seed_mt(math.ceil(time.time()*10000000))
        twist_cracked()

    y = MT[index]
    y = y ^ ((y>>u) & d)
    y = y ^ ((y<<s) & b)
    y = y ^ ((y<<t) & c)
    y = y ^ (y>>l)

    index += 1
    binNo = (bin(y)[2:]) .zfill(w)
    no = int(binNo[len(binNo)-w:], 2)
    return no


def crackMT():
    initialiseMT()
    twist_cracked()


def randomizeMT():
    for i in range(random.randrange(0, n)):
        no = MT19937.extract_number()


def main():
    randomizeMT()
    crackMT()

    isSame = True
    for i in range(200*n):
        extractedNo = MT19937.extract_number()
        predictedNo = extract_number_cracked()
        if predictedNo != extractedNo:
            print(i)
            isSame = False

    if isSame:
        print("Cracked!!")


if __name__ == "__main__":
    main()

