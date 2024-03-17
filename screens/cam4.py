from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Line
from kivy.uix.image import Image
import numpy as np
from kivy.core.camera import CameraBase
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import utilities.omr_eval.capture_sheet as sheet
CaptureSheet = sheet.CaptureSheet
from utilities.omr_eval.omr_functions import Debugger
import cv2
#import screens.get_cam_params as cam_params
from PIL import Image as Pimage
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
db = Debugger()
db.run_debug = False
sheet.omr_functions.db.run_debug=False

db.start_time()

################ ANDROID INIITIALIZATION
class AndroidPlat:
    def __init__(self):
        self.running_on_android = False
    def init_jnius(self):
        try:
            from jnius import autoclass
            self.autoclass = autoclass
            self.python_activity = self.autoclass('org.kivy.android.PythonActivity')
            self.context = self.autoclass('android.content.Context')
            self.activity = self.python_activity.mActivity
            self.vibrator = self.activity.getSystemService(self.context.VIBRATOR_SERVICE)
            self.running_on_android = True
        except Exception as e:
            db.p('NOT RUNNING ON ANDROID. ANDROID ACTIVITIES ARE SKIPPED.',[255,0,0],force_show=True)
            
            

    def vibrate(self,pattern):
        if self.running_on_android:
            self.vibrator.vibrate(pattern)
            
AP = AndroidPlat()
AP.init_jnius()
##############

#################

# We need a reference to the Java activity running the current
# application, this reference is stored automatically by
# Kivy's PythonActivity bootstrap:



class CameraWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        
        # Create a camera widget
        #highest_resolution = cam_params.get_highest_resolution()
        #print(highest_resolution)
        self.camera = Camera(play=True, resolution=(1280,720), opacity=0, size_hint=(1,1))
        #self.camera.play = True
        #self.camera_is_on = False
        #self.camera.loaded
        # Bind the on_tex event to the update_frame method
        #self.camera.bind(texture=self.update_frame)
        self.cs_points = []
        self.cs_objs = []
        # Add camera widget to layout
        self.dummy_counter = 0
        #self.add_widget(self.camera)

        # Create lines for the initial bounding box
        self.bounding_box = Line(points=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], width=2)
        self.label = Label(color=(1, 0, 0, 1))
        self.label.text = 'Eugene'
        # Add bounding box to layout canvas
        #self.canvas.add(self.bounding_box)

        # Create a button to extract camera frame
        self.extract_button = Button(text='Extract Frame', size_hint=(None, None), size=(150, 50), pos=(20, 20))
        self.extract_button.bind(on_press=self.get_choices)
        #self.add_widget(self.extract_button)
        self.start_timer()
        self.timer_value = 0
        # Create an image widget to display the extracted frame
        self.frame_image = Image(size_hint=(1,1), pos_hint={'center_x': 0.5, 'center_y': 0.5},allow_stretch=True, keep_ratio=False)
        self.add_widget(self.frame_image)
        self.add_widget(self.label)
        self.remove_camera = False
        self.orientation = 'vertical'
        self.size_hint = (1,1)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.3}
        

    def start_timer(self):
        # Schedule the timer function
        Clock.schedule_once(self.update_timer, 0.01)
    
    def eucdist(self,x1y1,x2y2):
        x1,y1 = x1y1
        x2,y2 = x2y2
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance
    
    def compute_distances(self,coordinates):
        """
        Compute the distances between consecutive points in a list of coordinates.
        
        Args:
        - coordinates (list of tuples): List of (x, y) coordinates.
        
        Returns:
        - distances (list of floats): List of distances between consecutive points.
        """
        distances = []
        for i in range(len(coordinates) - 1):
            # Extract coordinates of consecutive points
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[i + 1]
            
            # Compute Euclidean distance
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            distances.append(distance)
        
        return distances
    
    def update_timer(self, dt):
        self.extract_frame(None)
        if self.remove_camera == False:
            self.start_timer()
    
    def get_quad_angles(self, points):
        """
        Compute the angles of a quadrilateral given its four points.
        
        Args:
        - points (list of tuples): Four points representing the quadrilateral, each tuple containing (x, y) coordinates.
        
        Returns:
        - angles (list of floats): List of angles (in degrees) of the quadrilateral.
        """
        def compute_angle(p1, p2, p3):
            """Compute the angle between three points."""
            v1 = np.array(p1) - np.array(p2)
            v2 = np.array(p3) - np.array(p2)
            dot_product = np.dot(v1, v2)
            magnitude_v1 = np.linalg.norm(v1)
            magnitude_v2 = np.linalg.norm(v2)
            angle_rad = np.arccos(dot_product / (magnitude_v1 * magnitude_v2))
            angle_deg = np.degrees(angle_rad)
            return angle_deg
        
        # Compute angles between consecutive points
        angles = []
        for i in range(len(points)):
            angle = compute_angle(points[i], points[(i+1)%len(points)], points[(i+2)%len(points)])
            angles.append(angle)
        
        return np.array(angles)
    
    def good_angles(self, points, threshold = 80):
        """
        This Python function checks if a set of points forms a quadrilateral with no angles less than or
        equal to 60 degrees.
        
        :param points: It seems like the code snippet you provided is a method called `angles_are_good`
        that takes in a list of points as input. The method calculates the angles of the quadrilateral
        formed by the points and checks if there is any angle less than or equal to 60 degrees. If there
        is at
        :return: If the `has_small_angle` variable is `True`, then `False` is being returned. Otherwise,
        `True` is being returned.
        """
        angles = self.get_quad_angles(points)
        # gets boolean with less than 60 degrees angle
        has_small_angle = sum(angles <= threshold) > 0
        if has_small_angle:
            return False
        else:
            return True
    
    def process_frame(self, frame_data):
        
        
        db.funcname = 'process_frame'
        db.color = [100,10,10]
        db.p('start',bold=True)
        try:
            #raise Exception
            
            if frame_data is None:
                return None
            self.cs = CaptureSheet(100, 25,10,frame_data,1,False,False)
            
            self.cs.get_boxes()
            
            #__________________________________________________________
            if self.cs.boxes.rectangles is not None:

                npbox = np.array(self.cs.boxes.rectangles)
                if npbox.size==1:
                    cv2.drawContours(frame_data, [], -1, (0, 255, 0), 3)
                    self.show_frame(frame_data)
                    return None
                else:
                    npbox = npbox.reshape(4, 2)

                for rect in self.cs.boxes.rectangles:
                    # Get the coordinates of the rectangle
                    x, y, w, h = cv2.boundingRect(rect)

                    # Draw the text on the image
                if not self.good_angles(npbox,85): # display threshold
                    # get bounding box
                    db.p('Not correct enough')
                    
                    if not self.good_angles(npbox, 45):
                        #cv2.rectangle(frame_data, (x, y), (x + w, y + h), (175,0,175), 3)
                        cv2.drawContours(frame_data, [], -1, (0, 255, 0), 3)
                        self.show_frame(frame_data)
                        return None
                    else:
                        # Draw the text on the blank image
                        #cv2.putText(frame_data, text, (10,10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,150), 2
                        cv2.rectangle(frame_data, (x, y), (x + w, y + h), (255,0,175), 3)
                    #__________________________________________________
                else:
                    db.p('drawing contours')
                    cv2.drawContours(frame_data, self.cs.boxes.rectangles, -1, (0, 255, 0), 4)
                    #cv2.rectangle(frame_data, (x, y), (x + w, y + h), (0,255,0), 3)
                    #self.label.text = 'Attempting Extraction'
                    #self.cs.get_bubbles()
                    #self.cs.get_choices()
                    #self.cs.get_scores()
                    db.p('getting boxes')
                    #score = obj.bubbles[0].final_score
                    #test_type = obj.bubbles[0].test_type
                    #self.label.text = str(counting)
                    #self.label.text = '\n'.join([str(counting), 'SCORE:'+str(score),'TYPE:'+str(test_type)])
                    #_________________________________________
                    self.cs_points.append((x,y))
                    if len(self.cs_points) > 1:
                        previous_cs_point = self.cs_points[-2]
                        if self.eucdist(previous_cs_point, (x,y)) < 40:
                            self.cs_objs.append(self.cs)
                            if len(self.cs_points) == 5:
                                print("EVALUATING")
                                counts = []
                                done=False
                                for obj in self.cs_objs:
                                    print("GETTTING BUBBBLES")
                                    obj.get_bubbles()
                                    print("DONE GETTING BUBBLES")
                                    counting = obj.bubbles[0].count
                                    print('DONE GETTING BUBBLES',counting)
                                    nums = [obj.mcq.num_items*4, obj.tfq.num_items*2, obj.idq.num_items, 45*4, 30*2, 5]
                                    if counting not in nums:
                                        obj.get_bubbles(redo=True)
                                        counting = obj.bubbles[0].count
                                    if counting in nums:
                                        #if counting in [100*4, 10*2, 10*1, 45*4, 30*2, 1*5]:
                                        #vibrator.vibrate(100)
                                         # the argument is in milliseconds
    
                                        obj.get_choices()
                                        obj.get_scores()
                                        AP.vibrate(50)
                                        score = obj.bubbles[0].final_score
                                        test_type = obj.bubbles[0].test_type
                                        self.label.text = str(counting)
                                        self.label.text = '\n'.join([str(counting), 'SCORE:'+str(score),'TYPE:'+str(test_type)])
                                        self.cs_points = []
                                        self.cs_objs = []
                                        
                                        
                                        done=True
                                        break

                                    counts.append(counting)
                                print("COUNTING ALL",counts)
                                if done == False:
                                    #if num in [100*4, 10*2, 10*1, 45*4, 30*2, 1*5]:
                                    self.label.text = str(max(counts))
                                    #vibrator.vibrate(100)
                                    #AP.vibrate(50)  # the argument is in milliseconds
                                    self.cs_points = []
                                    self.cs_objs = []
                                    print(max(counts))
                                    
                                done=False
                            else:
                                pass
                        else:
                            self.cs_points = []
                            self.cs_objs = []

                    """self.cs.get_bubbles()
                    self.label.text = str(self.cs.bubbles[0].count)"""
                    #___________________________________________________
        except AttributeError as e:
            print(db.p('ERRROR'+str(e),rgb=[255,0,0],force_show=True))
        self.show_frame(frame_data)
    
        
    def show_frame(self, frame_data):
        db.funcname = 'show_frame'
        db.color = [50,100,200]

        db.p('start', bold=True)

        # Convert the numpy array to a PIL Image
        pil_image = Pimage.fromarray(frame_data)

        # Rotate the image by 90 degrees clockwise
        rotated_pil_image = pil_image.rotate(90, expand=True)

        # Convert the rotated PIL Image to numpy array
        rotated_frame_data = np.array(rotated_pil_image)
        #rotated_frame_data = np.rot90(frame_data, k=-1)

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

        #
        db.p('done',bold=True)

    def get_choices(self,instance=None):
        self.cs.get_bubbles()
        self.label.text = str(self.cs.bubbles[0].count)
    def extract_frame(self, instance):
        try:
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
                pil_image = Pimage.frombytes(mode='RGBA', size=size,data=pixels)

                numpypicture=np.array(pil_image)
                self.frame_image.texture = texture
                # Convert the NumPy array into a texture
                #print("CONTENT",image_np)
                self.process_frame(numpypicture)
                
            else:
                print("Camera texture not available.")
        except Exception as e:
            print(e)
        
