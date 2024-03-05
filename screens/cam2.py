from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Line
from kivy.uix.image import Image
import numpy as np
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import utilities.omr_eval.capture as capture
import cv2
#import screens.get_cam_params as cam_params
from PIL import Image as Pimage
import io
class CameraWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        
        # Create a camera widget
        #highest_resolution = cam_params.get_highest_resolution()
        #print(highest_resolution)
        self.camera = Camera(play=True, resolution=(1080,1920), opacity=100, size_hint=(1,1))

        # Bind the on_tex event to the update_frame method
        #self.camera.bind(texture=self.update_frame)

        # Add camera widget to layout
        self.add_widget(self.camera)

        # Create lines for the initial bounding box
        self.bounding_box = Line(points=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], width=2)

        # Add bounding box to layout canvas
        #self.canvas.add(self.bounding_box)

        # Create a button to extract camera frame
        self.extract_button = Button(text='Extract Frame', size_hint=(None, None), size=(150, 50), pos=(20, 20))
        self.extract_button.bind(on_press=self.extract_frame)
        self.add_widget(self.extract_button)

    def process_frame(self, frame_data):
        try:
            
            ground_mc = capture.TestType.MultipleChoice(100)
            ground_tf = capture.TestType.MultipleChoice(10)
            rect, crop = capture.get_box(frame_data)
            for x, y, w, h in rect:
                
                cv2.rectangle(frame_data, (x, y), (x + w, y + h), (0, 0, 255), 3)
            frame_data = cv2.flip(frame_data, 0)
            frame_data = cv2.flip(frame_data, 1)
            print(capture.get_bubbles(rect, crop,ground_mc,ground_tf))
            
        except Exception as e:
            print(e)
   

    def show_frame(self, frame_data):
        frame_texture = Texture.create(size=(frame_data.shape[1], frame_data.shape[0]), colorfmt='rgba')
        frame_texture.blit_buffer(frame_data.tobytes(), colorfmt='rgba', bufferfmt='ubyte')

        # Update the image widget with the extracted frame
        self.frame_image.texture = frame_texture


    def extract_frame(self, instance):
        #camera_texture = self.camera.texture
        texture = self.camera.texture
        size=texture.size
        pixels = texture.pixels
        if texture:
            # Extract frame as a NumPy array
            #frame_data = np.frombuffer(camera_texture.pixels, dtype=np.uint8).reshape((self.camera.resolution[1], self.camera.resolution[0], 4))
            #print("Frame extracted as array:", frame_data)
            texture = self.camera.texture
            size=texture.size
            pixels = texture.pixels
            pil_image=Pimage.frombytes(mode='RGBA', size=size,data=pixels)
            numpypicture=np.array(pil_image)

            # Convert the NumPy array into a texture
            #print("CONTENT",image_np)
            self.process_frame(numpypicture)
            
        else:
            print("Camera texture not available.")
