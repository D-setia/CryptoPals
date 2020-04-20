import time
import math

w, n, m, r = 64, 312, 156, 31
a = int('b5026f5aa96619e9', 16)
(u, d) = (29, int('5555555555555555', 16))
(s, b) = (17, int('71d67fffeda60000', 16))
(t, c) = (37, int('fff7eee000000000', 16))
f = 6364136223846793005
l = 43

MT = [None for i in range(n)]
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


def seed_mt(seed):
    global index, n, MT
    index = n
    MT[0] = seed
    for i in range(1, n):
        binNo =  (bin( f*MT[i-1]^(MT[i-1]>>(w-2)) + i)[2:]).zfill(w)
        MT[i] = int(binNo[len(binNo)-w: ], 2)  


def twist():
    global n, index
    for i in range(n):
        x = (MT[i] & upper_mask)+(MT[(i+1)%n] & lower_mask)
        xA = x >> 1
        if x%2 != 0:
            xA = xA ^a
        MT[i] = MT[(i+m)%n] ^ xA
    index = 0


def extract_number():
    global index, n, u, s, t, l, d, b, c
    if index >= n:
        if index > n:
            seed_mt(math.ceil(time.time()*10000000))
        twist()

    y = MT[index]
    y = y ^ ((y>>u) and d)
    y = y ^ ((y<<s) and b)
    y = y ^ ((y<<t) and c)
    y = y ^ (y>>l)

    index += 1
    binNo = (bin(y)[2:]) .zfill(w)
    no = int(binNo[len(binNo)-w:], 2)
    return no

def main():
    seed_mt(12345)
    for i in range(10):
        print(extract_number())

    print('')
    seed_mt(12345)
    for i in range(10):
        print(extract_number())

if __name__ == "__main__":
    main()

