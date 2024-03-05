import cv2
import numpy as np
try:
    import omr
except ModuleNotFoundError as e:
    print(e, 'Getting alt path')
    import utilities.omr_eval.omr as omr
run_debug = True

def debug(text):
    if run_debug:
        print(f"\033[34m{text}\033[0m")


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
    get_result_img = CaptureSheet_obj.get_result_img
    show_plots = CaptureSheet_obj.show_plots and get_result_img
    image = BoxGetter_obj.crops[boxes_num]
    adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Invert the thresholded image
    debug('[get_bubbles] inverting thresh')
    adaptive_thresh = 255 - adaptive_thresh
    debug('get_bubbles: initialized')
    #image = 255-cv2.dilate(255-image,  np.ones((3, 3), np.uint8) , iterations=1)
    contours, hierarchy = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #omr.show_img(adaptive_thresh)
    print("GETING IMAGE")
    print(len(contours))
    cv2.imwrite('sample.png', image)
    rectangles=[]
    # Filter contours based on area
    # Filter quadrilaterals
    debug('get_bubbles: getting contours')
    wh_ratios=  []
    total_area = (image.shape[0]*image.shape[1])
    constant = 1511.9066666
    benchmark_area = total_area/constant
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
                            print("INSIDE")
                            break
                    if not_inside:
                        rectangles.append((x,y,w,h))

                        cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
    #[print(x) for x in wh_ratios]
    omr.show_img(image, 'perspective transformed')

def resize_image_to_max_side(image, max_side_length):
    # Get the dimensions of the image
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
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return resized_image
def sharpen_image(image):
    # Define the sharpening kernel
    sharpening_kernel = np.array([[-1, -1, -1],
                                  [-1,  9, -1],
                                  [-1, -1, -1]])
    
    # Apply the sharpening kernel to the image using filter2D
    sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)
    
    return sharpened_image
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
    try:
        # Load an image from file
        #image = CaptureSheet_obj.bw_orig_img
        get_result_img = CaptureSheet_obj.get_result_img
        show_plots = CaptureSheet_obj.show_plots and get_result_img
        #image = cv2.equalizeHist(image)
        debug('[get_boxes] initializing')
        
        if get_result_img:
            result_img = CaptureSheet_obj.orig_img.copy()
        
        debug('[get_boxes] gettting copy of original image')
        #print("FINISHED READING")
        # Apply adaptive thresholding
        debug('[get_boxes] applying adaptive thresh')
        adaptive_thresh = cv2.adaptiveThreshold(CaptureSheet_obj.orig_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # Invert the thresholded image
        debug('[get_boxes] inverting thresh')
        adaptive_thresh = 255 - adaptive_thresh

        # Apply median blur
        debug('[get_boxes] applying median blur')
        #blurred_image = cv2.medianBlur(adaptive_thresh, 9)

        # Find contours
        debug('[get_boxes] finding contours')
        contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #omr.show_img(adaptive_thresh)
        rectangles=[]
        debug('[get_boxes] filtering contours')
        # Filter contours based on area
        # Filter quadrilaterals
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

            # Check if the contour has 4 vertices (a quadrilateral)
            if len(approx) == 4:
                if area > max_area:
                    max_area = area
                    max_rect =approx

        

        #cv2.drawContours(clone_img, rectangles, -1, (0, 255, 0), 2)
        CaptureSheet_obj.boxes.rectangles = [max_rect]
    
        #omr.show_img(clone_img, "COUNTORS")
        
        # Sort rectangles based on area
        transform = perspective_transform(CaptureSheet_obj.orig_img, max_rect, get_output_size(max_rect))
        transform = cv2.rotate(transform, cv2.ROTATE_90_CLOCKWISE)
        transform = cv2.flip(transform, 1)
        transform = resize_image_to_max_side(transform, 1280)
        
        BoxGetter_obj.crops.append(transform)
        debug("SHOWING TRANSFORMATION")
        if show_plots:
            omr.show_img(transform, 'perspective transformed')
    except Exception as e:
        print('get_boxes//',e)
        pass
    
    #omr.show_img(orig_img)

