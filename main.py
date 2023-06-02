import cv2

img = cv2.imread('/tmp/img/Scan0001.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (100, 15, 100), (170, 255, 255))
inv_mask = cv2.bitwise_not(mask)
out = cv2.bitwise_and(img, img, inv_mask)
out = 255 * (out/255)**30
cv2.imwrite('out.png', out)

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