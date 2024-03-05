from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Line
from kivy.uix.image import Image
import numpy as np
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from utilities.omr_eval.capture_sheet import CaptureSheet
import cv2
#import screens.get_cam_params as cam_params
from PIL import Image as Pimage
import io
from PIL import Image as Pimage
class CameraWidget(FloatLayout):
    def __init__(self, **kwargs):
        self.count = 0
        super(CameraWidget, self).__init__(**kwargs)
        
        # Create a camera widget
        #highest_resolution = cam_params.get_highest_resolution()
        #print(highest_resolution)
        self.camera = Camera(play=True, resolution=(1280, 720), opacity=0, size_hint=(1,1))

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
        self.start_timer()
        self.timer_value = 0
        # Create an image widget to display the extracted frame
        self.frame_image = Image(size_hint=(1,1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.frame_image)

    def start_timer(self):
        # Schedule the timer function
        Clock.schedule_once(self.update_timer, 0.01)
        
    def update_timer(self, dt):
        self.extract_frame(None)
        #print(True)
        self.start_timer()
        
    def process_frame(self, frame_data):
        try:
            #raise Exception
            if frame_data is None:
                #print(None)
                return None
            cs = CaptureSheet(100, 10,10,frame_data,1,False,False)
            cs.get_boxes()
            img = cs._resize_img(frame_data, 1280)
            cv2.drawContours(img, cs.boxes.rectangles, -1, (0, 255, 0), 3)
            """frame_data = cv2.flip(frame_data, 0)
            frame_data = cv2.flip(frame_data, 1)"""
            #print('done')
        except Exception as e:
            print(e)
        self.show_frame(img)
        
    def show_frame(self, frame_data):
        # Convert the numpy array to a PIL Image
        """pil_image = Pimage.fromarray(frame_data)

        # Rotate the image by 90 degrees clockwise
        rotated_pil_image = pil_image.rotate(90, expand=True)

        # Convert the rotated PIL Image to numpy array
        rotated_frame_data = np.array(rotated_pil_image)"""
        rotated_frame_data = np.rot90(frame_data, k=-1)

        # Ensure the image is in RGB format
        if rotated_frame_data.shape[2] == 4:  # RGBA
            rotated_frame_data = cv2.cvtColor(rotated_frame_data, cv2.COLOR_RGBA2RGB)
        elif rotated_frame_data.shape[2] == 3:  # RGB
            pass  # No need for conversion
        else:
            raise ValueError("Unexpected number of color channels in frame_data")

        frame_texture = Texture.create(size=(720, 1280), colorfmt='rgb')
        frame_texture.blit_buffer(rotated_frame_data.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

        # Update the Image widget with the rotated frame
        self.frame_image.texture = frame_texture


    def extract_frame(self, instance):
        #camera_texture = self.camera.texture
        texture = self.camera.texture
        
        if texture:
            size=texture.size
            pixels = texture.pixels
            # Extract frame as a NumPy array
            #frame_data = np.frombuffer(camera_texture.pixels, dtype=np.uint8).reshape((self.camera.resolution[1], self.camera.resolution[0], 4))
            #print("Frame extracted as array:", frame_data)
            #texture = self.camera.texture
            #size=texture.size
            #pixels = texture.pixels
            #pil_image = Pimage.frombytes(mode='RGBA', size=size,data=pixels)
            pil_image = np.frombuffer(pixels, dtype=np.uint8).reshape(size[1], size[0], 4)  # Assuming RGBA format


            numpypicture=np.array(pil_image)
            self.frame_image.texture = texture
            # Convert the NumPy array into a texture
            #print("CONTENT",image_np)
            self.process_frame(numpypicture)
            
        else:
            print("Camera texture not available.")
        
