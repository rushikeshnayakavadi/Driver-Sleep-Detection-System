import os
import cv2
import numpy as np
from src.entity.config_entity import DataTransformationConfig
from src.utils.main_utils import save_json

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def transform_image(self, image_path):
        """Resize and normalize image."""
        img = cv2.imread(image_path)
        img = cv2.resize(img, self.config.target_size)
        img = img / 255.0  # Normalize (0-1)
        return img

    def transform_data(self):
        """Apply transformations to all images."""
        os.makedirs(self.config.transformed_data_dir, exist_ok=True)
        transformed_images = []

        for category in ["Closed", "Open", "Yawn", "No_Yawn"]:
            category_path = os.path.join(self.config.transformed_data_dir, category)
            os.makedirs(category_path, exist_ok=True)
            
            for img_name in os.listdir(category_path):
                img_path = os.path.join(category_path, img_name)
                transformed_img = self.transform_image(img_path)
                transformed_images.append(transformed_img)

        print("Data Transformation Complete!")

if __name__ == "__main__":
    print("Starting Data Transformation...")

    transformation_config = DataTransformationConfig(
        target_size=(224, 224),
        normalization_mean=[0.5, 0.5, 0.5],
        normalization_std=[0.5, 0.5, 0.5],
        transformed_data_dir="data/transformed"
    )

    data_transformer = DataTransformation(transformation_config)
    data_transformer.transform_data()

    print("Data Transformation Done!")
