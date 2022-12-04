import bchlib
import hashlib
import random

# create a bch object
alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
BCH_POLYNOMIAL = 8219
BCH_BITS = 16
bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)
print(bch)
# random data
a = "".join(random.choices(alph, k=512))
data = a.encode("utf-16")
print(data)
print(data.decode('utf-16'))
# encode and make a "packet"
ecc = bch.encode(data)
packet = data + ecc
print(list(ecc))
print(list(packet))
