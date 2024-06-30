from tensorflow import keras
from tensorflow.keras.preprocessing import image

from data_class.detected_object import DetectedObject
from data_class.multilabel import MultilabelObject
import numpy as np

class MultilabelClassificationModel:
    def __init__(self):
        self.model_directory = 'models/logo_resnet50_model_0.46'
        self.space_model_directory = 'models/space_resnet50_model_0.61'
        self.model_layer = keras.layers.TFSMLayer(self.model_directory, call_endpoint='serving_default')
        self.model = keras.Sequential([
            self.model_layer
        ])
        self.space_model_layer = keras.layers.TFSMLayer(self.space_model_directory, call_endpoint='serving_default')
        self.space_model = keras.Sequential([
            self.space_model_layer
        ])
        self.classes=['tiger', 'larue', 'bia_viet', 'heineken', 'bivina', 'strongbow', 'edelweiss']
        self.space_classes=['event', 'restaurant', 'place_of_distribution', 'grocery', 'street', 'karaoke', 'supermarket', 'bar']

    def predict(self, detected_objects):
        img = detected_objects.image
        img = img.resize((224, 224))

        X = image.img_to_array(img)
        X = np.expand_dims(X, axis=0)
        images = np.vstack([X])

        
        predictions = self.model.predict(images)
        space_predictions = self.space_model.predict(images)

        first_key = list(predictions.keys())[0]
        space_first_key = list(space_predictions.keys())[0]

        predictions = predictions[first_key][0]
        space_predictions = space_predictions[space_first_key][0]
       
        return MultilabelObject(
            position=detected_objects.position,
            type=detected_objects.type, 
            value=detected_objects.value, 
            brands={ self.classes[j]: str(predictions[j]) for j in range(len(predictions)) if predictions[j] > 0.01 },
            spaces={ self.space_classes[j]: str(space_predictions[j]) for j in range(len(space_predictions)) if space_predictions[j] > 0.01 }
        )