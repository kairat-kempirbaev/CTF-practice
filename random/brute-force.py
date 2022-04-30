import hashlib
import sys
import itertools

# https://stackoverflow.com/questions/1851134/generate-all-binary-strings-of-length-n-with-k-bits-set


def kbits(n, k):
    for bits in itertools.combinations(range(n), k):
        so_far = bytearray()
        s = ['0'] * n
        for i in bits:
            s[i] = '1'
        so_far.extend(int("".join(s), 2).to_bytes(n/8, 'big'))
        yield so_far

#Look for any hash that starts with "000" in hex
with open("hashMe.png", mode='rb') as file:  # b is important -> binary
    fileContent = file.read()
    m = hashlib.new('sha256')
    n = 8
    while n < 33:
        k = 1
        while True:
            for i in kbits(n, k):
                xs = bytearray(fileContent)
                xs.extend(i)
                m.update(xs)
                hashed = m.hexdigest()
                if hashed[:2] == "000":
                    print("FOUND")
                    print(hashed)
                    sys.exit(1)
            k += 1
            if k > n:
                break
        n += 8
