import numpy as np
import matplotlib.pyplot as plt
import cv2
plt.style.use({
    'figure.facecolor': 'gray',
    'axes.facecolor': 'gray',
    'axes.edgecolor': 'black',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'text.color': 'white',
})
import math
class Drawer:

    def __init__(self,width,height,mcf,tf,idtf):
        self.mcf_count = mcf
        self.tf_count = tf
        self.idtf_count = idtf
        self.bubble_size = 36
        image = np.ones((height,width), dtype=np.uint8) * 255
        self.image =  cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        self.height, self.width = image.shape[:2]
    def save(self, filename='saved_image'):
        cv2.imwrite(f'{filename}.jpg', self.image)

    def show(self):
        plt.imshow(self.image)
        plt.show()

    def draw_rectangle(self,x,y,w,h,thickness=2,color=(0,0,0), padding=0):
        cv2.rectangle(self.image, (x+padding, y+padding), (x + w-padding, y + h-padding), color, thickness)

    def top_layout(self, h_prop):
        # Divide the image into header and content sections
        self.header_size = int(self.height * h_prop)
        
        self.draw_rectangle(
                            x=0,
                            y=0,
                            w=self.width,
                            h=self.header_size,
                            thickness=2,
                            color=(0,0,0),
                            padding=5)
    def bottom_layout(self):
        self.content_size = int(self.height - self.header_size)
        """self.draw_rectangle(x=0,
                            y=self.header_size,
                            w=self.width,
                            h = self.content_size,
                            thickness=0,
                            padding=5,
                            )"""
   
    def mcf_box(self):
        self.mcf_height = self.content_size
        print(self.content_size/26)
        # 23 per row
        self.mcf_max_width = int(math.ceil(175/25))
        # 182 per column
        self.mcf_width = int(math.ceil(self.mcf_count/25))*int(self.width/self.mcf_max_width)
        self.draw_rectangle(x=0,
                            y=self.header_size,
                            w=self.mcf_width,
                            h = self.mcf_height,
                            padding=10,
                            thickness=3)
    def tf_box(self):
        self.tf_height = self.content_size
        self.tf_max_width = int(math.ceil(300/25))
        self.tf_width = int(math.ceil(self.tf_count/25))*int(self.width/self.tf_max_width)
        self.draw_rectangle(x=self.mcf_width,
                            y=self.header_size,
                            w=self.tf_width,
                            h = self.tf_height,
                            padding=10,
                            thickness=3)
    
    def mcf_create_choices(self):
        self.draw_rectangle(
            x=0+15+25,
            y=self.header_size+15,
            w=23,
            h=23,
            thickness=3,
        )
    
drawer = Drawer(1280,720,mcf=100,tf=0,idtf=10)
drawer.top_layout(0.15)
drawer.bottom_layout()
drawer.mcf_box()
drawer.tf_box()
drawer.mcf_create_choices()
drawer.show()
drawer.save()
"""# Calculate square size based on image dimensions
square_size = min(image.shape) // 4  # Divide by 4 to fit three squares with equal spacing

# Calculate square positions to fit equally within the image
margin = (image.shape[0] - 3 * square_size) // 4  # Margin between squares
square1 = [(margin, margin), (margin + square_size, margin + square_size)]
square2 = [(2 * margin + square_size, margin), (2 * margin + 2 * square_size, margin + square_size)]
square3 = [(3 * margin + 2 * square_size, margin), (3 * margin + 3 * square_size, margin + square_size)]

# Draw squares on the image
cv2.rectangle(image, square1[0], square1[1], (0, 0, 0),2)  # Black color, -1 means filled
cv2.rectangle(image, square2[0], square2[1], (0, 0, 0),2)
cv2.rectangle(image, square3[0], square3[1], (0, 0, 0),2)

# Display the image using Matplotlib
plt.imshow(image, cmap='gray')
plt.title('White Image with Equally Fitted Black Squares')
plt.axis('off')  # Turn off axis
plt.show()
"""