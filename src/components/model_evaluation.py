import os
import logging
from keras.models import load_model

from src.entity.s3_estimator import S3ModelResolver
from src.utils.main_utils import load_data_for_evaluation
from src.constants import MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelEvaluation:
    def __init__(self):
        self.model_resolver = S3ModelResolver()
        self.model_dir = "models"

    def evaluate_and_push(self):
        try:
            current_model_path = os.path.join(self.model_dir, "sleep_detection_model.h5")
            logging.info(f"Current trained model path: {current_model_path}")

            latest_model_path = self.model_resolver.get_latest_model_path()

            if latest_model_path is None:
                logging.info("No existing model in S3. Uploading current model.")
                self.model_resolver.push_model_to_s3(current_model_path)
                return

            # Load both models
            current_model = load_model(current_model_path)
            previous_model = load_model(latest_model_path)

            # Load validation data (create helper function to return generator)
            val_gen = load_data_for_evaluation()  # Define this in your utils/model_utils.py

            current_loss, current_acc = current_model.evaluate(val_gen)
            prev_loss, prev_acc = previous_model.evaluate(val_gen)

            logging.info(f"Current Model Accuracy: {current_acc}")
            logging.info(f"Previous Model Accuracy: {prev_acc}")

            improvement = current_acc - prev_acc
            if improvement > MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE:
                logging.info("New model is better. Uploading to S3.")
                self.model_resolver.push_model_to_s3(current_model_path)
            else:
                logging.info("No significant improvement. Skipping upload.")

        except Exception as e:
            logging.error(f"Error during model evaluation: {str(e)}")
            raise e
if __name__ == "__main__":
    evaluator = ModelEvaluation()
    evaluator.evaluate_and_push()
