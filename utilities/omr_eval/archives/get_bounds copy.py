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
        if CaptureSheet_obj.show_plots:
            omr.show_img(transform, 'perspective transformed')
    except Exception as e:
        print('get_boxes//',e)
        pass
    
    #omr.show_img(orig_img)
    


