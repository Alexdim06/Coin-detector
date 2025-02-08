import numpy as np
import cv2 as cv

def av_pix(original_image, circles, size):
    av_value = [] 
    for coords in circles[0,:]:
        col = np.mean(img[coords[1]-size:coords[1]+size, coords[0]-size:coords[0]+size]) # средна стойност на пикселите
        av_value.append(col)
    return av_value


def get_radius(cirles):
    radius = []
    for i in cirles[0, :]:
        radius.append(i[2])
    return radius
# Черно-бяла снимка на монети
img = cv.imread('capstone_coins.png', cv.IMREAD_GRAYSCALE)
original_image = cv.imread('capstone_coins.png',1)
img = cv.GaussianBlur(img, (5,5), 0)
# намиране на кръгове
circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 0.1,120, param1=20, param2=28, minRadius=60, maxRadius=120)  

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv.circle(original_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv.circle(original_image, (i[0], i[1]), 2, (0, 0, 255), 3)
radii = get_radius(circles)
print(radii)

brigh_vals = av_pix(img, circles, 20)
print(brigh_vals)

values = []
# радиуси и цветове на монетите, които определят стойностите на монетите
for a, b in zip(brigh_vals, radii):
    if a > 90 and a < 95 and b > 100:
        values.append(50)
    elif a > 150 and b > 90:
        values.append(10)
    elif a > 150 and b <= 110:
        values.append(5)    
    elif a < 150 and b > 85:
        values.append(2)
    elif a < 150 and b <= 110:
        values.append(1)        
print(values)
counter_2 = 0
# показване на стойностите на монетите
for i in circles[0,:]:
    cv.putText(original_image, f'{values[counter_2]}p', (i[0], i[1]), cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
    counter_2 += 1
# показване на общата стойност на монетите
cv.putText(original_image, f'Total Estimated Value: {sum(values)}p', (100, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)    
    
cv.imshow('Detected Coins',original_image)
cv.waitKey(0)
cv.destroyAllWindows()