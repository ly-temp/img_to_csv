import cv2

img = cv2.imread('/tmp/img/Scan0001.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 0, 0), (170, 40, 255))
inv_mask = cv2.bitwise_not(mask)
b,g,r = cv2.split(img)
b = cv2.bitwise_and(b,b,inv_mask)
g = cv2.bitwise_and(g,g,inv_mask)
r = cv2.bitwise_and(r,r,inv_mask)
masked = cv2.merge((b,g,r))
cv2.imwrite('out.png', inv_mask)
exit()

from img2table.document import Image
from img2table.ocr import TesseractOCR

ocr = TesseractOCR(lang="eng")

img = Image(src="/tmp/img/Scan0002.jpg")
#img = Image(src="/tmp/img/test.jpg")
img_tables = img.extract_tables(ocr=ocr)
print(img_tables)
for i in img_tables:
    #print(f'{i.title} {i.content}')
    print(i.df)