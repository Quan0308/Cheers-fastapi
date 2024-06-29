from fastapi import FastAPI
from model import ObjectDetectionModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/predict")
def predict():
    model = ObjectDetectionModel()
    response = model.predict("c3928afa-BZ1A0675.jpg")
    print(response)
    return {"message": "Prediction done"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)