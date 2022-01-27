# Bruger: https://xlsxwriter.readthedocs.io/
import xlsxwriter
from PIL import Image

import random


workbook = xlsxwriter.Workbook('nc3ctf2021_regnearket.xlsx')

worksheet = workbook.add_worksheet()
worksheet.insert_image('A1', 'nc3ctf2021_logo_small.png')

worksheet.write('B1', 'Prøv at regne lidt på den her ...')


worksheet = workbook.add_worksheet()
worksheet.hide()

im = Image.open('regnearket_lille.png')
pix = im.load()
print(im.size)

for x in range(0, im.size[0]) :
    for y in range(0, im.size[1]) :
        rgbaInBG = pix[x, y]
        r = rgbaInBG[0]
        g = rgbaInBG[1]
        b = rgbaInBG[2]
        rbgaAsHexString = '0x' + hex(r)[2:] + hex(g)[2:] + hex(b)[2:]
        rgbaAsInt = int(rbgaAsHexString, 0)
        xorKey = random.randrange(0x6e633321)
        rgbaAsInt = rgbaAsInt ^ xorKey
        finalFormula = '=XOR(' + str(rgbaAsInt) + ", " + str(xorKey) + ")"
        worksheet.write(x, y, finalFormula)

        xorKey += x + y
        xorKey += 64

workbook.close()
