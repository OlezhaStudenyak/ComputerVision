import cv2 as cv

def sift_feature_matching (filename_1, filename_2):

    img1 = cv.imread(filename_1, cv.IMREAD_GRAYSCALE)
    img2 = cv.imread(filename_2, cv.IMREAD_GRAYSCALE)

    sift = cv.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    matchesMask = [[0, 0] for i in range(len(matches))]

    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]

    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=cv.DrawMatchesFlags_DEFAULT)

    img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

    cv.imshow('sift_feature_matching', img3)
    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()

    return


if __name__ == '__main__':

    sift_feature_matching('img/img1.jpg', 'img/img2.jpg')
    sift_feature_matching('img/img3.jpg', 'img/img4.jpg')
    sift_feature_matching('img/img5.jpg', 'img/img6.jpg')


