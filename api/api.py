from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
import numpy as np
import cv2

app = FastAPI()

CLASSES = {
    0: "Cashier",
    1: "Civil Servant (Batik)",
    2: "Civil Servant (Uniform)",
    3: "Military Camouflage",
    4: "Military Uniform",
    5: "No Flag"
}

model = tf.keras.models.load_model("model.keras")


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):

    # Read uploaded file
    content = await file.read()

    # Convert bytes -> numpy array
    img = np.frombuffer(content, np.uint8)

    # Decode JPEG/PNG -> OpenCV image
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Could not decode image"}

    img = cv2.resize(img, (299, 299))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.expand_dims(img, axis=0)

    predictions = model.predict(img)

    cat = np.argmax(predictions[0])

    return {
        "description": CLASSES[cat],
        "probability": np.round(float(predictions[0][cat]), 2)
    }