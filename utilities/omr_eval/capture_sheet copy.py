
import cv2
try:
    import omr_functions as omr_functions
    import util4string as u4str
except ModuleNotFoundError as e:
    print(e, 'Getting alt path')
    import utilities.omr_eval.util4string as u4str
    import utilities.omr_eval.omr_functions as omr_functions
import numpy as np

omr_functions.db.run_debug = True

class _TestType:
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
    class Identification:
        def __init__(self, items):
            self.name = 'IDENTIFICATION'
            self.num_items = items

class _BoxGetter:
    def __init__(self):
        self.rectangles = None
        self.result_img = None
        self.crops = []
        self.bubbles = []
        self.transformed_imgs = []
    
    def retrieve(self, CaptureSheet_obj, boxes_num, **kwargs):
        omr_functions.get_boxes(BoxGetter_obj =self, 
                        CaptureSheet_obj=CaptureSheet_obj, 
                        boxes_num=boxes_num, **kwargs)

class _BubbleGetter:
    crop_i = None
    def __init__(self):
        self.img = None
        self.bubbles = None
        self.result_img = None
        

    def retrieve(self, BoxGetter_obj, CaptureSheet_obj, box_index,**kwargs):
        """omr.get_choices(BubbleGetter_obj=self,
                        BoxGetter_obj=BoxGetter_obj,
                        CaptureSheet_obj=CaptureSheet_obj, 
                        box_index=box_index,
                        **kwargs)"""
        omr_functions.get_bubbles(BubbleGetter_obj=self,
                               CaptureSheet_obj=CaptureSheet_obj, 
                               boxes_num=box_index,
                                BoxGetter_obj=BoxGetter_obj,
                                **kwargs)
        
class CaptureSheet:
    def __init__(self, mcq_items, tfq_items, idq_items, img, boxes_num,get_result_img=False, show_plots=False, ):
        self.get_result_img = get_result_img
        self.show_plots = show_plots
    
        self.boxes_num = boxes_num
        # create questions object
        self.count = 0
        self.mcq = _TestType.MultipleChoice(mcq_items)
        self.tfq = _TestType.TrueOrFalse(tfq_items)
        self.idq = _TestType.Identification(idq_items)

        # process image on instantiation
        self.orig_img = img
        self.bw_orig_img = None
        self._get_img_array()

        # initialization only; to be processed...
        self.boxes = _BoxGetter()
        self.bubbles = [_BubbleGetter() for x in range(boxes_num)]
        # detects all rows

    def _resize_img(self, image, max_side_length):
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
        resized_image = cv2.resize(image, (new_width, new_height))
        
        return resized_image

    def _get_img_array(self):
        # turn to image array if input is a path
        if type(self.orig_img) == str:
            self.orig_img = cv2.imread(self.orig_img, cv2.IMREAD_GRAYSCALE)
            #self.orig_img = self._resize_img(self.orig_img,1280)
            #self.bw_orig_img = self.orig_img.copy()
        elif isinstance(self.orig_img, np.ndarray): # input img is already in image array
            self.orig_img = cv2.cvtColor(self.orig_img, cv2.COLOR_BGR2GRAY)
            #self.bw_orig_img = self.orig_img.copy()
            #self.bw_orig_img = self._resize_img(self.orig_img, 1280)
            
        else:
            raise TypeError('Capture Sheet requires path or numpy array image')
        
    def get_boxes(self, **kwargs):
        self.boxes.retrieve(CaptureSheet_obj=self, 
                            boxes_num=self.boxes_num,**kwargs)
        return self
        
    def get_bubbles(self):
        for crop_i in range(len(self.boxes.crops)):
            self.bubbles[crop_i].retrieve(BoxGetter_obj=self.boxes,
                                          CaptureSheet_obj=self,
                                          box_index=crop_i)
            #self.bubbles[crop_i].img = self.boxes[crop_i].transformed_imgs
        return self
    
    
if __name__ == "__main__":
    #cs = CaptureSheet(100,10,10,r"C:\Users\USER\Downloads\WIN_20240228_07_05_54_Pro.jpg",True,True)
    cs = CaptureSheet(
        mcq_items=100,
        tfq_items=10,
        idq_items=10,
        img=r"C:\Users\USER\Downloads\samples\IMG_20240225_084949.jpg",
        boxes_num=1,
        get_result_img=True,
        show_plots=True
    )
    cs.get_boxes()
    cs.get_bubbles()
    
else:
    pass
