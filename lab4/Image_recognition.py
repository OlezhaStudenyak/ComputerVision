import cv2
from matplotlib import pyplot as plt


def image_read(FileIm):
    image = cv2.imread(FileIm)
    plt.imshow(image)
    plt.show()

    return image


def image_processing(image):
    adjusted = cv2.convertScaleAbs(image, alpha=1, beta=100)
    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 50, 40)
    vect = cv2.Canny(bfilter, 60, 300)

    cv2.imwrite("img_vec.jpg", vect)
    plt.imshow(vect)
    plt.show()

    return vect


def image_contours(image_entrance):
    return cv2.findContours(image_entrance.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]


def image_recognition(image_entrance, contours, file_name):
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)

        x, y, w, h = cv2.boundingRect(contour)

        if len(approx) > 4 and w > 70 and h > 80:
            cv2.drawContours(image_entrance, [approx], -1, (255, 0, 0), 4)  

    cv2.imwrite(file_name, image_entrance)
    plt.imshow(image_entrance)
    plt.show()

    return


if __name__ == '__main__':
    image_entrance = image_read("image.png")

    image_exit = image_processing(image_entrance)

    contours = image_contours(image_exit)

#image_recognition(image_entrance, contours, "image_recognition.png")
