from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from object_detection_model import ObjectDetectionModel
from multilabel_classification_model import MultilabelClassificationModel
from data_class.multilabel import MultilabelObject as Mul
from utils import response_helper
from PIL import Image
from io import BytesIO
from pydantic import BaseModel

import requests

app = FastAPI()

origins = [
    "http://localhost:3000",  # Allow requests from this origin
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    res: Mul = []

    for obj in detection_objects:
        data = multilabel_classification_model.predict(obj)
        res.append(data)
    
    space_res = multilabel_classification_model.predict_space(image)

    return {"message": "Prediction done", "data": response_helper.ResponseHelper.create_response(res, space_res)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)