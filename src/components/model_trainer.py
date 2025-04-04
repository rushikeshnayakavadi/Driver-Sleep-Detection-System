from src.entity.estimator import ModelTrainer

class ModelTraining:
    def __init__(self, config):
        self.config = config
        self.trainer = ModelTrainer()

    def initiate_model_training(self, X_train, y_train, X_test, y_test):
        """Start model training"""
        model = self.trainer.train(X_train, y_train, X_test, y_test)
        model.save(self.config.model_path)  # Save trained model
        print(f"✅ Model saved at {self.config.model_path}")
    