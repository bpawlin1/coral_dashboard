import cv2
import matplotlib.pyplot as plt


def showImage(img):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.subplot(2, 2, 1)
    plt.title("Original")
    plt.imshow(image)
    hgt, wdt = image.shape[:2]
    start_row, start_col = int(hgt * .15), int(wdt * .15)
    end_row, end_col = int(hgt * .85), int(wdt * .85)
    cropped = image[start_row:end_row , start_col:end_col]
    cropped_final = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    plt.subplot(2, 2, 2)
    plt.imshow(cropped)
    cv2.imwrite('saved.jpg', cropped_final)

img = cv2.imread("IMG_8537.JPG")
showImage(img)

def drawRegions(source, res, regions, color=(0, 0, 255), size=4):
    for (x, y, w, h) in regions:
        res[y: y + h, x: x + w] = source[y: y + h, x: x + w]
        cv2.rectangle(res, (x, y), (x + w, y + h), color, size)
    return res