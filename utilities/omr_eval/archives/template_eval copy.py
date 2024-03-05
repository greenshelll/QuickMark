import numpy as np
import cv2
import matplotlib.pyplot as plt
def get_rows(true_rectangles):
    """
    Divides bubbles into by row.
    """
    try:
        print("TRUE")
        
        second_column = np.array(true_rectangles)[:, 1]
        print(second_column)
        # Getting unique values from the second column
        unique_values_second_column = np.unique(second_column)
        diff= np.diff(unique_values_second_column)
        print(len(unique_values_second_column)/len(np.unique(diff)))
        print(unique_values_second_column)
        print("UNIEUQ")
        
        print(unique_values_second_column)
        output = []
        for unique_value in unique_values_second_column:
            
            temp_output = []
            for rect in true_rectangles:
                if rect[1] == unique_value:
                    temp_output.append(rect)
    
            output.append(temp_output)
            print(temp_output)
        
        return np.array(output)

    except Exception as e:
        print('omr.get_rows: ',e)


def get_type_test(bubbles_rowed,return_word=True, debug=True):
    try:
        def process(bubbles_rowed, return_word):
            col_ungrouped_length = bubbles_rowed.shape[1]
            arr = bubbles_rowed
            diff = abs(arr[0][1:] - arr[0][:-1])
            comdif = sum([x[0]<=40 for x in diff])
            spaces = col_ungrouped_length - comdif
            final = col_ungrouped_length/spaces
            return None
            a = np.array(bubbles_rowed)
            print(a)
            a = np.array(a)[:,0]
            ground_columns = len(a)
            print(ground_columns)
            print('columns',ground_columns)
            if ground_columns == 2:
                return 1 if return_word==False else 'TRUE OR FALSE'
            if ground_columns%4==2:
                return 1 if return_word==False else 'TRUE OR FALSE'
            if ground_columns > 4:
                comparison = abs(a[1]-a[2])/abs(a[0]-a[1])
                print(comparison)
                if comparison < 1.8:
                    return 0 if return_word==False else 'MULTIPLE CHOICE'
                else:
                    return 1 if return_word==False else 'TRUE OR FALSE'
        result = process(bubbles_rowed, return_word)
        
        if debug:
            print("Type of Test:", result)
        return result
    except Exception as e:
        print(e)


def is_valid(ground_rows, ground_cols, total):
    try:
        if total == ground_rows*ground_cols:
            return True
        else:
            return False
    except Exception as e:
        print(e)

def get_by_num(circles_per_num,bubbles):
    try:
        class Circle:
            def __init__(self, *args):
                self.xywh = args

        result_complete ={}
        result = []
        for i in range(len(bubbles)):
            row = np.array(bubbles)[i]
            # Combine each group of 4 into a rect object
            item_num = 0
            interval = circles_per_num
            print(row)
            for group in row.reshape(-1,circles_per_num):
                result.append(Circle(*group))
                interval-=1
                if interval == 0:
                    interval = 4
                    
                    result_complete[(25*item_num)+i+1] = result
                    item_num += 1
                    result = []
            item_num = 0
        return result_complete
    except Exception as e:
        print(e)

class TemplateEval:
    def __init__(self, boundings):
        self.boundings = boundings
        self.rectangles = []
        self.main_boxes = None
    def plot(self, image, xywh_array, group_iteration=False):
        if group_iteration:
            image = image.copy()
            for rect  in xywh_array:
                
                x,y,w,h = rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color, thickness 2
            self.show(image)
        else:
            image = image.copy()
            x,y,w,h = xywh_array
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color, thickness 2
            self.show(image)

    def show(self,image):
        plt.imshow(image)
        plt.title('Rectangles Detected')
        plt.axis('off')
        plt.show()
    def detect_boxes(self, path):
        # Read the image
        self.image = cv2.imread(path)  # Replace 'your_image.jpg' with the path to your image

        # Convert the image to RGB format (for Matplotlib)
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        # Convert the image to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Find contours
        contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Loop through all contours and filter rectangles
        for contour in contours:
            # Get the bounding rectangle of the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Draw the rectangle on the image
            if w > 20 and h > 20:
                self.rectangles.append((x,y,w,h))
                cv2.rectangle(image_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color, thickness 2
        self.show(image_rgb)
        # Display the image with detected rectangles
    def get_rows(self,bubbles):
        return get_rows(bubbles)
    def get_main_boxes(self):
        self.main_boxes = sorted(self.rectangles, key=lambda x: x[2]*x[3], reverse=True)[1:self.boundings+1]

        print(self.main_boxes)
        #(self.image, self.main_boxes, True)
    def group_main_boxes(self):
        grouped_rectangles = []
        
        for main_box in self.main_boxes:
            # Get main box coordinates
            main_x, main_y, main_w, main_h = main_box
            
            # Group rectangles inside main box
            group = []
            for rectangle in self.rectangles:
                x, y, w, h = rectangle
                if (x > main_x and y > main_y and x + w < main_x + main_w and y + h < main_y + main_h):
                    group.append(rectangle)
                    
            grouped_rectangles.append(group)
            
            # Plot main box and grouped rectangles
            
            #(self.image, group, True)  # Plot grouped rectangles in blue
            self.grouped_rectangles = grouped_rectangles
        print("\nGrouped Rectangles:")
        for i, group in enumerate(grouped_rectangles):
            print(f"Group {i+1}:")
            print(group)

te = TemplateEval(3)
te.detect_boxes(r'C:\Users\USER\Documents\GitHub\archive\2\utilities\sheet\template.png')
te.get_main_boxes()
te.group_main_boxes()
# detects all rows
a = te.get_rows(te.grouped_rectangles[2])
get_type_test(a,True)

#print(circles_by_row)

"""# get type of test
test_type_inference = get_type_test(circles_by_row,True,False)
if test_type_inference == 'MULTIPLE CHOICE':
    # set object info to mc
    test_type_inference = ground_mc
if test_type_inference == 'TRUE OR FALSE':
    # set object info to tf
    test_type_inference = ground_tf

# check validity; ensure all bubbles are included
if test_type_inference.num_items*test_type_inference.circles_per_num == len(circles):
    # if complete, get number for each group of bubble (ex. by 4 for MC, by 2 for TF)
    result_complete = get_by_num(test_type_inference.circles_per_num, circles_by_row)
    # -------------------(IF....) for debugging purposes only; verify each num
    if True:
        for num in range(1,test_type_inference.num_items+1):
            content = result_complete[num]
    # -------------------(ENDIF)
    return result_complete
else:
    return None
"""

"""te = TemplateEval(3)
te.debug = False
te.detect_boxes(r'C:\Users\USER\Documents\GitHub\archive\2\utilities\sheet\template.png')
te.get_main_boxes()
te.group_main_boxes()
te.calculate_relative_coordinates(te.main_boxes[0], te.grouped_rectangles[0])
# detects all rows
a = te.get_rows(te.grouped_rectangles[1])
b = get_type_test(a)
"""
#print(circles_by_row)

"""# get type of test
test_type_inference = get_type_test(circles_by_row,True,False)
if test_type_inference == 'MULTIPLE CHOICE':
    # set object info to mc
    test_type_inference = ground_mc
if test_type_inference == 'TRUE OR FALSE':
    # set object info to tf
    test_type_inference = ground_tf

# check validity; ensure all bubbles are included
if test_type_inference.num_items*test_type_inference.circles_per_num == len(circles):
    # if complete, get number for each group of bubble (ex. by 4 for MC, by 2 for TF)
    result_complete = get_by_num(test_type_inference.circles_per_num, circles_by_row)
    # -------------------(IF....) for debugging purposes only; verify each num
    if True:
        for num in range(1,test_type_inference.num_items+1):
            content = result_complete[num]
    # -------------------(ENDIF)
    return result_complete
else:
    return None
"""