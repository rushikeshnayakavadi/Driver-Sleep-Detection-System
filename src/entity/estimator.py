import cv2
import os
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

class DataTransformer:
    def __init__(self, image_size=(224, 224)):
        self.image_size = image_size

    def preprocess_image(self, img_path):
        """Load and preprocess a single image"""
        img = cv2.imread(img_path)
        img = cv2.resize(img, self.image_size)
        img = img / 255.0  # Normalize
        return img

    def transform_dataset(self, data_folder):
        """Transform all images in dataset"""
        X, y = [], []
        for class_name in os.listdir(data_folder):
            class_path = os.path.join(data_folder, class_name)
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                X.append(self.preprocess_image(img_path))
                y.append(class_name)
        return np.array(X), np.array(y)


class ModelTrainer:
    def __init__(self, image_size=(224, 224), num_classes=4):
        self.image_size = image_size
        self.num_classes = num_classes
        self.model = self.build_model()

    def build_model(self):
        """Build a CNN model"""
        model = keras.Sequential([
            layers.Conv2D(32, (3, 3), activation="relu", input_shape=(*self.image_size, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dense(self.num_classes, activation="softmax")
        ])
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        return model

    def train(self, X_train, y_train, X_test, y_test, epochs=10, batch_size=32):
        """Train the CNN model"""
        self.model.fit(np.array(X_train), np.array(y_train), epochs=epochs, batch_size=batch_size,
                       validation_data=(np.array(X_test), np.array(y_test)))
        print("✅ Model Training Completed")
        return self.model
