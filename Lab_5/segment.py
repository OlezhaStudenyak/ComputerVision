import cv2
from matplotlib import pyplot as plt


# --------------------------- Сегментація на основі порога OTSU -------------------------------
def Segment_Otsu(img, SaveTo):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    plt.imshow(thresh, 'gray')
    plt.axis('off')
    cv2.imwrite(SaveTo, thresh)
    plt.tight_layout()
    plt.show()
    return thresh


def image_processing(image):
    blur = cv2.medianBlur(image, 91)
    edged = cv2.Canny(blur, 100, 250)

    plt.imshow(edged)
    plt.show()

    return edged


def image_contours(image_entrance):
    return cv2.findContours(image_entrance.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]


def image_recognition(image_entrance, image_cont, file_name):
    for c in image_cont:
        peri = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if area > 200:
            cv2.drawContours(image_entrance, [approx], -1, (0, 255, 0), 4)

    cv2.imwrite(file_name, image_entrance)
    plt.imshow(image_entrance)
    plt.show()

    return


if __name__ == "__main__":
    img = cv2.imread('image.png')
    segment = Segment_Otsu(img, 'imgOTSU.jpg')

    image_exit = image_processing(segment)
    image_cont = image_contours(image_exit)

    image_recognition(img, image_cont, "image_recognition_1.jpg")
