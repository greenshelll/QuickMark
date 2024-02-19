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
image = cv2.imread(r"C:\Users\USER\Downloads\IMG_20240217_113026.jpg", 0)

# Apply adaptive thresholding
adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)


ret, thresh = cv2.threshold(adaptive_thresh, 50, 255, 1)

#cv2.imwrite("Final Image.jpg", thresh)

# Load the noisy image

# Apply Median blur
blurred_image = cv2.medianBlur(thresh, 9)  # Adjust the kernel size (e.g., 5) as needed


# Display the original and blurred images
blurred_image = 255-blurred_image
#cv2.imwrite('bl.png', blurred_image)
#show_img(blurred_image, cmap='gray')
blurred_imag2 = blurred_image
#_---------------------
contours, hierarchy = cv2.findContours(blurred_image, 1, 2)
#print("Number of contours detected:", len(contours))


bounding_rectangles = []

for cnt in contours:
    x1, y1 = cnt[0][0]
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(cnt)
        ratio = float(w) / h
        if ratio >= 0.9 and ratio <= 1.1:
            pass
        else:
            bounding_rectangles.append((x, y, w, h))

#cv2.imwrite('sample.png', image)


# Convert the list of tuples to a list of rectangles
rectangles = [(x, y, x + w, y + h) for x, y, w, h in bounding_rectangles]

# Remove rectangles that are completely contained within another rectangle
reduced_rectangles = []
for rect1 in rectangles:
    is_contained = False
    for rect2 in rectangles:
        if rect1 != rect2:
            if rect1[0] >= rect2[0] and rect1[1] >= rect2[1] and rect1[2] <= rect2[2] and rect1[3] <= rect2[3]:
                is_contained = True
                break
    if not is_contained:
        reduced_rectangles.append(rect1)
    

# Convert the reduced rectangles back to the format of the original list
bounding_rectangles = [(x, y, w, h) for x, y, x2, y2 in reduced_rectangles for w, h in [(x2 - x, y2 - y)]]

numbers = [x[2]*x[3] for x in bounding_rectangles]

# Step 1: Sort the list
sorted_numbers = sorted(numbers)

# Step 2: Create a dictionary of ranks
rank_dict = {number: rank for rank, number in enumerate(sorted_numbers, start=1)}

# Step 3: Retrieve the ranks for each element in the original list
ranks = [rank_dict[number] for number in numbers]

print("Original list:", numbers)
print("Ranks:", ranks)

final_lis = []
print([final_lis.append(bounding_rectangles[i]) if ranks[i]>max(ranks)-3 else None for i in range(len(bounding_rectangles))])
print(final_lis)

for rect in final_lis:
    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
show_img(image, cmap='gray')
