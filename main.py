import uvicorn
from fastapi import FastAPI, File, UploadFile
import skimage
import numpy as np
import os 
from PIL import Image
from io import BytesIO
from keras.models import load_model

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# port = int(os.getenv("PORT"))
port = os.getenv("PORT")
if port is None:
  port = 8000

app = FastAPI()

image_shape = (100, 100)

def read_image(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    image = np.asarray(image)
    return image

def preprocess_image(image: np.ndarray):
    image = skimage.transform.resize(image, image_shape, mode='reflect')
    image = np.expand_dims(image, 0)

    return image

model = load_model("model/")

class_name = [
    'Varroa, Small Hive Beetles', 
    'ant problems',
    'few varrao, hive beetles', 
    'healthy', 
    'hive being robbed',
    'missing queen'
]


def predict_image_class(image: np.ndarray):
    prediction = model.predict(image)
    idx = np.argmax(prediction)

    return class_name[idx]

@app.post("/predict")
async def predict_api(file: UploadFile = File(...)):
    image = read_image(await file.read())
    image = preprocess_image(image)

    prediction = predict_image_class(image)
    return {'prediction': prediction}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)