from src.entity.estimator import DataTransformer

class DataTransformation:
    def __init__(self, config):
        self.config = config
        self.transformer = DataTransformer()

    def initiate_data_transformation(self):
        """Transform training and testing dataset"""
        X_train, y_train = self.transformer.transform_dataset(self.config.train_data_path)
        X_test, y_test = self.transformer.transform_dataset(self.config.test_data_path)

        print("✅ Data Transformation Completed")
        return X_train, y_train, X_test, y_test
