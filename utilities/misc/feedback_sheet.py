from utilities.omr_eval.capture_sheet import CaptureSheet
import os
import cv2
import numpy as np
import random

# Directory containing PNG files

def feedback(answer_array, correct_array, test_type, item_count, save_filepath='img.png'):
    

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
    
    
    image =  np.repeat(image[:, :, np.newaxis], 3, axis=2)
    index_char = [
        ['A','T'],
        ['B', 'F'],
        ['C'],
        ['D']
    ]
    print("COLORING PAPERS")
    print(answer_array)
    print(correct_array)
    print(answer_array)
    for answer, correct, index in zip(answer_array, correct_array, range(1,len(answer_array)+1)):
        #for choices in choices_by_num[index]:
        
        choice = choices_by_num[index]
        #print(choices_by_num)
        
        for bubble_pos in range(multiplier_ref[test_type]):
            x,y,w,h = choice[bubble_pos].xywh
            x2, y2 = x + w, y + h
            
            print("GETTING ")
            print(bubble_pos)
            print(answer)
            print(index_char)
            print(correct_array)
            #print(answer, index_char[bubble_pos], correct_array[bubble_pos])
            for correct_list in correct: # correct single is a bubbble # caorrect can have cor
                if  correct_list in index_char[bubble_pos]: # yellow, listed as correct list
                    #print(correct_list)
                    cv2.rectangle(image, (x, y), (x2, y2), [0,150,150], 5)

            if answer in index_char[bubble_pos]:
                print(True)
                cv2.rectangle(image, (x, y), (x2, y2), [00,00,00], cv2.FILLED)
                if answer in correct:
        
                    cv2.rectangle(image, (x, y), (x2, y2), [00,200,00], 5)
                else:
                    print(False)
                    cv2.rectangle(image, (x, y), (x2, y2), [00,000,200],5)
            # mark possible correct yellow
            
                # green = correct answer
                
    

    cv2.imwrite(save_filepath,image)
 
