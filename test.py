
from utilities.ocr.function import handwrite_predict
import cv2 as cv
from utilities.omr_eval.capture_sheet import CaptureSheet

prediction = handwrite_predict([cv.imread(r'C:\Users\USER\Documents\GitHub\QuickMark\0.png', cv.IMREAD_GRAYSCALE)])
print('prediction',prediction)

if __name__ == "__main__":
    # sample input
    #cs = CaptureSheet(100,10,10,r"C:\Users\USER\Downloads\WIN_20240228_07_05_54_Pro.jpg",True,True)
    cs = CaptureSheet(
        mcq_items=100,
        tfq_items=10,

        idq_items=10,
        img=r"C:\Users\USER\Downloads\IMG_20240311_122156.jpg",
        boxes_num=1,
        get_result_img=True, 
        show_plots=True,
        on_android=False
    )
    cs.get_boxes()
    cs.get_bubbles(True)
    cs.get_choices()
    cs.get_scores()
    print(cs.bubbles[0].count)
    print(cs.bubbles[0].final_score)
else:
    pass