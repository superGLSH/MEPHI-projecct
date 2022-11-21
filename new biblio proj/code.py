import bch
from PIL import Image, ImageDraw
import numpy as np

# inpf = input("Введите название файла: ")
inpf = '1.txt'
with open(f"inputfile/{inpf}", mode="rb") as file:
    data = list(
        map(lambda x: list("0" * (8 - len(bin(x).replace("0b", "", 1))) + bin(x).replace("0b", "", 1)),
            list(file.read())))
# mode = input("Хотите кодировать (1) или декодировать (2): ")
mode = "1"

if mode == "1":
    # percent = int(input("Введите процент ошибок: "))
    # percent = 18
    coded = bch.BCH(24, 3)
    m = coded.g.size - 1
    msgs = np.array(data, dtype="int64")
    enc_msgs = coded.encode(msgs)
    # print(enc_msgs)
    width = len(enc_msgs)
    height = len(enc_msgs[0])
    img = Image.new(mode="RGB", size=(width, height))
    draw = ImageDraw.Draw(img)
    pix = img.load()
    for x in range(width):
        for y in range(height):
            if enc_msgs[x][y] == 1:
                draw.point((x, y), (255, 255, 255))  # рисуем пиксель
            else:
                draw.point((x, y), (0, 0, 0))  # рисуем пиксель
    img.save('outputfile\image2.png')


elif mode == "2":
    pass
