import os

from ultralytics import YOLO


class YoloService:
    def __init__(self):
        self.model = None
        # self.model_folder = "yolo11n_ncnn_model"
        self.model_folder = "disrupton_v1_ncnn_model"
        self.load_or_create_model()

    def load_or_create_model(self):
        if os.path.exists(self.model_folder):
            self.load_model()
        else:
            self.create_model()
            self.load_model()

    def create_model(self):
        # model = YOLO("yolo11n.pt", task="detect")
        model = YOLO("utec11n.pt", task="detect")
        model.export(format="ncnn")

    def load_model(self):
        self.model = YOLO(self.model_folder, task="detect")

    def analyze_photo(self, photo):
        results = self.model.predict(photo, conf=0.6)
        return results
