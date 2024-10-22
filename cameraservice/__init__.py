try:
    from picamera2 import Picamera2
    print
except ImportError:
    import cv2

class CameraService:
    def __init__(self):
        self.camera = Picamera2()

    def start(self):
        self.camera.preview_configuration.main.size = (640, 360)
        self.camera.preview_configuration.main.format = "RGB888"
        self.camera.preview_configuration.align()
        self.camera.configure("preview")
        self.camera.start()
    
    def stop(self):
        self.camera.stop()

    def get_photo(self):
        frame = self.camera.capture_array()
        return frame
    
class WindowsCameraService:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def start(self):
        self.camera.set(3, 640)
        self.camera.set(4, 360)
    
    def stop(self):
        self.camera.release()

    def get_photo(self):
        success, frame = self.camera.read()
        if success:
            return frame
        return None