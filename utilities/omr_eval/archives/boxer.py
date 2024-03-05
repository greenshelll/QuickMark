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
        #image = cv2.equalizeHist(CaptureSheet_obj.bw_orig_img)
        debug('[get_boxes] initializing')
        if get_result_img:
            result_img = CaptureSheet_obj.bw_orig_img.copy()
        
        debug('[get_boxes] gettting copy of original image')
        #print("FINISHED READING")
        # Apply adaptive thresholding
        debug('[get_boxes] applying adaptive thresh')
        adaptive_thresh = cv2.adaptiveThreshold(CaptureSheet_obj.bw_orig_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

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
        debug('[get_boxes] filtering contours')
        # Filter contours based on area
        if get_result_img:
            clone_img = result_img.copy()
        rectangles = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if cv2.contourArea(cnt) > 100:
                rectangles.append((x, y, w, h))
                if get_result_img:
                    # reserve result_img for last (N boxes)
                    cv2.rectangle(clone_img, (x, y), (x + w, y + h), (255, 0, 0), 10)
                
        if show_plots:
            omr.show_img(clone_img, 'All Contours')

        
        # Sort rectangles based on area
        debug('[get_boxes] sorting rectangles based on area size')
        rectangles.sort(key=lambda rect: rect[2] * rect[3])

        # Keep the largest rectangles
        debug('[get_boxes] gets last larges rectangles')
        final_rectangles = rectangles[-boxes_num:]

        # Crop the rectangles
        debug('[get_boxes] cropping rectangles')
        print(final_rectangles)
        crops = [CaptureSheet_obj.orig_img[y:y+h, x:x+w] for x, y, w, h in final_rectangles]

        # Draw rectangles on the original image
        if get_result_img:
            debug('[get_boxes] showing final boxes')
            for x, y, w, h in final_rectangles:
                cv2.rectangle(result_img, (x, y), (x + w, y + h), (255, 0, 0), 10)
        if show_plots:
            omr.show_img(result_img, 'Box Result for {} box/s'.format(boxes_num))
        debug('[get_boxes] end')
        #cv2.imwrite('hello.png', image)
        BoxGetter_obj.result_img = result_img if get_result_img else None
        BoxGetter_obj.crops = crops
        BoxGetter_obj.rectangles = final_rectangles
        #return (final_rectangles, image, crops, orig_img)
    except Exception as e:
        print('get_boxes//',e)
        pass
    
    #omr.show_img(orig_img)
    


