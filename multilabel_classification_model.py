from tensorflow import keras
from tensorflow.keras.preprocessing import image

from data_class.detected_object import DetectedObject
from data_class.multilabel import MultilabelObject
import numpy as np

class MultilabelClassificationModel:
    def __init__(self):
        self.model_directory = 'models/logo_resnet50_model_0.46'
        self.model_layer = keras.layers.TFSMLayer(self.model_directory, call_endpoint='serving_default')
        self.model = keras.Sequential([
            self.model_layer
        ])
        self.classes=['tiger', 'larue', 'bia_viet', 'heineken', 'bivina', 'strongbow', 'edelweiss']

    def predict(self, detected_objects):
        img = detected_objects.image
        img = img.resize((224, 224))

        X = image.img_to_array(img)
        X = np.expand_dims(X, axis=0)
        images = np.vstack([X])

        
        predictions = self.model.predict(images)
        first_key = list(predictions.keys())[0]
        predictions = predictions[first_key][0]
       
        return MultilabelObject(
            position=detected_objects.position,
            type=detected_objects.type, 
            value=detected_objects.value, 
            brands={ self.classes[j]: str(predictions[j]) for j in range(len(predictions)) if predictions[j] > 0.01 }
        )