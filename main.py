from fastapi import FastAPI, UploadFile
from object_detection_model import ObjectDetectionModel
from multilabel_classification_model import MultilabelClassificationModel
from utils import response_helper
from PIL import Image
from io import BytesIO
from pydantic import BaseModel

import requests

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


class ImageLink(BaseModel):
    link: str

@app.post("/predict")
async def predict(link: ImageLink):
    link = link.link
    response = requests.get(link)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    obj_detection_model = ObjectDetectionModel()
    multilabel_classification_model = MultilabelClassificationModel()
    detection_objects = obj_detection_model.predict(image)
    res: list = []

    for obj in detection_objects:
        data = multilabel_classification_model.predict(obj)
        res.append(data)
    
    res = response_helper.ResponseHelper.create_response(res)

    return {"message": "Prediction done", "data": res}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)