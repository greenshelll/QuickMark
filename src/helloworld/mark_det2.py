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

# Read image. 
img = cv2.imread('1.png', cv2.IMREAD_COLOR) 
  
# Convert to grayscale. 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
#
import cv2
import numpy as np
from matplotlib import pyplot as plt

def show_img(img, cmap=None):
    plt.figure(figsize=(8, 6))
    plt.imshow(img, cmap=cmap)
    plt.axis('off')
    plt.show()

# Load an image from file
image = cv2.imread(r"1.png", 0)

# Apply adaptive thresholding
adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

# Display the original and thresholded
ret, thresh = cv2.threshold(adaptive_thresh, 50, 255, 1)

# Apply Median blur
blurred_image = cv2.medianBlur(thresh, 7)  # Adjust the kernel size (e.g., 5) as needed

# Display the original and blurred images
blurred_image = 255-blurred_image

"""#
# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) """
  
# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(blurred_image,  
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
               param2 = 25, minRadius = 1, maxRadius = 40) 
  
# Draw circles that are detected. 
if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
  
    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Draw the circumference of the circle. 
        cv2.circle(blurred_image, (a, b), r, (0, 255, 0), 5) 
  
        # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(blurred_image, (a, b), 1, (0, 0, 255), 50) 
        #cv2.imshow("Detected Circle", img)
show_img(blurred_image)