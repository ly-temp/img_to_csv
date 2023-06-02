import os
#os.environ["TESSDATA_PREFIX"] = os.path.realpath("./testdata")

from img2table.document import Image
from img2table.ocr import TesseractOCR

ocr = TesseractOCR(lang="eng", tessdata_dir="./testdata")

#img = Image(src="/tmp/img/Scan0001.jpg")
img = Image(src="/tmp/img/test.jpg")
img_tables = img.extract_tables(ocr=ocr)
print(img_tables)
for i in img_tables:
    #print(f'{i.title} {i.content}')
    print(i.df)