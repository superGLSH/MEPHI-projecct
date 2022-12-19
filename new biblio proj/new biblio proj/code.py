import bch
from PIL import Image, ImageDraw
import numpy as np
import cv2
import skimage


def mybin(a):
    b = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ";"]
    c = ["0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011"]
    return c[b.index(a)]


def nibym(a):
    b = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ";", ""]
    c = ["0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "0000"]
    return b[c.index(a)]


# inpf = input("Введите название файла: ")
inpf = '1.txt'
with open(f"inputfile/{inpf}", mode="rb") as file:
    data = list(
        map(lambda x: list("0" * (8 - len(bin(x).replace("0b", "", 1))) + bin(x).replace("0b", "", 1)),
            list(file.read())))
mode = input("Хотите кодировать (1) или декодировать (2) или сломать (3): ")

if mode == "1":
    percent = int(input("Введите процент ошибок: "))
    n = int(input("Введите длину блока: "))  # длина блока
    h = np.log2(n + 1)  # нужная степень
    t = round(percent * n / (1 + percent * h))  # количество ошибок
    # percent * n / (1 + percent * h)
    k = int(n - h * t)  # длина начального сообщения
    print(k)
    # n - Блок, h - степень, K = n - h*S, s - количество ошибок k = n - h * percent*n = n*(1 - perncent *h)
    coded = bch.BCH(n, k)
    print(t)
    print(coded.g.size)
    m = coded.g.size - 1
    print(m)
    msgs = np.array(data, dtype="int64")
    print(msgs[0])
    print(list(map(list, msgs)))
    enc_msgs = coded.encode(msgs)
    msgs1 = coded.decode(enc_msgs)
    print(list(map(list, enc_msgs)))
    print(list(map(list, msgs1)))
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
    promej = [[enc_msgs[i][j] for j in range(len(enc_msgs[i]))] for i in range(len(enc_msgs))]
    enc_msgs_to_list = []
    for i in promej:
        enc_msgs_to_list.extend(i)

    print("".join(map(str, enc_msgs_to_list)))

    pusto = 0
    shag = 0
    print(len("".join(map(str, enc_msgs_to_list))))
    for i in range(len(enc_msgs_to_list)):
        if rejim == 1 and xd // 2 - 5 <= (i + shag) % xd <= xd // 2 + 4 and xd // 2 - 5 <= (
                i + shag) // xd <= xd // 2 + 4:
            shag += 10
        elif rejim == 2 and xd // 2 - 5 <= (i + shag) % xd <= xd // 2 + 5 and xd // 2 - 5 <= (
                i + shag) // xd <= xd // 2 + 5:
            shag += 11
        elif enc_msgs_to_list[i] == 1:
            draw.point(((i + shag) % xd, (i + shag) // xd), (255, 255, 255))  # рисуем пиксель
        else:
            draw.point(((i + shag) % xd, (i + shag) // xd), (0, 0, 0))  # рисуем пиксель
        pusto = i
    print(pusto)
    for i in range(pusto + 1, xd ** 2):
        draw.point(((i + shag) % xd, (i + shag) // xd), (0, 0, 0))

    rabinf = str(n) + ';' + str(t) + ';' + str(xd) + ';' + str(width) + ';' + str(height) + ';' + str(pusto)
    print(len(rabinf))

    if rejim == 1:
        inf = "".join([mybin(i) for i in list(rabinf)]) + "0" * (100 - len("".join([mybin(i) for i in list(rabinf)])))
        print(inf)
        chet = 0
        for i in range(xd // 2 - 5, xd // 2 + 5):
            for j in range(xd // 2 - 5, xd // 2 + 5):
                if inf[chet] == "1":
                    draw.point((i, j), (255, 255, 255))  # рисуем пиксель
                    chet += 1
                elif inf[chet] == "0":
                    draw.point((i, j), (0, 0, 0))  # рисуем пиксель
                    chet += 1
    elif rejim == 2:
        inf = "".join([mybin(i) for i in list(rabinf)]) + "0" * (
                121 - len("".join([mybin(i) for i in list(rabinf)])))
        print(inf)
        chet = 0
        for i in range(xd // 2 - 5, xd // 2 + 6):
            for j in range(xd // 2 - 5, xd // 2 + 6):
                if inf[chet] == "1":
                    draw.point((i, j), (255, 255, 255))  # рисуем пиксель
                    chet += 1
                elif inf[chet] == "0":
                    draw.point((i, j), (0, 0, 0))  # рисуем пиксель
                    chet += 1

    img.save('outputfile\image.png')

elif mode == "2":
    img = Image.open('outputfile\image.png')
    x = img.size[0]
    pix = img.load()
    slujba = ""
    if x % 2 == 0:
        for i in range(x // 2 - 5, x // 2 + 5):
            for j in range(x // 2 - 5, x // 2 + 5):
                if pix[i, j][0] == 255:
                    slujba += "1"
                else:
                    slujba += "0"

    else:
        for i in range(x // 2 - 5, x // 2 + 6):
            for j in range(x // 2 - 5, x // 2 + 6):
                if pix[i, j][0] == 255:
                    slujba += "1"
                else:
                    slujba += "0"
    flag = 0
    sp = []
    slovo = ""
    for i in slujba:
        slovo += i
        flag += 1
        if flag % 4 == 0:
            sp.append(slovo)
            slovo = ""
    print(slujba)
    n, t, xd, width, height, pusto = tuple(map(int, "".join(list(map(nibym, sp))).split(";")))
    print(n, t, xd, width, height, pusto)
    enc_file = ""
    for i in range(x):
        for j in range(x):
            if x % 2 == 0 and not (xd // 2 - 5 <= i <= xd // 2 + 4 and xd // 2 - 5 <= j <= xd // 2 + 4):
                if pix[j, i][0] == 255:
                    enc_file += "1"
                else:
                    enc_file += "0"
            elif x % 2 == 1 and not (xd // 2 - 5 <= i <= xd // 2 + 5 and xd // 2 - 5 <= j <= xd // 2 + 5):
                if pix[j, i][0] == 255:
                    enc_file += "1"
                else:
                    enc_file += "0"
    flag = 0
    sp = []
    slovo = ""
    for i in enc_file[:(pusto + 1)]:
        slovo += i
        flag += 1
        if flag % height == 0:
            sp.append(list(str(slovo)))
            slovo = ""
    print(list(map(list, sp)))
    sp = np.array(sp, dtype="int64")
    bch = bch.BCH(n, t)
    print(len(list(map(list, sp))))
    msgs = bch.decode(sp)
    msgs_to_list = []
    print(list(msgs))
    bla = 0
    for i in range(len(list(map(list, msgs)))):
        try:
            msgs_to_list += list(map(int, [msgs[i][j] for j in range(len(sp[0]))]))
        except Exception:
            msgs_to_list += list(map(int, [sp[i][j] for j in range(len(sp[0]))]))
    flag = 0
    sp = []
    sp1 = []
    slovo = ""
    for i in msgs_to_list:
        slovo += str(i)
        flag += 1
        if flag % len(msgs[0]) == 0:
            sp.append(chr(int(slovo[:8], 2)))
            sp1.append(list(slovo[:8]))
            slovo = ""
    for i in range(len(data)):
        if data[i] != sp1[i]:
            print(i, data[i], sp1[i], sp[i])
    with open(f"outputfile/{inpf}", mode="w") as file:
        file.write("".join(sp).replace("\r", ""))

elif mode == "3":
    origin = skimage.io.imread("outputfile\image.png")
    noisy = skimage.util.random_noise(origin, mode='gaussian', var=80)
    skimage.io.imsave("outputfile\image.png", noisy.astype(np.uint8))
# 00110001100111001100100110010011001110011000110100011010001101011001010011011001101100110111100100000011011110010000101000010101101000110100011001101100110111001100011001101001001011011010001101000110011011001101110011000110011101010001010110100011010001100110110011011100110001100000110111100100001010000101011110010000110110000100111100100000010000011100110001100110111100100001100010110001011000010011110110101100101001100001001111001000000100000111010011101001101001001011001000000100000111001100011001101111001000011000101100010110000100111101101011001010011000010011110000110111100100001010000101011011101101110111100100001101101110110111011110010000110110111011011101111001000011011000010011110000110111100100001010000101011000101100010110110011011001100001001111001000000100000110001011000101101100110110011000010011110010000001000001100000110001011011001101100110000100111100100000010000011000101100010110110001011001100001001111001000000100000100001011000101101100110110011000010001110010000001000001100010110001011001001101100110000100111100001101111001000010100001010110111011011101110101000101011100101110010111010100010101101110110111011110010000110110000100111100001101111001000010100001010110110011011001111001000011011100101110010110010100110101110001000111011101110001000110010100110101110010111001011101001110100111100100001101110101000101011010010010110110111100100001110000111000011011001101100110101100101001101010110101011010110010100110100011010001101010110101011001110011000111100100001101100110110011011101001110100110010011001001100101001101011100101110010111010011101001101000110100011010010010110110001011000101110110111011011000110011100110011100110001101111001000011110010000110110100011010000100111101100011011010010010110111011011101100010110001011011001101100111010100010101110110111011011001110011000110111100100001101000110100011101010001010110111100100000001101111001000010100001010111100011110001100100110010
# 00110001100111001100100110010011001110011000110100011010001101011001010011011001101100110111100100000011011110010000101000010101101000110100011001101100110111001100011001101001001011011010001101000110011011001101110011000110011101010001010110100011010001100110110011011100110001100000110111100100001010000101011110010000110110000100111100100000010000011100110001100110111100100001100010110001011000010011110110101100101001100001001111001000000100000111010011101001101001001011001000000100000111001100011001101111001000011000101100010110000100111101101011001010011000010011110000110111100100001010000101011011101101110111100100001101101110110111011110010000110110111011011101111001000011011000010011110000110111100100001010000101011000101100010110110011011001100001001111001000000100000110001011000101101100110110011000010011110010000001000001100010110001011011001101100110000100111100100000010000011000101100010110110011011001100001001111001000000100000110001011000101101100110110011000010011110010000001000001100010110001011011001101100110000100111100001101111001000010100001010110111011011101110101000101011100101110010111010100010101101110110111011110010000110110000100111100001101111001000010100001010110110011011001111001000011011100101110010110010100110101110001000111011101110001000110010100110101110010111001011101001110100111100100001101110101000101011010010010110110111100100001110000111000011011001101100110101100101001101010110101011010110010100110100011010001101010110101011001110011000111100100001101100110110011011101001110100110010011001001100101001101011100101110010111010011101001101000110100011010010010110110001011000101110110111011011000110011100110011100110001101111001000011110010000110110100011010000100111101100011011010010010110111011011101100010110001011011001101100111010100010101110110111011011001110011000110111100100001101000110100011101010001010110111100100000001101111001000010100001010111100011110001100100110010

# [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1]


# [['0', '0', '1', '1', '0', '0', '0', '1'], ['0', '0', '1', '1', '0', '0', '1', '0'], ['0', '0', '1', '1', '0', '0', '1', '1'], ['0', '0', '1', '1', '0', '1', '0', '0'], ['0', '0', '1', '1', '0', '1', '0', '1'], ['0', '0', '1', '1', '0', '1', '1', '0'], ['0', '0', '1', '1', '0', '1', '1', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '0', '0', '1', '1', '0'], ['0', '1', '1', '1', '0', '0', '1', '1'], ['0', '1', '1', '0', '1', '0', '0', '1'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '0', '0', '1', '1', '0'], ['0', '1', '1', '1', '0', '0', '1', '1'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '0', '0', '1', '1', '0'], ['0', '1', '1', '1', '0', '0', '1', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '1', '0', '0', '1', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '1', '1', '0', '1', '0', '1', '1'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '1', '0', '1', '0', '0'], ['0', '1', '1', '0', '1', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '1', '0', '0', '1', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '1', '1', '0', '1', '0', '1', '1'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '1', '0', '0', '1', '0'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '1', '0', '0', '1', '0'], ['0', '1', '1', '0', '0', '1', '0', '1'], ['0', '1', '1', '1', '0', '0', '0', '1'], ['0', '1', '1', '1', '0', '1', '1', '1'], ['0', '1', '1', '0', '0', '1', '0', '1'], ['0', '1', '1', '1', '0', '0', '1', '0'], ['0', '1', '1', '1', '0', '1', '0', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '0', '1', '0', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '1', '1', '1', '0', '0', '0', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '1', '0', '1', '1'], ['0', '1', '1', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '1', '0', '1', '1'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '0', '1', '1', '1'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '0', '1', '1', '0'], ['0', '1', '1', '1', '0', '1', '0', '0'], ['0', '1', '1', '0', '0', '1', '0', '0'], ['0', '1', '1', '0', '0', '1', '0', '1'], ['0', '1', '1', '1', '0', '0', '1', '0'], ['0', '1', '1', '1', '0', '1', '0', '0'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '0', '1', '0', '0', '1'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '1', '0', '1', '1', '0'], ['0', '1', '1', '0', '0', '0', '1', '1'], ['0', '1', '1', '0', '0', '1', '1', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '0', '1', '0', '0', '1', '1', '1'], ['0', '1', '1', '0', '1', '1', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '1', '0', '1', '1', '0'], ['0', '1', '1', '0', '0', '1', '1', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '0'], ['0', '1', '1', '0', '0', '1', '0', '0']]
# [['0', '0', '1', '1', '0', '0', '0', '1'], ['0', '0', '1', '1', '0', '0', '1', '0'], ['0', '0', '1', '1', '0', '0', '1', '1'], ['0', '0', '1', '1', '0', '1', '0', '0'], ['0', '0', '1', '1', '0', '1', '0', '1'], ['0', '0', '1', '1', '0', '1', '1', '0'], ['0', '0', '1', '1', '0', '1', '1', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '0', '0', '1', '1', '0'], ['0', '1', '1', '1', '0', '0', '1', '1'], ['0', '1', '1', '0', '1', '0', '0', '1'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '0', '0', '1', '1', '0'], ['0', '1', '1', '1', '0', '0', '1', '1'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '0', '0', '1', '1', '0'], ['0', '1', '1', '1', '0', '0', '1', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '1', '0', '0', '1', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '1', '1', '0', '1', '0', '1', '1'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '1', '0', '1', '0', '0'], ['0', '1', '1', '0', '1', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '1', '0', '0', '1', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '1', '1', '0', '1', '0', '1', '1'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '0', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '1', '0', '0', '0', '1'], ['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '1', '0', '0', '1', '0'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '0', '0', '0', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '1', '0', '0', '1', '0'], ['0', '1', '1', '0', '0', '1', '0', '1'], ['0', '1', '1', '1', '0', '0', '0', '1'], ['0', '1', '1', '1', '0', '1', '1', '1'], ['0', '1', '1', '0', '0', '1', '0', '1'], ['0', '1', '1', '1', '0', '0', '1', '0'], ['0', '1', '1', '1', '0', '1', '0', '0'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '0', '1', '0', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '1', '1', '1', '0', '0', '0', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '0', '1', '0', '1', '1'], ['0', '1', '1', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '1', '0', '1', '1'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '0', '1', '0', '1', '0'], ['0', '1', '1', '0', '0', '1', '1', '1'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '0', '1', '1', '0'], ['0', '1', '1', '1', '0', '1', '0', '0'], ['0', '1', '1', '0', '0', '1', '0', '0'], ['0', '1', '1', '0', '0', '1', '0', '1'], ['0', '1', '1', '1', '0', '0', '1', '0'], ['0', '1', '1', '1', '0', '1', '0', '0'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '0', '1', '0', '0', '1'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '1', '0', '1', '1', '0'], ['0', '1', '1', '0', '0', '0', '1', '1'], ['0', '1', '1', '0', '0', '1', '1', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '1', '1', '1', '1', '0', '0', '1'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '0', '1', '0', '0', '1', '1', '1'], ['0', '1', '1', '0', '1', '1', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '0'], ['0', '1', '1', '0', '0', '0', '1', '0'], ['0', '1', '1', '0', '1', '1', '0', '0'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '1', '0', '1', '1', '0'], ['0', '1', '1', '0', '0', '1', '1', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '1', '1', '0', '1', '0', '0', '0'], ['0', '1', '1', '1', '0', '1', '0', '1'], ['0', '1', '1', '0', '1', '1', '1', '1'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '0', '0', '1', '0', '1', '0'], ['0', '1', '1', '1', '1', '0', '0', '0'], ['0', '1', '1', '0', '0', '1', '0', '0']]
