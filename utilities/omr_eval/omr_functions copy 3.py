import cv2
import numpy as np
import sys
try:
    import utilities.omr_eval.util4string as u4str
except ModuleNotFoundError as e:
    print(e, 'Getting alt path')
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
                print(e)
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
    #print(max_rect)
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
        #print(angles)
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
    operated_current = None
    while True:
        stop = False
        for op_i in range(len(operations)):
            current = operations[op_i](points)
            print(operations[op_i])
            operation_sequence.append(operations_actual[op_i])
            directions = direction_between_points(current)
            if is_correct(directions):
                stop = True
                print("STOPING")
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
    


def get_bubbles(BubbleGetter_obj, BoxGetter_obj, CaptureSheet_obj, boxes_num):
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
    print("STARTING")
    db.p('Start',bold=True)
    try:
        get_result_img = CaptureSheet_obj.get_result_img
        show_plots = CaptureSheet_obj.show_plots and get_result_img
        image = BoxGetter_obj.crops[boxes_num]
        #
        #image = resize_image_to_max_side(image, 320)
        #image = cv2.equalizeHist(image)
        db.p('applying adaptive thresh')
        adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # Invert the thresholded image
        #
        db.p('inverting thresh')
        adaptive_thresh = 255 - adaptive_thresh

        db.p('finding contours')
        contours, hierarchy = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        CaptureSheet_obj.count = len(contours)
        if CaptureSheet_obj.count == 0:
            CaptureSheet_obj.count = 'None'
        #
        db.p(f'contours total -- {len(contours)}')
        
        rectangles=[]
        # Filter contours based on area
        # Filter quadrilaterals
        total_area = (image.shape[0]*image.shape[1])
        constant = 1511.9066666
        benchmark_area = total_area/constant
        
        #
        db.p('iterating contours')
        count = 0
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)

            # Process the contour only if its area is greater than 50
            # Approximate contour to simplify shape
            epsilon = 0.04 * cv2.arcLength(contour, True)
            #print(benchmark_area)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            #print(np.array(approx[0]))
            #cv2.drawContours(image, [approx], -1, (0, 255, 0), 2) if db.show_plot else None
            if len(approx) == 4 and ((cv2.contourArea(contour) > benchmark_area-(benchmark_area*0.3)  and cv2.contourArea(contour) < benchmark_area*100)) :

                #cv2.drawContours(image, [approx], -1, (0, 255, 0), 2) if db.show_plot else None    
                #print('stnd',(image.shape[0]*image.shape[1])/300)
                # Check if the contour has 4 vertices (a quadrilateral)
                x, y, w, h = cv2.boundingRect(approx)
                ok = good_angles(np.array(approx).reshape(4,2),60)
                
                if not ok:
                    continue
                
                # Calculate width-to-height ratio
                if h != 0:  # Avoid division by zero
                    ratio = w / h
                    if (ratio >= 0.7 and ratio <= 1.3) or (cv2.contourArea(contour) > benchmark_area*10):
                        not_inside = True
                        for rect in rectangles:
                            x_center = x + w / 2
                            y_center = y + h / 2
                            rectx_center = rect[0] + rect[2]/2
                            recty_center = rect[1] + rect[3]/2
                            if distance((rectx_center,recty_center),(x_center,y_center)) < 10:
                                not_inside=False
                                continue
                        if not_inside:
                            rectangles.append((x,y,w,h))
                            count += 1

                            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2) if db.show_plot else None
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


def get_choices_by_num(BubbleGetter_obj, BoxGetter_obj, CaptureSheet_obj, box_index, **kwargs):
    db.funcname = 'get_choices_by_num'
    db.color = [200,150,0]
    db.p('Start',bold=True)
    get_result_img = CaptureSheet_obj.get_result_img
    show_plots = CaptureSheet_obj.show_plots and get_result_img


    def get_type_test(bubbles_rowed,return_word=True, debug=False):
        def process(bubbles_rowed, return_word):
            print(bubbles_rowed.shape)
            first_row = np.array(bubbles_rowed[0])
            db.p('first row {}'.format(first_row))
            ground_columns = len(first_row)
            db.p(f'Number of columns raw {ground_columns} {first_row.shape}')
            #print('columns',ground_columns)
            if ground_columns == 2:
                return 1 if return_word==False else 'TRUE OR FALSE'
            if ground_columns%4==2:
                return 1 if return_word==False else 'TRUE OR FALSE'
            if ground_columns > 4:
                comparison = abs(first_row[0][0]-first_row[1][0])/abs(first_row[1][0]-first_row[2][0])
                print(comparison)
                if comparison < 1.8:
                    return 0 if return_word==False else 'MULTIPLE CHOICE'
                else:
                    return 1 if return_word==False else 'TRUE OR FALSE'
        result = process(bubbles_rowed, return_word)
        
        if debug:
            print("Type of Test:", result)
        return result
    
    try:
        rows = np.array(
            get_rows(BubbleGetter_obj.rectangles))
        image = BoxGetter_obj.crops[box_index]
        if True:
            for row in rows:
                x,y,w,h = row[0]
                cv2.rectangle(image, (x, y), (x + w, y + h), (255,0,0), 5)
        
        #
        db.plot(image, 'rows')
        #
        db.p('Rerieved by row; acquiring test type')
        db.p(len(rows[0]))
        db.p(len(rows[1]))
        if len(rows[0]) == 1:
            rows = rows[1:]
        test_type_str = get_type_test(rows)

        #
        db.p(f'Test Type: {test_type_str}')

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

def get_rows(true_rectangles):
    """
    Divides bubbles into by row.
    """
    try:
        true_rectangles = true_rectangles[::-1] 
        
        max_rows = 25
        #multiplier = max_rows/rows
        # convert to np array
        true_rectangles = np.array(true_rectangles)
        #preview
        # get x and y for each rectangle
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
    except Exception as e:
        print('omr.get_rows: ',e)

def scale_coordinates(point, original_width, new_width):
    """
    Scale coordinates from original width to new width.
    """
    original_x, original_y = point
    scale_factor = new_width / original_width
    new_x = int(original_x * scale_factor)
    new_y = int(original_y * scale_factor)
    return new_x, new_y

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
        #image = resize_image_to_max_side(image, int(1280/scaler))
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
        #max_rect = np.array(max_rect)*scaler
        #max_rect = max_rect.astype(int)
        #max_rect=  reorder_points(max_rect)
        CaptureSheet_obj.boxes.rectangles = [max_rect]
        #
        op_seq = operate_orient(max_rect)
        print(op_seq)
        db.p('transforming image perspective', fclr)
        transform = perspective_transform(CaptureSheet_obj.orig_img, max_rect, (get_output_size(max_rect)))
        db.p('Applying transformation')
        for operation in op_seq:
            transform = operation(transform)
        
        transform = resize_image_to_max_side(transform, 1280)
        BoxGetter_obj.crops.append(transform)
        #transform = resize_image_to_max_side(image, 1280)
        #
        db.plot(transform, 'crop+perspective transformed')
        db.p('Done',bold=True)
    except Exception as e:
        db.p(e, rgb=[255,0,0])
        pass




