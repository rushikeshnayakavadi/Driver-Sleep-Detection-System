import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from src.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def build_model(self):
        """Define a simple CNN model for image classification."""
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(4, activation='softmax')  # 4 classes: Closed, Open, Yawn, No_Yawn
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.learning_rate),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def train_model(self):
        """Train the CNN model using image data."""
        train_datagen = ImageDataGenerator(rescale=1./255)
        test_datagen = ImageDataGenerator(rescale=1./255)

        train_generator = train_datagen.flow_from_directory(
            "data/train",
            target_size=(64, 64),
            batch_size=self.config.batch_size,
            class_mode='categorical'
        )

        validation_generator = test_datagen.flow_from_directory(
            "data/test",
            target_size=(64, 64),
            batch_size=self.config.batch_size,
            class_mode='categorical'
        )

        model = self.build_model()

        model.fit(
            train_generator,
            epochs=self.config.epochs,
            validation_data=validation_generator
        )

        # Save model
        model.save(self.config.model_save_path)
        print(f"Model saved at {self.config.model_save_path}")

if __name__ == "__main__":
    print("Starting Model Training...")

    config = ModelTrainerConfig(
        model_save_path="models/sleep_detection_model.h5",
        learning_rate=0.001,
        batch_size=32,
        epochs=10
    )

    trainer = ModelTrainer(config)
    trainer.train_model()

    print("Model Training Complete!")
