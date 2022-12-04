from bchlib import BCH
from PIL import Image
from random import randint

mode = 0
if mode == 0:
    with open("input.txt", mode="rb") as file:
        bf = file.read()
    print(bf)
elif mode == 1:
    pass
