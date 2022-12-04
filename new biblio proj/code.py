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
    percent = int(input("Введите процент ошибок: "))
    n = int(input("Введите длину блока: "))  # длина блока
    h = np.log2(percent + 1)  # нужная степень
    t = round(percent * n / (1 + percent * h))  # количество ошибок
    k = int(n - h * t)  # длина начального сообщения
    coded = bch.BCH(n, t)
    m = coded.g.size - 1
    msgs = np.array(data, dtype="int64")
    enc_msgs = coded.encode(msgs)
    # print(enc_msgs)
    width = len(enc_msgs)
    height = len(enc_msgs[0])
    xd = int((width * height) ** 0.5) + 1
    rejim = None
    povtor = True
    while povtor:
        if xd % 2 == 0:
            if xd ** 2 - width * height >= 100:
                rejim = 1
                povtor = False
            elif 0 <= xd ** 2 - width * height < 100:
                xd += 1
                rejim = 2
                povtor = False
            else:
                xd += 1
                rejim = 2
        else:
            if xd ** 2 - width * height >= 121:
                rejim = 2
                povtor = False
            elif 0 <= xd ** 2 - width * height < 121:
                xd += 1
                rejim = 1
                povtor = False
            else:
                xd += 1
                rejim = 1
    img = Image.new(mode="RGB", size=(xd, xd))
    draw = ImageDraw.Draw(img)
    pix = img.load()
    promej = [[enc_msgs[i][j] for j in range(len(enc_msgs[i]))] for i in range(len(enc_msgs) - 1)]
    enc_msgs_to_list = []
    for i in promej:
        enc_msgs_to_list.extend(i)
    pusto = 0
    shag = 0
    for i in range(len(enc_msgs_to_list)):
        if rejim == 1 and xd // 2 - 5 <= (i + shag) % xd <= xd // 2 + 4 and xd // 2 - 5 <= (
                i + shag) // xd <= xd // 2 + 4:
            shag += 10
        elif rejim == 2 and xd // 2 - 5 <= (i + shag) % xd <= xd // 2 + 5 and xd // 2 - 5 <= (
                i + shag) // xd <= xd // 2 + 5:
            shag += 11
        elif enc_msgs_to_list[i] == 1:
            draw.point(((i+shag) % xd, (i+shag) // xd), (255, 255, 255))  # рисуем пиксель
        else:
            draw.point(((i+shag) % xd, (i+shag) // xd), (0, 0, 0))  # рисуем пиксель
        pusto = i
    for i in range(pusto + 1, xd ** 2):
        draw.point(((i+shag) % xd, (i+shag) // xd), (255, 255, 255))

    img.save('outputfile\image.png')

elif mode == "2":
    pass
