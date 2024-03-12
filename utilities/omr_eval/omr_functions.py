import cv2
import numpy as np
import sys
try:
    import utilities.omr_eval.util4string as u4str
    #from utilities.ocr.function import handwrite_predict
except ModuleNotFoundError as e:
    ##*print(e, 'Getting alt path')
    import util4string as u4str
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
class Debugger:
    def __init__(self):
        self.run_debug = True
        self.funcname = ''
        self.text = ''
        self.show_plot = True
        self.color = [255,255,255]
        
        self.p('Initializing----\nINITIALIZING DEBUGGER\n', italic=True,rgb=[100,0,0],ignore_time=True)
        self.p('Formatting ----\n[FUNCTION NAME] Text Message (TIME TOOK TO ARRIVE FROM PREV TIME RECORD)\n', italic=True,rgb=[100,0,0],ignore_time=True)
        self.time_base = 0
        
    def p(self,text=None, rgb=None,bold=False,italic=False,dim=False,strike=False,underline=False,ignore_time=False,force_show=False):
        if self.run_debug or force_show:
            if not ignore_time:
                import time
                current_time = time.time()
                diff = round((current_time - self.time_base)*1000,4)
                self.time_base = time.time()
            else:
                diff = '?'
            print(u4str.get_asciiface(f'[{self.funcname}] {self.text if text is None else text} (+{diff})', rgb if rgb is not None else self.color,bold,italic,underline,strike,dim))

    def plot(self,image,title='',**kwargs):
        if self.run_debug and self.show_plot:
            import matplotlib.pyplot as plt
            import time
            try:
                # Display the image with detected rectangles using matplotlib
                plt.title(title)
                plt.imshow(image,**kwargs)
                plt.axis('off')
                plt.show()
                self.time_base = time.time()
            except Exception as e:
                ##*print(e)
                pass
    def start_time(self):
        import time
        if self.run_debug:
            self.time_base = time.time()

#_______________________________________________________________________________________________________
db = Debugger()
db.start_time()
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________


def perspective_transform(original_image, max_rect, output_size):
    """
    Apply perspective transform to the original image based on the quadrilateral defined by max_rect.

    Parameters:
        original_image (numpy.ndarray): The original input image.
        max_rect (list): List of four points defining the quadrilateral.
        output_size (tuple): Tuple containing the width and height of the output image.

    Returns:
        numpy.ndarray: The perspective-transformed image.
    """
    # Define the destination points for the perspective transform
    dst_points = np.array([[0, 0], [output_size[0], 0], [output_size[0], output_size[1]], [0, output_size[1]]], dtype=np.float32)

    # Convert max_rect to the format required by cv2.getPerspectiveTransform()
    src_points = np.float32(max_rect)

    # Compute the perspective transform matrix
    perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Apply the perspective transform to the original image
    warped_image = cv2.warpPerspective(original_image, perspective_matrix, output_size)

    return warped_image


def get_output_size(max_rect):
    """
    The function `get_output_size` calculates the width and height of the bounding box of a
    quadrilateral defined by four points.
    
    :param max_rect: It seems like you were about to provide the `max_rect` parameter for the
    `get_output_size` function, but the values are missing. Could you please provide the list of four
    points defining the quadrilateral so that I can assist you in calculating the output size for
    perspective transformation?
    """
    """
    Calculate the output size for perspective transformation based on the bounding box of the quadrilateral.

    Parameters:
        max_rect (list): List of four points defining the quadrilateral.

    Returns:
        tuple: Tuple containing the width and height of the output image.
    """
    # Convert the list of points to a NumPy array for easier manipulation
    # 
    db.p('getting perspective size')
    max_rect = np.array(max_rect).reshape(-1, 2)
    ###*print(max_rect)
    # Find the minimum and maximum x and y coordinates of the quadrilateral
    min_x = np.min(max_rect[:, 0])
    max_x = np.max(max_rect[:, 0])
    min_y = np.min(max_rect[:, 1])
    max_y = np.max(max_rect[:, 1])

    # Calculate the width and height of the bounding box
    width = max_x - min_x
    height = max_y - min_y

    return int(width), int(height)



def distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_quad_angles(points):
        """
        Compute the angles of a quadrilateral given its four points.
        
        Args:
        - points (list of tuples): Four points representing the quadrilateral, each tuple containing (x, y) coordinates.
        
        Returns:
        - angles (list of floats): List of angles (in degrees) of the quadrilateral.
        """
        def compute_angle(p1, p2, p3):
            """Compute the angle between three points."""
            v1 = np.array(p1) - np.array(p2)
            v2 = np.array(p3) - np.array(p2)
            dot_product = np.dot(v1, v2)
            magnitude_v1 = np.linalg.norm(v1)
            magnitude_v2 = np.linalg.norm(v2)
            angle_rad = np.arccos(dot_product / (magnitude_v1 * magnitude_v2))
            angle_deg = np.degrees(angle_rad)
            return angle_deg
        
        # Compute angles between consecutive points
        angles = []
        for i in range(len(points)):
            angle = compute_angle(points[i], points[(i+1)%len(points)], points[(i+2)%len(points)])
            angles.append(angle)
        ###*print(angles)
        return np.array(angles)
def flip_points_horizontal(points):
    flipped_points = [[-point[0], point[1]] for point in points]
    return flipped_points
def flip_points_vertical(points):
    flipped_points = [[point[0], -point[1]] for point in points]
    return flipped_points
def rotate_points_90_degrees(points):
    rotated_points = [[-point[1], point[0]] for point in points]
    return rotated_points
def direction_between_points(points):
    def direction(p1, p2):
        p1, p2 = np.array(p1), np.array(p2)
        vector = p2 - p1
        direction = vector / np.linalg.norm(vector)
        direction = np.round(direction)
        return direction

    directions = []
    for i in range(len(points) - 1):  # Loop over all points except the last one
        directions.append(direction(points[i], points[i+1]))

    return np.array(directions)


def is_correct(directions, custom_correct=None):
    if custom_correct is None:
        correct = np.array([[ 1.,  0.],
       [ 0.,  1.],
       [-1.,  0.]])
    else:
        correct = custom_correct
    
    db.p(f'current\n{directions}')
    db.p(f'correct\n{correct}')
    if np.sum(directions != correct) == 0:
        return True
    else:
        return False

def operate_orient(points):
    points = np.array(points).reshape(4,2)
    operations = [flip_points_horizontal,flip_points_vertical,rotate_points_90_degrees]
    operations_actual = ['horizontal flip', 'vertical flip', '90 degrees rotate']
    operations_actual = [lambda x: cv2.flip(x, 1), lambda x: cv2.flip(x,0), lambda x: cv2.rotate(x, cv2.ROTATE_90_COUNTERCLOCKWISE)]
    operation_sequence = []
    ground = direction_between_points(points)
    current = []
    while True:
        stop = False
        for op_i in range(len(operations)):
            current = operations[op_i](points)
            ##*print(operations[op_i])
            operation_sequence.append(operations_actual[op_i])
            directions = direction_between_points(current)
            if is_correct(directions):
                stop = True
                ##*print("STOPING")
                break
        if stop:
            break
        points = current
        if is_correct(ground, direction_between_points(current)):
            break
        
    return operation_sequence



def good_angles(points, threshold = 80):
    """
    This Python function checks if a set of points forms a quadrilateral with no angles less than or
    equal to 60 degrees.
    
    :param points: It seems like the code snippet you provided is a method called `angles_are_good`
    that takes in a list of points as input. The method calculates the angles of the quadrilateral
    formed by the points and checks if there is any angle less than or equal to 60 degrees. If there
    is at
    :return: If the `has_small_angle` variable is `True`, then `False` is being returned. Otherwise,
    `True` is being returned.
    """
    angles = get_quad_angles(points)
    # gets boolean with less than 60 degrees angle
    has_small_angle = sum(angles <= threshold) > 0
    if has_small_angle:
        return False
    else:
        return True
    
def xywh_to_points(xywh):
    db.p('xywh to points')
    x, y, w, h = xywh
    x1, y1 = x, y
    x2, y2 = x + w, y
    x3, y3 = x + w, y + h
    x4, y4 = x, y + h
    db.p('xywh translated to points')
    return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

def get_bubbles(BubbleGetter_obj, BoxGetter_obj, CaptureSheet_obj, boxes_num, redo=False, use_rect=True):
    """
    The function `get_bubbles` processes an image to detect and extract bubble contours based on certain
    criteria.
    
    :param BubbleGetter_obj: The `BubbleGetter_obj` parameter seems to be a custom object or class that
    is used to retrieve bubble data. It likely contains methods or attributes related to fetching
    information about bubbles in a specific context
    :param BoxGetter_obj: The `BoxGetter_obj` parameter in the `get_bubbles` function seems to be an
    object that contains cropped images. It is used to retrieve a specific cropped image from a
    collection of cropped images based on the `boxes_num` parameter provided to the function. The
    function then performs image processing operations
    :param CaptureSheet_obj: The `CaptureSheet_obj` parameter seems to be an object that contains
    methods or attributes related to capturing and processing images of a sheet. In the provided code
    snippet, it is used to access methods like `get_result_img` and `show_plots`
    :param boxes_num: The `boxes_num` parameter in the `get_bubbles` function is used to specify which
    box number to process. It is used to access the corresponding image crop from the `BoxGetter_obj`
    object. This image crop will then be processed to detect and extract bubbles from it
    """

    db.funcname = 'get_bubbles'
    db.color = [0,100,200]
    db.p('Start',bold=True)
    try:
        get_result_img = CaptureSheet_obj.get_result_img
        show_plots = CaptureSheet_obj.show_plots and get_result_img
        db.p('transforming image perspective')
        op_seq = operate_orient(BoxGetter_obj.orient_matrix[boxes_num])
        ##*print(op_seq)
        BoxGetter_obj.orient_operations.append(op_seq)
        size = get_output_size(BoxGetter_obj.orient_matrix[boxes_num])
        if redo == True:
            size = size[::-1]
        transform = perspective_transform(CaptureSheet_obj.orig_img, BoxGetter_obj.orient_matrix[boxes_num], size)
        db.p('Applying transformation')
        for operation in BoxGetter_obj.orient_operations[boxes_num]:
            transform = operation(transform)
        db.p(transform.shape)
        transform = resize_image_to_max_side(transform, 1280)
        db.plot(transform)
        db.p(transform.shape)
        BoxGetter_obj.crops.append(transform)
        #transform = resize_image_to_max_side(image, 1280)
        #
        db.plot(transform, 'crop+perspective transformed')
        image = BoxGetter_obj.crops[boxes_num]
        #
        #image = resize_image_to_max_side(image, 320)
        #image = cv2.equalizeHist(image)
        db.p('applying adaptive thresh')
        """kernel = np.array([[-1, -1, -1],
                   [-1, 9, -1],
                   [-1, -1, -1]])

        # Apply the kernel to sharpen the image
        image = cv2.filter2D(image, -1, kernel)"""
        adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        db.p(image)
        # Invert the thresholded image
        #
        db.p('inverting thresh')
        adaptive_thresh = 255 - adaptive_thresh

        db.p('finding contours')
        contours, hierarchy = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        #CaptureSheet_obj.count = len(contours)
        #if CaptureSheet_obj.count == 0:
            #CaptureSheet_obj.count = 'None'
        #
        #db.p(f'contours total -- {len(contours)}')
        
        rectangles=[]
        # Filter contours based on area
        # Filter quadrilaterals
        total_area = (image.shape[0]*image.shape[1])
        constant = 1511.9066666
        benchmark_area = total_area/constant
        
        #
        db.p('iterating contours')
        count = 0
        iteration_count = 0
        for i, contour in enumerate(contours):
            iteration_count+=1
            ##*print(iteration_count)
            area = cv2.contourArea(contour)

            # Process the contour only if its area is greater than 50
            # Approximate contour to simplify shape
            epsilon = 0.04 * cv2.arcLength(contour, True)
            ###*print(benchmark_area)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            ###*print(np.array(approx[0]))
            #cv2.drawContours(image, [approx], -1, (0, 255, 0), 2) if db.show_plot else None
            ##*print('benchmaerk min',benchmark_area-(benchmark_area*0.7))
            ##*print('benchamerk max',benchmark_area*200)
            ##*print("SHAPE",len(approx))
            ##*print('own', (area))
            #print(benchmark_area*0.5)
            if use_rect == True:
                approx = cv2.boundingRect(contour)
    
                # Draw the rectangle on the original image (optional)
                #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if len(approx) == 4 and ((area > (benchmark_area*0.9)  and area < benchmark_area*10)) :
                
                #cv2.drawContours(image, [approx], -1, (0, 255, 0), 2) if db.show_plot else None    
                ###*print('stnd',(image.shape[0]*image.shape[1])/300)
                # Check if the contour has 4 vertices (a quadrilateral)
                if use_rect == False:
                    x, y, w, h = cv2.boundingRect(approx)
                    ok = good_angles(np.array(approx).reshape(4,2),60)
                else:
                    x, y, w, h = approx
                    ok = good_angles(xywh_to_points(approx),60)
                
                if not ok:
                    ##*print("NOT OK")
                    continue
                
                ##*print("OK")
                # Calculate width-to-height ratio
                if h != 0:  # Avoid division by zero
                    ratio = w / h
                    
                    ###*print(ratio)
                    valid_area = (area > benchmark_area*10)
                    ###*print(valid_area)
                    if (ratio >= 0.7 and ratio <= 1.3):
                        not_inside = True
                        for rect in rectangles:
                            x_center = x + w / 2
                            y_center = y + h / 2
                            rectx_center = rect[0] + rect[2]/2
                            recty_center = rect[1] + rect[3]/2
                            
                            if distance((rectx_center,recty_center),(x_center,y_center)) < 10:
                                ##*print("DISTANCE IS INSIDE")
                                not_inside=False
                                continue
                        if not_inside:
                            ##*print("IS NOT INSIDE")
                            rectangles.append((x,y,w,h))
                            #cv2.rectangle(image, (x, y), (x + w, y + h), (255,0,0), 5)
                            
                            ##*print(rectangles)
                            count += 1
                            ##*print(count)

                            
        #
        db.plot(image, 'perspective transformed')
        #db.p('qualified contoures ---',len(rectangles))
        #
        BubbleGetter_obj.count = count
        db.p('numbers---'+str(count))
        BubbleGetter_obj.rectangles = rectangles
        db.p('done',bold=True)
        db.p(BoxGetter_obj.crops[boxes_num].shape)     
            
    except Exception as e:
        db.p(e, rgb=[255,0,0])

def sort_matrix(array, by):
    """
    Sorts the rows of a 2D array based on the values in the first column.

    Args:
    - array (numpy.ndarray): Input 2D array.

    Returns:
    - sorted_array (numpy.ndarray): Sorted 2D array.
    """
    sorted_indices = np.argsort(array[:, by])  # Get indices that would sort the array by the first column
    sorted_array = array[sorted_indices]  # Use the sorted indices to reorder the rows
    return sorted_array

def get_by_num(circles_per_num,bubbles,CaptureSheet_obj):
    # The above Python code defines a class `Circle` with an `__init__` method that takes variable
    # arguments and initializes the `xywh` attribute with the arguments. It then iterates over a list
    # of `bubbles`, sorts each row of the list, groups elements into sets of 4, creates `Circle`
    # objects from each group, and stores them in a dictionary `result_complete` where the key is
    # calculated based on the item number and index. Finally, it returns the `result_complete`
    # dictionary.
    try:
        ##*print(circles_per_num)
        class Circle:
            def __init__(self, *args):
                self.xywh = args

        result_complete ={}
        result = []
        ###*print(bubbles)
        for i in range(len(bubbles)):
            row = np.array(bubbles)[i]
            row = sort_matrix(row,1 if CaptureSheet_obj.on_android else 0)
            # Combine each group of 4 into a rect object
            item_num = 0
            interval = circles_per_num
            ###*print(row)
            
            for group in row.reshape(-1,4):
                result.append(Circle(*group))
                interval-=1
                if interval == 0:
                    interval = circles_per_num
                    
                    result_complete[(25*item_num)+i+1] = result
                    item_num += 1
                    result = []
            item_num = 0
        ###*print("RESULT",result_complete)
        return result_complete
    except Exception as e:
        ##*print('Get By Num', e)
        pass


def get_scores(BubbleGetter_obj, BoxGetter_obj, CaptureSheet_obj, boxes_num):
    try:
        scores = {'0010': 'C', '0100': 'B', '0000': 'None', '1000':'A', '0001': 'D','01':'False','10':'True','00':'None'}
        choices_by_num = BubbleGetter_obj.choices_by_num
        image = BoxGetter_obj.crops[boxes_num]
        bin_scores = []
        inta = 0
        filled = []
        non_filled =[]
        
        for number in choices_by_num.keys():
            ##*print(number)
            ##*print(choices_by_num[number])
            temp = []
            for rect in choices_by_num[number]:
                ##*print(rect.xywh)
                rect_output = 0
                x,y,w,h = rect.xywh
                cropped_image = 255-image[y:y+h, x:x+w]
                ##*print("RAW")
                rate2 = np.sum(cropped_image[cropped_image >= np.mean(cropped_image)])
                ##*print(rate2)
                cropped_image = cv2.adaptiveThreshold(cropped_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, cropped_image.shape[0] - 1 - cropped_image.shape[0]%2, 2)
                rate2 = np.sum(255-cropped_image)/np.sum(np.ones(cropped_image.shape))
                ##*print(rate2)
                #db.plot(cropped_image)
                #rate = np.sum(255-(cropped_image>190)*255)
                ###*print("IMG")
                
                rate = np.sum(cropped_image)*3
                ##*print(rate)
                ##*print(np.mean(cropped_image))
                inta+=1
                ##*print(inta-np.mean(cropped_image))
                #.plot(cropped_image)
                if rate2 < 90:
                    rect_output = rate
                    filled.append(rate)
                else:
                    non_filled.append(rate)
                
                temp.append(rect_output)
            # get intended answer
            index_maximum = temp.index(np.max(temp))
            
            for circle_i in range(len(temp)):
                if circle_i == index_maximum and temp[circle_i] != 0:
                    temp[circle_i] = '1'
                else:
                    temp[circle_i] = '0'
            temp = ''.join(temp)
            bin_scores.append(scores[temp])
        BubbleGetter_obj.answers = bin_scores
        ##*print(bin_scores)
        score = 0
        
        ground_truth = CaptureSheet_obj.mcq.correct if BubbleGetter_obj.test_type == 'MULTIPLE CHOICE' else CaptureSheet_obj.tfq.correct
        for correct,answer in zip(ground_truth, BubbleGetter_obj.answers):
            if correct == answer:
                score += 1
        BubbleGetter_obj.final_score = score
        ##*print("SCORE:",score)
    except Exception as e:
        db.p(e)


        
            
def evaluate_identification(CaptureSheet_obj, bubbles):
    cropped_image = CaptureSheet_obj.boxes.crops[0]
    sorted_indices = np.argsort(bubbles[0][:, 0])

    # Sort the array based on the sorted indices
    sorted_data = bubbles[0][sorted_indices]
    image  = cropped_image
    image =  cv2.adaptiveThreshold(cropped_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, cropped_image.shape[0] - 1 - cropped_image.shape[0]%2, 2)
    #db.plot(image)
    for charbox in sorted_data:
        # Calculate the new width and height
        x,y,w,h = charbox
        new_w = int(w * 0.8)
        new_h = int(h * 0.8)

        # Calculate the difference in width and height
        diff_w = w - new_w
        diff_h = h - new_h

        # Calculate the new top-left coordinates to maintain the same center
        new_x = x + diff_w // 2
        new_y = y + diff_h // 2
        
        cro = image[new_y:new_y+new_h, new_x:new_x+new_w]

        # Apply the sharpening kernel to the image
        #cro = cv2.filter2D(cro, -1, sharpening_kernel)
        print(cro.shape)
        #cro = cv2.GaussianBlur(cro, (5,5), 0)
        print(np.unique(cro))
        cv2.imwrite('0.png',cro)
        db.plot(cro)
        #cv2.rectangle(image, (x, y), (x + w, y + h), (0,255,0), 20)
        #print(handwrite_predict([cro]))


def get_choices_by_num(BubbleGetter_obj, BoxGetter_obj, CaptureSheet_obj, box_index, **kwargs):
    """
    This Python function takes input objects and parameters to identify the test type based on the
    number of choices, process the choices, and annotate the image accordingly.
    
    :param BubbleGetter_obj: BubbleGetter_obj is an object that likely contains information about
    bubbles or choices in a test sheet. It seems to be used to retrieve rectangles representing bubbles
    in the test sheet
    :param BoxGetter_obj: BoxGetter_obj is an object that contains information about the boxes in the
    program. It likely has attributes or methods related to cropping images or working with image boxes
    :param CaptureSheet_obj: CaptureSheet_obj is an object that likely contains information about
    capturing and processing sheets, such as images of test sheets. It seems to have methods like
    get_result_img and show_plots, which are used in the function get_choices_by_num. The function uses
    this object to retrieve information needed for processing test choices
    :param box_index: The `box_index` parameter in the `get_choices_by_num` function is used to specify
    the index of the box crop that you want to process. This index is used to access the corresponding
    box crop from the `BoxGetter_obj.crops` list within the function
    """
    db.funcname = 'get_choices_by_num'
    db.color = [200,150,0]
    db.p('Start',bold=True)
    get_result_img = CaptureSheet_obj.get_result_img
    show_plots = CaptureSheet_obj.show_plots and get_result_img

    try:
        num_choices, bubbles = get_rows(BubbleGetter_obj.rectangles,CaptureSheet_obj)
        ##*print('BUBBLES',bubbles)
        test_type_str=None
        if num_choices == 4:
            test_type_str = 'MULTIPLE CHOICE'
        elif num_choices == 2:
            test_type_str = 'TRUE OR FALSE'
        elif num_choices ==1:
            test_type_str = 'IDENTIFICATION'
        else:
            test_type_str = 'IDENTIFICATION'
        #
        db.p(f'Test Type: {test_type_str}')
        BubbleGetter_obj.test_type = test_type_str
        if test_type_str == 'IDENTIFICATION':
            evaluate_identification(CaptureSheet_obj, bubbles)
            return None

        result = get_by_num(num_choices, bubbles, CaptureSheet_obj)
        ##*print('RESULT',result)
        image = BoxGetter_obj.crops[box_index]
        ##*print(result.keys())
        BubbleGetter_obj.choices_by_num = result
        return None
        # STOP HERE
        for number in result.keys():
            ###*print(number)
            ###*print(result[number])
            for rect in result[number]:
                ###*print(rect.xywh)
                x,y,w,h = rect.xywh
                #cv2.rectangle(image, (x, y), (x + w, y + h), (255,0,0), 5)
            #db.plot(image)
        
    except Exception as e:
        db.p(e, rgb=[255,0,0])


def resize_image_to_max_side(image, max_side_length):
    # The above code is a Python function that resizes an image while maintaining its aspect ratio. It
    # first determines the dimensions of the image (height and width), then checks whether the image
    # is in landscape or portrait orientation. Based on the orientation, it calculates the new
    # dimensions for resizing the image while keeping the maximum side length specified by the
    # variable `max_side_length`. Finally, it resizes the image using OpenCV's `cv2.resize` function
    # with the calculated new width and height, and returns the resized image.
    # Get the dimensions of the image
    #
    db.p('resizing image')
    height, width = image.shape[:2]
    
    # Determine which side is larger
    if width >= height:  # Landscape orientation
        # Resize based on width
        new_width = max_side_length
        new_height = int(height * (max_side_length / width))
    else:  # Portrait orientation
        # Resize based on height
        new_height = max_side_length
        new_width = int(width * (max_side_length / height))

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    return resized_image

def get_rows(true_rectangles,CaptureSheet_obj):
    """
    Divides bubbles into by row.
    """
    try:
        true_rectangles = true_rectangles[::-1]
        #multiplier = max_rows/rows
        # convert to np array
        true_rectangles = np.array(true_rectangles)
        #preview
        db.p("GETTING COLUMNS")
        mat = true_rectangles
        ###*print(mat)
        
        sorted_indices = np.argsort(mat[:, 0 if CaptureSheet_obj.on_android else 1])
        
        sorted_mat = mat[sorted_indices]
        
        diff = np.diff(sorted_mat[:,0 if CaptureSheet_obj.on_android else 1])
        ###*print(diff)
        by_rows = []
        temp = []
        ##*print('MAT',sorted_mat.shape)
        for rowi in range(len(sorted_mat)):
            if rowi != len(sorted_mat)-1:
                if abs(diff[rowi]) > 15:
                    ##*print(diff[rowi])
                    temp.append(sorted_mat[rowi])
                    by_rows.append(temp)
                    temp = []
                else:
                    ###*print(sorted_mat[rowi])
                    temp.append(sorted_mat[rowi])
            else:
                temp.append(sorted_mat[rowi])
                by_rows.append(temp)
        
        if len(by_rows[0]) == 1:
            by_rows = by_rows[1:]
        ###*print(np.array(by_rows).shape)
        ###*print('geting y')
        mat = np.array(by_rows[0])
        ###*print('aas')
        db.p('GETTING ROWS')
        sorted_indices = np.argsort(mat[:, 1 if CaptureSheet_obj.on_android else 0])
        image = CaptureSheet_obj.boxes.crops[0]
        sorted_mat = mat[sorted_indices]
        print(sorted_mat)
        for rect in sorted_mat:
            ###*print(rect.xywh)
            x,y,w,h = rect
            #cv2.rectangle(image, (x, y), (x + w, y + h), (255,0,0), 5)
        db.plot(image)
        diff = np.diff(sorted_mat[:,1 if CaptureSheet_obj.on_android else 0])
        ###*print(diff)
        ###*print('diff\n',diff)
        threshold = (np.max(diff) + np.min(diff))/2
        ###*print(threshold)
        choices = diff > threshold
        ###*print(choices)
        ###*print(sorted_indices)
        ###*print(choices)
        if np.any(choices):
            
            # Get the index of the first choice that satisfies the condition
            index = np.where(choices)[0][0] + 1
            ###*print(index)
        else:
            index = len(sorted_mat[:,0])
        ###*print(index)

        num_choices = index
        print("NUM CHOCIES", num_choices)
        db.p(f'num choices: {num_choices}')
        ##*print("BYROWS")
        for x in by_rows:
            ##*print("ADDASDADD")
            ##*print(np.array(x).shape)
            pass
        return num_choices, np.array(by_rows)
    except Exception as e:
        ##*print('omr.get_rows: ',e)
        pass

def scale_coordinates(point, original_width, new_width):
    """
    Scale coordinates from original width to new width.
    """
    original_x, original_y = point
    scale_factor = new_width / original_width
    new_x = int(original_x * scale_factor)
    new_y = int(original_y * scale_factor)
    return new_x, new_y

def scale_coordinates(low_res_coords, low_res_dims, high_res_dims):
    """
    Scale coordinates from low resolution to high resolution maintaining proportionality.
    
    Args:
        low_res_coords (numpy.array): Array of coordinates in the low-resolution image.
        low_res_dims (tuple): Dimensions of the low-resolution image (width, height).
        high_res_dims (tuple): Dimensions of the high-resolution image (width, height).
        
    Returns:
        numpy.array: Array of scaled coordinates in the high-resolution image.
    """
    # Unpack dimensions
    low_res_width, low_res_height = low_res_dims
    high_res_width, high_res_height = high_res_dims
    
    # Calculate proportions
    x_proportions = low_res_coords[:, :, 0] / low_res_width
    y_proportions = low_res_coords[:, :, 1] / low_res_height
    
    # Scale coordinates to high-resolution image
    high_res_x = x_proportions * high_res_width
    high_res_y = y_proportions * high_res_height
    
    # Combine x and y coordinates into a single array
    high_res_coords = np.stack((high_res_x, high_res_y), axis=2)
    
    return high_res_coords

def get_boxes(BoxGetter_obj,CaptureSheet_obj, boxes_num): 
    """extracts boxes

    Args:
        image (string or array): can be np array or path
        boxes_num (int): number of box to take. (Prioritizes biggest boxes first)
        image_is_path (bool, optional): Specifiy if image is a path or an array. Defaults to False.
        get_plot (bool, optional): process plot as image with box. Defaults to False.
        get_np_orig (bool, optional): gets original image as np array. Defaults to True.

    Returns:
        tuple: (box, image, crops, original image)
            box: xywh for each element
            image: image with 
    """
    db.funcname = 'get_boxes'
    fclr = [125,0,125]
    db.color=fclr
    try:
        scaler = 4
        get_result_img = CaptureSheet_obj.get_result_img
        db.show_plot = CaptureSheet_obj.show_plots and get_result_img
        
        #
        db.p('Start',bold=True)
        if get_result_img:
            result_img = CaptureSheet_obj.orig_img
        image = CaptureSheet_obj.orig_img
        image = resize_image_to_max_side(image.copy(), int(1280/scaler))
        #
        #image = cv2.equalizeHist(image)
        db.p('applying adaptive thresh',fclr)
        adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # Invert the thresholded image
        db.p('inverting thresh',fclr)
        adaptive_thresh = 255 - adaptive_thresh

        #
        db.p('finding contours',fclr)
        contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        rectangles=[]
        db.p('filtering contours',fclr)
        max_rect = None
        max_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            # Process the contour only if its area is greater than 50
            if area < 1000:
                continue
            # Approximate contour to simplify shape
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            #x, y, w, h = cv2.boundingRect(approx)
            # Sort the vertices based on their x-coordinate
           
            # Check if the contour has 4 vertices (a quadrilateral)
            if len(approx) == 4:
                if area > max_area:
                    
                    max_area = area
                    max_rect=approx
        max_rect = scale_coordinates(max_rect, image.shape, CaptureSheet_obj.orig_img.shape).astype(int)
        #max_rect = max_rect.astype(int)
        #max_rect=  reorder_points(max_rect)
        CaptureSheet_obj.boxes.rectangles = [max_rect]
        #
        
        BoxGetter_obj.orient_matrix.append(max_rect)
        
        
        db.p('Done',bold=True)
    except Exception as e:
        db.p(e, rgb=[255,0,0])
        pass


