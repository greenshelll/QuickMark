from jnius import autoclass

# Get the necessary Android classes
Camera = autoclass('android.hardware.Camera')
CameraParameters = autoclass('android.hardware.Camera$Parameters')

def get_highest_resolution():
    # Open the camera
    camera = Camera.open()
    try:
        # Get the camera parameters
        params = camera.getParameters()

        # Get the supported picture sizes
        supported_picture_sizes = params.getSupportedPictureSizes()
        print([x for x in supported_picture_sizes])
        # Find the highest resolution
        max_resolution = (0, 0)
        for size in supported_picture_sizes:
            width, height = size.width, size.height
            if width * height > max_resolution[0] * max_resolution[1]:
                max_resolution = (width, height)

        return max_resolution

    finally:
        # Release the camera
        camera.release()
