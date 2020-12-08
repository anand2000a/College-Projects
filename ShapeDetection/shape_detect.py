import numpy as np
import cv2

img = cv2.imread('image4.webp')
# img = cv2.resize(img , (720 , 480))
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


cv2.imshow("img", thrash)
for contour in contours:
    if cv2.contourArea(contour) < 5:
        continue
    approx = cv2.approxPolyDP(
        contour, 0.01 * cv2.arcLength(contour, True), True)
    cv2.drawContours(img, [approx], -1, (0, 0, 0), 2)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    if len(approx) == 3:
        cv2.putText(img, "Triangle", (x-30, y),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0))
    elif len(approx) == 4:
        x1, y1, w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        # print(aspectRatio)
        if aspectRatio >= 0.94 and aspectRatio <= 1.05:
            cv2.putText(img, "square", (x, y),
                        cv2.FONT_HERSHEY_COMPLEX, 0.4, (0))
        else:
            cv2.putText(img, "rectangle", (x, y),
                        cv2.FONT_HERSHEY_COMPLEX, 0.4, (0))
    elif len(approx) == 5:
        cv2.putText(img, "Pentagon", (x-30, y),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (0))
    elif len(approx) == 6:
        cv2.putText(img, "hexagon", (x-10, y),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (0))
    elif len(approx) == 7:
        cv2.putText(img, "heptagon", (x-10, y),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (0))
    elif 7 < len(approx) < 15:
        cv2.putText(img, "oval", (x+10, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0))
    else:
        cv2.putText(img, "circle", (x-5, y),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (0))

imgS = cv2.resize(img, (720, 480))
cv2.imshow("shapes", imgS)
cv2.waitKey(0)
cv2.destroyAllWindows()
