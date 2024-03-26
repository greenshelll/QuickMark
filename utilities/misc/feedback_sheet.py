from utilities.omr_eval.capture_sheet import CaptureSheet
import os
import cv2
import numpy as np
try:
    #import dill as pickle
    import pickle
except Exception as e:
    import pickle
import random
# Directory containing PNG files
class Circle:
    def __init__(self, *args):
        self.xywh = args

class FeedBackChoices:

    def __init__(self):
        self.mc = []
        self.mc_img_paths = []
        #self.mc_choices_by_num = []
        self.tf = []
        self.tf_img_paths = []
        #self.tf_choices_by_num = []
    def get_mc_by_count(self, count):
        return self.mc[count-1]
    def get_tf_by_count(self, count):
        return self.tf[count-1]
    
def write_presaved_feedback(data):
    # Writing to a pickle file
    with open('assets/feedback.pkl', 'wb') as f:
        pickle.dump(data, f)

def read_presaved_feedback():
    # Reading from a pickle file
    with open('assets/feedback.pkl', 'rb') as f:
        data = pickle.load(f)
    return data


def PRESAVE_FEEDBACK(start,finish,test_type,fbc_obj=None):
    """_summary_

    Args:
        start (_type_): _description_
        finish (_type_): _description_
        test_type (string): mc or tf
    """
    errors = 0
    fbc = FeedBackChoices() if fbc_obj is None else fbc_obj
    for count in range(start,finish+1):

        #print("presave iteration ",count)

        filepath = f'assets/{test_type}_img/{count}.png'
        
        cs=CaptureSheet(count,count,count,filepath, 1,on_android=False,show_plots=True)
        cs.get_boxes()
        
        cs.get_bubbles(redo=True, mod_value=3, for_feedback=True)
        image = cs.boxes.crops[0]
        
        cv2.imwrite(f'assets/feedback/{test_type}_img/{count}.png',image)
        cs.get_choices()
        if cs.bubbles[0].test_type !='MULTIPLE CHOICE':
            errors += 1
        choices_by_num = cs.bubbles[0].choices_by_num_dict

        if test_type == 'mc':
            fbc.mc_img_paths.append(f'assets/feedback/{test_type}_img/{count}.png')
            fbc.mc.append(choices_by_num)
        elif test_type == 'tf':
            fbc.tf_img_paths.append(f'assets/feedback/{test_type}_img/{count}.png')
            fbc.tf.append(choices_by_num)
        #num_dict = {}
        #result = []
        #for index in range(1,count+1):
        #for choices in choices_by_num[index]:
            
            #choice = choices_by_num[index]
            ##print(choices_by_num)
            #
            #for bubble_pos in range(4 if test_type == 'mc' else 2):
           #     result.append(Circle(*choice[bubble_pos].xywh))
          #  num_dict[index] = result
         #   result=[]
        #cs.bubbles[0].choices_by_num = num_dict
        
    return fbc,errors



    
def feedback(answer_array, correct_array, test_type, item_count, save_filepath='img.png',for_preservation=False):
    folder_ref = {'TRUE OR FALSE': 'tf_img',
              'MULTIPLE CHOICE': 'mc_img',
              'IDENTIFICATION': 'idtf_img'}
    file_ref = f'{item_count}.png'
    multiplier_ref = {'TRUE OR FALSE': 2,
                      'MULTIPLE CHOICE':4,
                      'IDENTIFICATION': 1}
    overall_ref = f'assets/{folder_ref[test_type]}/{file_ref}'
    cs = CaptureSheet(item_count,item_count,item_count,overall_ref,1,on_android=False,show_plots=True)
    cs.get_boxes()
    
    #cs.get_bubbles()
    
    cs.get_bubbles(redo=True,mod_value=15)
    image = cs.boxes.crops[0]
    for x in cs.bubbles[0].rectangles:
        x,y,w,h = x
        x2, y2 = x + w, y + h
        #cv2.rectangle(image, (x, y), (x2, y2), [50,200,200], cv2.FILLED)
    cv2.imwrite('img.png',image)
    cs.get_choices()
    choices_by_num = cs.bubbles[0].choices_by_num
    if for_preservation:
        fbc = FeedBackChoices()
        if test_type == 'MULTIPLE CHOICE':
            fbc.mc_img_paths.append(f'assets/feedback/{test_type}_img/{item_count}.png')
            fbc.mc.append(choices_by_num)
        elif test_type == 'TRUE OR FALSE':
            fbc.tf_img_paths.append(f'assets/feedback/{test_type}_img/{item_count}.png')
            fbc.tf.append(choices_by_num)
        #print(fbc.mc)

    
    image =  np.repeat(image[:, :, np.newaxis], 3, axis=2)
    index_char = [
        ['A','T'],
        ['B', 'F'],
        ['C'],
        ['D']
    ]
    #print("COLORING PAPERS")
    #print(answer_array)
    #print(correct_array)
    #print(answer_array)
    
    for answer, correct, index in zip(answer_array, correct_array, range(1,len(answer_array)+1)):
        #for choices in choices_by_num[index]:
        
        choice = choices_by_num[index]
        ##print(choices_by_num)
        
        for bubble_pos in range(multiplier_ref[test_type]):
            x,y,w,h = choice[bubble_pos]
            x2, y2 = x + w, y + h
            
            #print("GETTING ")
            #print(bubble_pos)
            #print(answer)
            #print(index_char)
            #print(correct_array)
            ##print(answer, index_char[bubble_pos], correct_array[bubble_pos])
            for correct_list in correct: # correct single is a bubbble # caorrect can have cor
                if  correct_list in index_char[bubble_pos]: # yellow, listed as correct list
                    ##print(correct_list)
                    cv2.rectangle(image, (x, y), (x2, y2), [0,150,150], 5)

            if answer in index_char[bubble_pos]:
                #print(True)
                cv2.rectangle(image, (x, y), (x2, y2), [00,00,00], cv2.FILLED)
                if answer in correct:
        
                    cv2.rectangle(image, (x, y), (x2, y2), [00,200,00], 5)
                else:
                    #print(False)
                    cv2.rectangle(image, (x, y), (x2, y2), [00,000,200],5)
            # mark possible correct yellow
            
                # green = correct answer
                
    

    cv2.imwrite(save_filepath,image)
 

def feedback_quick(answer_array, correct_array, test_type, item_count, save_filepath='img.png',fbc=None,for_preservation=False):
    folder_ref = {'TRUE OR FALSE': 'tf_img',
              'MULTIPLE CHOICE': 'mc_img',
              'IDENTIFICATION': 'idtf_img'}
    file_ref = f'{item_count}.png'
    multiplier_ref = {'TRUE OR FALSE': 2,
                      'MULTIPLE CHOICE':4,
                      'IDENTIFICATION': 1}
    overall_ref = f'assets/{folder_ref[test_type]}/{file_ref}'
    #print("LOADING PRESAVED")
    fbc = read_presaved_feedback() if fbc is None else fbc
    #print("LOADING PRESAVED DONE")
    
    index_char = [
        ['A','T'],
        ['B', 'F'],
        ['C'],
        ['D']
    ]
    image = cv2.imread(f'assets/feedback/{folder_ref[test_type]}/{file_ref}')
    #image =  np.repeat(image[:, :, np.newaxis], 3, axis=2)
    
    #print("COLORING PAPERS")
    content = fbc.mc if test_type=='MULTIPLE CHOICE' else fbc.tf
    choices_by_num = content[item_count-1]
    #print((choices_by_num))
    0
    for answer, correct, index in zip(answer_array, correct_array, range(1,len(answer_array)+1)):
        #for choices in choices_by_num[index]:
        
        choice = choices_by_num[index]
        ##print(choices_by_num)
        
        for bubble_pos in range(multiplier_ref[test_type]):
            x,y,w,h = choice[bubble_pos]
            ##print(x,y,w,h)
            x2, y2 = x + w, y + h
            ##print(answer, index_char[bubble_pos], correct_array[bubble_pos])
            for correct_list in correct: # correct single is a bubbble # caorrect can have cor
                if  correct_list in index_char[bubble_pos]: # yellow, listed as correct list
                    ##print(correct_list)
                    cv2.rectangle(image, (x, y), (x2, y2), [0,150,150], 5)

            if answer in index_char[bubble_pos]:
                ##print(True)
                cv2.rectangle(image, (x, y), (x2, y2), [00,00,00], cv2.FILLED)
                if answer in correct:
        
                    cv2.rectangle(image, (x, y), (x2, y2), [00,200,00], 5)
                else:
                    ##print(False)
                    cv2.rectangle(image, (x, y), (x2, y2), [00,000,200],5)
            # mark possible correct yellow
        
            
                # green = correct answer
    # Specify the border size

    padding_size = 15

    # Define the border size
    border_size = 15

    # Define the color for the border (e.g., black)
    border_color = (0, 0, 0)  # Black color in BGR format

    # Add a border to the image by painting over the pixels
    image_with_border = np.copy(image)
    image_with_border[:border_size, :, :] = border_color  # Top border
    image_with_border[-border_size:, :, :] = border_color  # Bottom border
    image_with_border[:, :border_size, :] = border_color  # Left border
    image_with_border[:, -border_size:, :] = border_color  # Right border

    # Pad the image with black color
    image = np.pad(image_with_border, ((padding_size, padding_size), (padding_size, padding_size), (0, 0)), mode='constant', constant_values=255)

    cv2.imwrite(save_filepath,image)

    return True

        
    #print("DONE FEEDBACK GENERATION")
 