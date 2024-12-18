import os

from ultralytics import YOLO

from dotenv import load_dotenv

load_dotenv()


class YoloService:
    def __init__(self):
        self.model = None
        # self.model_folder = "yolo11n_ncnn_model"
        self.model_folder = "./models/disrupton_plus_v2_ncnn_model"
        self.load_or_create_model()

    def load_or_create_model(self):
        if os.path.exists(self.model_folder):
            self.load_model()
        else:
            self.create_model()
            self.load_model()

    def create_model(self):
        # model = YOLO("yolo11n.pt", task="detect")
        model = YOLO("./models/roboflow_models/best.pt", task="detect")
        model.export(format="ncnn")

    def load_model(self):
        self.model = YOLO(self.model_folder, task="detect")

    def analyze_photo(self, photo):
        results = self.model.predict(
            source=photo,
            conf=0.4,
            half=True,
            iou=0.4,
            agnostic_nms=True,
            verbose=False,
            vid_stride=2,
            augment=True,
            # stream=True, # doesnt allow fsm to run in parallel for some reason
            show=True,
        )
        # print(results)
        return results
