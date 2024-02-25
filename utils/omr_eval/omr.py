import cv2
import numpy as np
run_debug = True
if run_debug:
    from matplotlib import pyplot as plt
import copy
def debug(text):
    if run_debug:
        print(f"\033[95m{text}\033[0m")

def show_img(image, **kwargs):
    # Display the image with detected rectangles using matplotlib
    plt.imshow(image,**kwargs)
    plt.axis('off')
    plt.show()

def get_orient_marker(xy):
    code = 2
    # Calculate Euclidean distances between all pairs of points
    def euclidean_distances(points):
        return np.sqrt(np.sum((points[:, np.newaxis] - points) ** 2, axis=-1))

    # Find the coordinate with the average farthest distance to all other coordinates
    def find_coordinate_with_average_farthest_distance(coordinates):
        distances = euclidean_distances(coordinates)
        avg_distances = np.mean(distances, axis=1)
        farthest_index = np.argmax(avg_distances)
        return coordinates[farthest_index]

    # Example ordered pairs (points)
    ordered_pairs = np.array(xy)
    print("RESULT")
    # Find the coordinate with the average farthest distance to all other coordinates
    result = find_coordinate_with_average_farthest_distance(ordered_pairs)
    if np.min(ordered_pairs.T[0]) == result[0] and np.max(ordered_pairs.T[1]) == result[1]:
        print('TOP TO LEFT: FLIP TO CLOCKWISE')
        code = 0
    elif np.min(ordered_pairs.T[1]) == result[1] and np.max(ordered_pairs.T[0]) == result[0]:
        print('TOP TO RIGHT: FLIP TO COUNTERCLOCKWISE')
        code = 1
    elif np.min(ordered_pairs.T[0]) == result[0] and np.min(ordered_pairs.T[1]) == result[1]:
        code = 2
    elif np.max(ordered_pairs.T[0]) == result[0] and np.max(ordered_pairs.T[1]) == result[1]:
        print('TOP-TOP: FLIP CLOCKWISE TWICE')
        code = 3
    print("Coordinate with the average farthest distance to all other coordinates:", result)

    return result, code

def process_choices(erode, image, orig_image, get_plot):
    debug('[process_choices] initializing')
    # Find contours with cv2.RETR_CCOMP
    debug('[process_choices] finding contours')
    contours,hierarchy = cv2.findContours(erode,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    code = 2
    rectangles = []
    #circles = []
    for i,cnt in enumerate(contours):
        # Check if it is an external contour and its area is more than 100
        if hierarchy[0,i,3] == -1 and cv2.contourArea(cnt)>100:
            x,y,w,h = cv2.boundingRect(cnt)
            rectangles.append((x,y,w,h))
            #cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

            """m = cv2.moments(cnt)
            cx,cy = m['m10']/m['m00'],m['m01']/m['m00']
            circles.append([int(cx),int(cy)])
            #cv2.circle(image,(int(cx),int(cy)),10,255,-1)"""


    #######################
    #show_img(image)
    # Calculate the areas of rectangles
    debug('[process_choices] finding areas')
    areas = [w * h for x, y, w, h in rectangles]
    #areas = areas = rectangles[:, 2] * rectangles[:, 3]
    # Calculate the interquartfile range (IQR) of areas
    debug('[process_choices] calculating rectangles based on area for filtering')
    Q1 = np.percentile(areas, 25)
    Q3 = np.percentile(areas, 75)
    IQR = Q3 - Q1

    # getting the mean of areas
    meann = np.mean(areas)

    # Define the upper and lower bounds for filtering
    # area size must be around average to include
    lower_bound = meann - (meann*0.75)
    upper_bound = meann + (meann*0.75)
    
    # Create a list indicating whether each rectangle's area is within the interquartile range
    within_IQR = [1 if lower_bound <= area <= upper_bound else 0 for area in areas]
    
    def get_ratio(width,height):
        ratio = width / height

        # Check if the ratio is close to 1 (within the threshold)
        if ratio>=0.75 and ratio <=1.25:
            return 1
        else:
            return 0
    
    # target must be a square or approx.
    debug('[process_choices] calculating rectangles based on W,H ratio')
    is_square = [get_ratio(x[2], x[3]) for x in rectangles ]

    debug('[process_choices] filtering rectangles')
    overall = [sq and iqr for sq,iqr in zip(is_square, within_IQR)]
    #print(overall)
    ## Calculate the ratio of width to height
    true_rectangles = []
    
    # taking rectangles that satisfies area and shape condition
    xy_rect = []
    for i in range(len(rectangles)):
        x,y,w,h = rectangles[i]
        if overall[i] == 1:
            true_rectangles.append(rectangles[i])
            xy_rect.append([x,y])
            #cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),5)
    
    debug('[process_choices] getting orientation')
    # returns code on its orientation and what can be done to reset into upright orientation
    xy, code = get_orient_marker(xy_rect)
    if code == 2:
        pass # correct/desired orientation, skip..
    elif code == 1:
        # head is @ right.
        debug('[process_choices] reprocessing for updated orientation')
        erode = cv2.rotate(erode, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return process_choices(erode, image, orig_image, get_plot)
    elif code == 0:
        print("CODE 0")
        #print(true_rectangles)
        # head is @ left
        debug('[process_choices] reprocessing for updated orientation')
        erode = cv2.rotate(erode, cv2.ROTATE_90_CLOCKWISE)
        return process_choices(erode, image, orig_image, et_plot)
    elif code == 3:
        print("CODE 0")
        #print(true_rectangles)
        # head is @ below (flipped)
        debug('[process_choices] reprocessing for updated orientation')
        debug('[process_choices] reprocessing for updated orientation')
        erode = cv2.rotate(erode, cv2.ROTATE_90_CLOCKWISE)
        erode = cv2.rotate(erode, cv2.ROTATE_90_CLOCKWISE)
        return process_choices(erode, image, orig_image, get_plot)
    
    output = []
    for rect in true_rectangles:
        x,y,w,h = rect
        if x != xy[0] and y != xy[1]:
            output.append(rect)
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),10) if get_plot else None

    return (output, image if get_plot else None, orig_image)



# Example usage
"""x, y, w, h = 100, 100, 200, 100
angle_degrees = 45
x_rot, y_rot, w_rot, h_rot = rotate_rectangle_counterclockwise(x, y, w, h, angle_degrees)
print("Rotated rectangle coordinates:", x_rot, y_rot, w_rot, h_rot)
"""

def get_choices(image, image_is_path = False, get_original=False, get_plot=False):
    # Load an image from file
    debug('[get_choices] initializing')
    if image_is_path:
        image = cv2.imread(image, 0)
    
    debug('[get_choices] getting copy of orig image')
    orig_image = copy.copy(image) if get_original else None

    # Apply adaptive thresholding
    debug('[get_choices] applying adaptive thresh')
    adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    ret, thresh = cv2.threshold(adaptive_thresh, 50, 255, 1)

    #cv2.imwrite("Final Image.jpg", thresh)

    # Load the noisy image

    # Apply Median blur
    debug('[get_choices] applying median blur')
    blurred_image = cv2.medianBlur(thresh, 13)  # Adjust the kernel size (e.g., 5) as needed


    # Display the original and blurred images
    debug('[get_choices] inverting')
    blurred_image = 255-blurred_image
    # Normal routines
    img = blurred_image
    ret,thresh = cv2.threshold(img,50,255,1)

    debug('[get_choices] removing small noises')
    # Remove some small noise if any.
    dilate = cv2.dilate(thresh,None)
    erode = cv2.erode(dilate,None)

    # proceeds to another function (to allow reprocessing based on orientation)
    debug('[get_choices] processing choices')
    return process_choices(erode, image, orig_image, get_plot)
    



def get_rows(true_rectangles):
    """
    Divides bubbles into by row.
    """
    true_rectangles = true_rectangles[::-1]
    max_rows = 25
    #multiplier = max_rows/rows
    true_rectangles = np.array(true_rectangles)
    x = true_rectangles[:,0]
    y = true_rectangles[:,1]
    smallest = (np.min(y))
    largest = (np.max(y))
    interval = (largest-smallest)/max_rows
    interval = interval - (interval*0.5)
    bubbles = []
    temp_bubbles = [true_rectangles[0]]
    previous = true_rectangles[0]
    for rect in true_rectangles[1:]:
        diff = abs(rect[1]-previous[1])
        if abs(diff) <= interval:
            temp_bubbles.append(rect)
        else:
            bubbles.append(temp_bubbles)
            temp_bubbles = []
            temp_bubbles.append(rect)
        previous = rect
    if len(temp_bubbles) > 0:
        bubbles.append(temp_bubbles)
    
    # Sort the list of arrays based on their first value
    return_value = []
    for x in bubbles:
        sorted_arr_list = sorted(x, key=lambda x: x[0])
        return_value.append(sorted_arr_list)
    
    return return_value



def get_type_test(bubbles_rowed,return_word=True, debug=True):
    def process(bubbles_rowed, return_word):
        a = np.array(bubbles_rowed)[0]
        a = np.array(a)[:,0]
        ground_columns = len(a)
        print('columns',ground_columns)
        if ground_columns == 2:
            return 1 if return_word==False else 'TRUE OR FALSE'
        if ground_columns%4==2:
            return 1 if return_word==False else 'TRUE OR FALSE'
        if ground_columns > 4:
            comparison = abs(a[1]-a[2])/abs(a[0]-a[1])
            print(comparison)
            if comparison < 1.8:
                return 0 if return_word==False else 'MULTIPLE CHOICE'
            else:
                return 1 if return_word==False else 'TRUE OR FALSE'
    result = process(bubbles_rowed, return_word)
    
    if debug:
        print("Type of Test:", result)
    return result


def is_valid(ground_rows, ground_cols, total):
    if total == ground_rows*ground_cols:
        return True
    else:
        return False

def get_by_num(circles_per_num,bubbles):
    class Circle:
        def __init__(self, *args):
            self.xywh = args

    result_complete ={}
    result = []
    for i in range(len(bubbles)):
        row = np.array(bubbles)[i]
        # Combine each group of 4 into a rect object
        item_num = 0
        interval = circles_per_num
        for group in row.reshape(-1,circles_per_num):
            result.append(Circle(*group))
            interval-=1
            if interval == 0:
                interval = 4
                
                result_complete[(25*item_num)+i+1] = result
                item_num += 1
                result = []
        item_num = 0
    return result_complete

