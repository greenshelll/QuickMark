import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import glob
import tensorflow as tf
from tensorflow import lite
#from tensorflow.keras.models import load_model

interpreter = tf.lite.Interpreter(model_path=r"assets\best_model.tflite")
interpreter.allocate_tensors()

#images = [cv.imread(file) for file in glob.glob("test\*.jpg")]

def handwrite_predict(images):
    """_summary_

    Args:
        images (array): an opencv image grayscaled

    Returns:
        string: predicted character
    """
    dict_word = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}
    for i in range(len(images)):
        #gray = cv.cvtColor(images[i], cv.COLOR_BGR2GRAY)
        gray = images[i]
        cv2 = cv
        cropped_image = gray
        
        gray = 255 - cv2.adaptiveThreshold(cropped_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, cropped_image.shape[0] - 1 - cropped_image.shape[0]%2, 2)
        #ret, gray = cv.threshold(gray, 75, 180, cv.THRESH_BINARY)
        #gray = cv2.erode(gray, (27,27), iterations=5)
        gray = cv.resize(gray, (28, 28)) 
        plt.imshow(gray)
        plt.show()

        gray = np.reshape(gray, (1, 28, 28, 1)).astype(np.float32)

        input_details = interpreter.get_input_details()
        interpreter.set_tensor(input_details[0]['index'], gray)

        interpreter.invoke()

        output_details = interpreter.get_output_details()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        predicted_class = dict_word[np.argmax(output_data)]
    print(output_data)
    return predicted_class
