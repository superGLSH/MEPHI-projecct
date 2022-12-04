from bchlib import BCH
from PIL import Image
from random import randint


mp_table = [67, 137, 285, 529, 1033, 2053, 4179, 8219, 17475, 32771, 69643]


#print('''Ведите режим работы:
#e - закодировать последовательность байт,
#d - раскодировать последовательность байт''')
#m = input()
m = "e"
if m == 'e':
    print('Введите процент корректируемых ошибок')
    #percent = int(input())
    percent = 20
    print('Введите название файла ввода')
    #inp = input()
    inp = "input.txt"
    with open(inp, mode='rb') as file:
        st = b''
        for ststr in file.readlines():
            print(ststr)
            st += ststr
        print(st)
        if not st:
            print('Ошибка ввода строки: пустая строка')
            quit()
        meslen = len(st)
        parts = 1
        while meslen // parts > 2 ** 12:
            parts *= 2
        while True:
            ecclen = (meslen // parts / (1 - percent / 100)).__ceil__()
            print((meslen // parts / (1 - percent / 100)))
            print(ecclen)
            i = 6
            while i <= 10 and ecclen > mp_table[i] * 0.05:
                i += 1
            if i < 10:
                break
            parts *= 2
        # По невыясненным причинам(не сильно то и хотелось) ecclen < 0.05 * polynom, иначе ошибка.
        # По этой же причине библиотека отказывается работать с m < 6, и они были убраны за ненадобностью.
        polynom = mp_table[i]
        print(polynom, ecclen, meslen, parts)
        coder = BCH(polynom, ecclen)
        for i in list(coder):
            print(i)
        # Для кодировки в фото: 1 байт - знак UTF-8, 13 бит - символ ecc
        # Есть смысл в 13 битах тех данных
    for i in range(parts):
        if i == parts - 1:
            mes = bin(int(st[meslen // parts * i:].hex(), 16))[2:]
            ecc = bin(int(coder.encode(st[meslen // parts * i:]).hex(), 16))[2:]
        else:
            mes = bin(int(st[meslen // parts * i: meslen // parts * (i + 1)].hex(), 16))[2:]
            ecc = bin(int(coder.encode(st[meslen // parts * i: meslen // parts * (i + 1)]).hex(), 16))[2:]
        mes = mes.zfill((len(mes) / 8).__ceil__() * 8)
        ecc = ecc.zfill((len(ecc) / 8).__ceil__() * 8)
        to_write = bin((len(mes) / 8).__ceil__())[2:].zfill(12) + bin(ecclen)[2:].zfill(12) + bin((len(ecc) / 8).__ceil__())[2:].zfill(12) + bin(mp_table.index(polynom))[2:].zfill(4) + mes + ecc
        a = int(len(to_write) ** 0.5 + 1)
        im = Image.new('1', (a, a))
        for j in range(len(to_write)):
            im.putpixel((j % a, j // a), (int(to_write[j]) + j % 2) % 2)
        for j in range(len(to_write), a * a):
            im.putpixel((j % a, j // a), randint(0, 1))
        im.save(f'IMECC/ECC{i + 1}.png')
        # Необходимо предварительно создать директорию IMECC
elif m == 'd':
    print('Введите название файла вывода')
    o = input()
    with open(o, mode='wb') as out:
        parts = int(input('Скока файлов декодируем?\n'))
        for i in range(parts):
            im = Image.open(f'IMECC/ECC{i + 1}.png')
            masked_mes = [im.getpixel((y, x)) for x in range(im.width) for y in range(im.height)]
            unmasked_mes = [(masked_mes[j] + j % 2) % 2 for j in range(im.width * im.height)]
            meslen = int(''.join(map(str, unmasked_mes[:12])), 2)
            ecclen = int(''.join(map(str, unmasked_mes[12:24])), 2)
            lenecc = int(''.join(map(str, unmasked_mes[24:36])), 2)
            coder = BCH(mp_table[int(''.join(map(str, unmasked_mes[36: 40])), 2)], ecclen)
            mes = bytearray.fromhex(hex(int(''.join(map(str, unmasked_mes[40:40 + meslen * 8])), 2))[2:])
            ecc = bytearray.fromhex(hex(int(''.join(map(str, unmasked_mes[40 + meslen * 8: 40 + meslen * 8 + lenecc * 8])), 2))[2:])
            if not ecc:
                print('Ошибка ввода строки: пустая строка')
                quit()
            out.write(coder.decode(mes, ecc)[1])
