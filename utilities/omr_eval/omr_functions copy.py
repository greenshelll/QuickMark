import cv2
import numpy as np
try:
    import util4string as u4str
except ModuleNotFoundError as e:
    print(e, 'Getting alt path')
    import utilities.omr_eval.util4string as u4str
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
        
    def p(self,text=None, rgb=None,bold=False,italic=False,dim=False,strike=False,underline=False,ignore_time=False):
        if self.run_debug:
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
    db.p('Start',bold=True)
    try:
        get_result_img = CaptureSheet_obj.get_result_img
        show_plots = CaptureSheet_obj.show_plots and get_result_img
        image = BoxGetter_obj.crops[boxes_num]
        #
        #image = resize_image_to_max_side(image, 320)
        db.p('applying adaptive thresh')
        image = cv2.equalizeHist(image)
        adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # Invert the thresholded image
        #
        db.p('inverting thresh')
        adaptive_thresh = 255 - adaptive_thresh

        db.p('finding contours')
        contours, hierarchy = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
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
            
            if len(approx) == 4 and cv2.contourArea(contour) > benchmark_area-(benchmark_area*0.3) and cv2.contourArea(contour) < benchmark_area*100:
            
                #print('stnd',(image.shape[0]*image.shape[1])/300)
                # Check if the contour has 4 vertices (a quadrilateral)
                x, y, w, h = cv2.boundingRect(approx)
            
                # Calculate width-to-height ratio
                if h != 0:  # Avoid division by zero
                    ratio = w / h
                    if (ratio >= 0.7 and ratio <= 1.3):
                        not_inside = True
                        for rect in rectangles:
                            x_center = x + w / 2
                            y_center = y + h / 2
                            rectx_center = rect[0] + rect[2]/2
                            recty_center = rect[1] + rect[3]/2
                            if distance((rectx_center,recty_center),(x_center,y_center)) < 20:
                                not_inside=False
                                break
                        if not_inside:
                            rectangles.append((x,y,w,h))
                            count += 1
                            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2) if db.show_plot else None
        #
        db.plot(image, 'perspective transformed')
        #db.p('qualified contoures ---',len(rectangles))
        #
        db.p('numbers---'+str(count))
        db.p('done',bold=True)
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
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
    
    return resized_image



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
            result_img = CaptureSheet_obj.orig_img.copy()
        image = CaptureSheet_obj.orig_img
        image = resize_image_to_max_side(image, int(1280/scaler))
        #
        db.p('applying adaptive thresh',fclr)
        
        adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # Invert the thresholded image
        db.p('inverting thresh',fclr)
        adaptive_thresh = 255 - adaptive_thresh

        #
        db.p('finding contours',fclr)
        contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
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

            # Check if the contour has 4 vertices (a quadrilateral)
            if len(approx) == 4:
                if area > max_area:
                    max_area = area
                    max_rect =approx
        max_rect = np.array(max_rect)*scaler
        max_rect = max_rect.astype(int)
        
        CaptureSheet_obj.boxes.rectangles = [max_rect]

        #
        db.p('transforming image perspective', fclr)
        transform = perspective_transform(CaptureSheet_obj.orig_img, max_rect, get_output_size(max_rect))
        transform = cv2.flip(transform, 1)
        transform = resize_image_to_max_side(transform, 1280)
        BoxGetter_obj.crops.append(transform)

        #
        db.plot(transform, 'crop+perspective transformed')
        db.p('Done',bold=True)
    except Exception as e:
        db.p(e, rgb=[255,0,0])
        pass




