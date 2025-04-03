import logging
from src.components.data_ingestion import DataIngestion
from src.entity.config_entity import DataIngestionConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def start_training_pipeline():
    """Runs the complete training pipeline."""
    logging.info("Starting Training Pipeline...")

    try:
        ingestion_config = DataIngestionConfig(local_data_path="data/")
        ingestion = DataIngestion(ingestion_config)

        logging.info("Initiating Data Ingestion...")
        result = ingestion.initiate_data_ingestion()

        if result:
            logging.info("Data Ingestion Completed Successfully!")
        else:
            logging.error("Data Ingestion Failed.")

    except Exception as e:
        logging.error(f"Training Pipeline Failed: {e}")

if __name__ == "__main__":
    start_training_pipeline()
