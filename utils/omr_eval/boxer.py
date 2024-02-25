import cv2
import numpy as np
try:
    import helloworld.omr as omr
except Exception:
    import omr
def debug(text):
    print(f"\033[34m{text}\033[0m")

def get_boxes(image, boxes_num, image_is_path=False, get_plot=False, get_np_orig=True): 
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
    # Load an image from file
    debug('[get_boxes] initializing')
    if image_is_path:
        image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

    debug('[get_boxes] gettting copy of original image')
    orig_img = image.copy() if get_np_orig else None
    #print("FINISHED READING")
    # Apply adaptive thresholding
    debug('[get_boxes] applying adaptive thresh')
    adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Invert the thresholded image
    debug('[get_boxes] inverting thresh')
    adaptive_thresh = 255 - adaptive_thresh

    # Apply median blur
    debug('[get_boxes] applying median blur')
    blurred_image = cv2.medianBlur(adaptive_thresh, 9)

    # Find contours
    debug('[get_boxes] finding contours')
    contours, _ = cv2.findContours(blurred_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    debug('[get_boxes] filtering contours')
    # Filter contours based on area
    rectangles = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt) > 100:
            rectangles.append((x, y, w, h))

    
    # Sort rectangles based on area
    debug('[get_boxes] sorting rectangles based on area size')
    rectangles.sort(key=lambda rect: rect[2] * rect[3])

    # Keep the largest rectangles
    debug('[get_boxes] gets last larges rectangles')
    final_rectangles = rectangles[-boxes_num:]

    # Crop the rectangles
    debug('[get_boxes] cropping rectangles')
    crops = [orig_img[y:y+h, x:x+w] for x, y, w, h in final_rectangles]

    # Draw rectangles on the original image
    if get_plot:
        debug('[get_boxes] showing final boxes')
        for x, y, w, h in final_rectangles:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)
        omr.show_img(image)
    debug('[get_boxes] end')
    return (final_rectangles, image, crops, orig_img)


