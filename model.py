from ultralytics import YOLO
from PIL import Image
from data_class.detected_object import DetectedObject
from data_class.postition import Position

from typing import List
import logging

class ObjectDetectionModel:
    def __init__(self):
        self.model = YOLO('best.pt')

    def predict(self, image: Image):
        try:
            results =  self.model.predict(source=image, save=True, save_txt=True)
            boxes = results[0].boxes.xyxy.tolist()
            classes = results[0].boxes.cls.tolist()
            names = results[0].names

            return self.predict_response(boxes, classes, names, image)
        except Exception as e:
            logging.error(f"Error while predicting: {e}")
            return []
    
    def predict_response(self, boxes: list, classes: list, names: list, image: Image) -> List[DetectedObject]:
        res = []
        for box, class_index in zip(boxes, classes):
            x1, y1, x2, y2 = box
            res.append(DetectedObject(
            position=Position(x1, y1, x2, y2),
            type=names[class_index],
            image=image.crop((x1, y1, x2, y2))
        ))
        return res