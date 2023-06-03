def main():
    import cv2

    img = cv2.imread('/tmp/img/Scan0001.jpg')
    #img = cv2.fastNlMeansDenoising(img, None, 20, 7, 21) 

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (100, 10, 130), (170, 255, 255))
    inv_mask = cv2.bitwise_not(mask)

    #out = img.copy()
    #out[mask!=0] = (255,255,255)

    #edges = cv2.Canny(inv_mask,100,200)
    damaged_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = cv2.inpaint(damaged_image, mask, 0.1, cv2.INPAINT_TELEA)

    gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
            cv2.THRESH_BINARY_INV,9,11)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    #dilate = cv2.dilate(close, kernel, iterations=1)
    out = cv2.bitwise_not(close)
    #out = 255*(out/255)**5

    cv2.imwrite('out.jpg', out)


    from img2table.document import Image
    from img2table.ocr import TesseractOCR

    ocr = TesseractOCR(lang="eng+chi_tra+chi_sim", psm=3)

    img = Image(src="/tmp/img/out.jpg")

    img_tables = img.extract_tables(ocr=ocr)
    for i in img_tables:
        #print(f'{i.title} {i.content}')
        print(i.df)
        #print(i.df.to_csv(f'{i}.csv', sep='\t'))

if __name__ == "__main__":
    main()
