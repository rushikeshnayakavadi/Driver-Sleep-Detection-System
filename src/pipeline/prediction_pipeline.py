import cv2
import numpy as np
from keras.models import load_model

class PredictionPipeline:
    def __init__(self, model_path="models/sleep_detection_model.h5"):
        self.model = load_model(model_path)

    def preprocess_frame(self, frame):
        resized = cv2.resize(frame, (224, 224))  # Change size if your model expects different
        normalized = resized / 255.0
        reshaped = np.expand_dims(normalized, axis=0)
        return reshaped

    def predict(self, frame):
        processed = self.preprocess_frame(frame)
        prediction = self.model.predict(processed)[0][0]  # Assuming binary output
        return "Drowsy" if prediction > 0.5 else "Alert"
