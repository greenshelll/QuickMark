import numpy as np
import cv2
import matplotlib.pyplot as plt
def get_rows(true_rectangles):
    """
    Divides bubbles into by row.
    """
    try:
        
        true_rectangles = np.array(true_rectangles[::-1])
        print(true_rectangles)
        max_rows = 25
        #multiplier = max_rows/rows
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


def get_type_test(bubbles_rowed,return_word=True, debug=True):
    try:
        def process(bubbles_rowed, return_word):
            a = np.array(bubbles_rowed)[0]
            a = np.array(a)[:,0]
            ground_columns = len(a)
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
        if result == None:
            return 2 if return_word==False else 'IDENTIFICATION'
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
        self.debug = True
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
    def apply_relative_coordinates(self, relative_xywh, main_xywh, image):
        absolute_xywh = []
        mx, my, mw, mh = main_xywh
        for xywh in relative_xywh:
            x, y, w, h = xywh
            # Calculate absolute coordinates
            abs_x = int(x * mw) + 0
            abs_y = int(y * mh) + 0
            abs_w = int(w * mw)
            abs_h = int(h * mh)
            # Draw rectangle on the image
            cv2.rectangle(image, (abs_x, abs_y), (abs_x + abs_w, abs_y + abs_h), (0, 255, 0), 2)
        return image
    
    def calculate_relative_coordinates(self,main_box, sub_rectangles):
        main_x, main_y, main_w, main_h = main_box
        relative_sub_rectangles = []
        x,y,w,h = main_box
        image = self.image[y:y+h, x:x+w]
        for rectangle in sub_rectangles:
            x, y, w, h = rectangle

            if (x > main_x and y > main_y and x + w < main_x + main_w and y + h < main_y + main_h):
                # Calculate relative coordinates
                relative_x = (x - main_x) / main_w
                relative_y = (y - main_y) / main_h
                relative_w = w / main_w
                relative_h = h / main_h
                # Append relative coordinates along with width and height to the result list
                relative_sub_rectangles.append((relative_x, relative_y, relative_w, relative_h))
                # Draw a circle on the main image to indicate the relative position of the sub-rectangle
        self.relative_sub_rect = relative_sub_rectangles
        image = self.apply_relative_coordinates(relative_sub_rectangles, main_box,image)
        self.show(image)
        return relative_sub_rectangles
    def show(self,image):
        if self.debug == False:
            return None
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
        #self.plot(self.image, self.main_boxes, True)
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
            
            #self.plot(self.image, group, True)  # Plot grouped rectangles in blue
            self.grouped_rectangles = grouped_rectangles
        print("\nGrouped Rectangles:")
        for i, group in enumerate(grouped_rectangles):
            print(f"Group {i+1}:")
            print(group)
    

