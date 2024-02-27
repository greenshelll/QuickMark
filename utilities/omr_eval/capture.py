try:
    import boxer
except ModuleNotFoundError as e:
    print(e, 'Getting alt path')
    import utilities.omr_eval.boxer as boxer
try:
    import omr
except ModuleNotFoundError as e:
    print(e, 'Getting alt path')
    import utilities.omr_eval.omr as omr
import math
import cv2
omr.run_debug = False
boxer.run_debug = False
class TestType:
    class MultipleChoice:
        def __init__(self, items):
            self.name = 'MULTIPLE CHOICE'
            self.num_items = items
            self.circles_per_num = 4
    class TrueOrFalse:
        def __init__(self, items):
            self.name ='TRUE OR FALSE'
            self.num_items = items
            self.circles_per_num = 2

def get_scores(target_img, ground_mc, ground_tf, target_ispath = True, return_result_image = False):
    
    # Gets boxes in image
    rectangles, _, cropped_result, orig_image = boxer.get_boxes(target_img, 1,target_ispath)

    #omr.show_img(image_result)
    # gets first cropped image (largest box detected)
    cropped_result = cropped_result[0]

    # gets ALL bubble choices
    circles, circle_image_result, orig_image = omr.get_choices(cropped_result, False)
    #omr.show_img(circle_image_result)

    # detects all rows
    circles_by_row = omr.get_rows(circles)
    #print(circles_by_row)

    # get type of test
    test_type_inference = omr.get_type_test(circles_by_row,True,False)
    if test_type_inference == 'MULTIPLE CHOICE':
        # set object info to mc
        test_type_inference = ground_mc
    if test_type_inference == 'TRUE OR FALSE':
        # set object info to tf
        test_type_inference = ground_tf

    # check validity; ensure all bubbles are included
    if test_type_inference.num_items*test_type_inference.circles_per_num == len(circles):
        # if complete, get number for each group of bubble (ex. by 4 for MC, by 2 for TF)
        result_complete = omr.get_by_num(test_type_inference.circles_per_num, circles_by_row)
        # -------------------(IF....) for debugging purposes only; verify each num
        if return_result_image:
            for num in range(1,test_type_inference.num_items+1):
                content = result_complete[num]
                for circles in content:
                    x, y, w, h = circles.xywh
                    cv2.rectangle(orig_image, (x, y), (x + w, y + h), (255,255,0), 5)
                omr.show_img(orig_image)
            return orig_image
        # -------------------(ENDIF)
        return result_complete
    else:
        return None

def get_box(target_img):
    result = boxer.get_boxes(target_img, 1 , False)
    rectangles, img, cropped_result, orig_image = result
    return rectangles

#get_box(r"C:\Users\USER\Downloads\samples\IMG_20240225_084903.jpg")