import cv2
import numpy as np
from matplotlib import pyplot as plt

def show_img(image, **kwargs):
    # Display the image with detected rectangles using matplotlib
    plt.imshow(image,**kwargs)
    plt.axis('off')
    plt.show()

def show_img(img, cmap=None):
    plt.figure(figsize=(8, 6))
    plt.imshow(img, cmap=cmap)
    plt.axis('off')
    plt.show()

# Load an image from file
image = cv2.imread(r"C:\Users\USER\Downloads\IMG_20240218_184648.jpg", 0)

# Apply adaptive thresholding
adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)


ret, thresh = cv2.threshold(adaptive_thresh, 50, 255, 1)

#cv2.imwrite("Final Image.jpg", thresh)

# Load the noisy image

# Apply Median blur
blurred_image = cv2.medianBlur(thresh, 9)  # Adjust the kernel size (e.g., 5) as needed


# Display the original and blurred images
blurred_image = 255-blurred_image
# Normal routines
img = blurred_image
ret,thresh = cv2.threshold(img,50,255,1)

# Remove some small noise if any.
dilate = cv2.dilate(thresh,None)
erode = cv2.erode(dilate,None)

# Find contours with cv2.RETR_CCOMP
contours,hierarchy = cv2.findContours(erode,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

rectangles = []
for i,cnt in enumerate(contours):
    # Check if it is an external contour and its area is more than 100
    if hierarchy[0,i,3] == -1 and cv2.contourArea(cnt)>100:
        x,y,w,h = cv2.boundingRect(cnt)
        rectangles.append((x,y,w,h))
        #cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

        m = cv2.moments(cnt)
        cx,cy = m['m10']/m['m00'],m['m01']/m['m00']
        cv2.circle(img,(int(cx),int(cy)),3,255,-1)

"""show_img(image, cmap='gray')
cv2.imwrite('sofsqure.png',img)
print(rectangles)
"""

numbers = [x[2]*x[3] for x in rectangles]

# Step 1: Sort the list
sorted_numbers = sorted(numbers)

# Step 2: Create a dictionary of ranks
rank_dict = {number: rank for rank, number in enumerate(sorted_numbers, start=1)}

# Step 3: Retrieve the ranks for each element in the original list
ranks = [rank_dict[number] for number in numbers]

print("Original list:", numbers)
print("Ranks:", ranks)

final_lis = []
print([final_lis.append(rectangles[i]) if ranks[i]>max(ranks)-3 else None for i in range(len(rectangles))])
print(final_lis)

num = 0
for rect in final_lis:
    x, y, w, h = rect
    num+=1
    cv2.imwrite(f'{num}.png',image[y:y+h, x:x+w])
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
show_img(image, cmap='gray')