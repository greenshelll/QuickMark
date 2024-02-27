from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Line
from kivy.uix.image import Image
import numpy as np
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from utilities.omr_eval.capture import get_box
import cv2
from PIL import Image as Pimage
import io
class CameraWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        
        # Create a camera widget
        self.camera = Camera(play=True, resolution=(2340, 4160), opacity=0, size_hint=(1,1))

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
        self.frame_image = Image(size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.frame_image)

    def start_timer(self):
        # Schedule the timer function
        Clock.schedule_once(self.update_timer, 1/30)
        
    def update_timer(self, dt):
        self.extract_frame(None)
        self.start_timer()

    def process_frame(self, frame_data):
        rect = get_box(frame_data)
        for x, y, w, h in rect:
            cv2.rectangle(frame_data, (x, y), (x + w, y + h), (0, 0, 255), 3)
        frame_data = cv2.flip(frame_data, 0)
        frame_data = cv2.flip(frame_data, 1)
        self.show_frame(frame_data)

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
