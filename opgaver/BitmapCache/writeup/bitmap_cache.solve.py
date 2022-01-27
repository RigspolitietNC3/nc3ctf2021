# python3 -m pip install --upgrade Pillow
from PIL import Image

import glob

bitmapFiles = []
for file in glob.glob("*.bmp"):
    bitmapFiles.append(file)


correctOrder = dict()


for c in bitmapFiles :
	im = Image.open(c)
	pix = im.load()
	print(im.size)
	rbgInBG = pix[1,1]
	print(rbgInBG)
	correctOrder[ rbgInBG[0] ] = c


assert( len(correctOrder) == len(bitmapFiles) )


resultImage = Image.new('RGB', (len(correctOrder) * 32, 64), (250,250,250))

i = 0

for k in sorted(correctOrder) :
	c = correctOrder[k]
	print(k, c)
	im = Image.open(c)
	pix = im.load()
	i += 1
	resultImage.paste( im, ( (len(correctOrder) - i) * 32,0) )


resultImage.save("result.jpg","JPEG")
