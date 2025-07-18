import pandas as pd
import os # to handle file paths and directories
import numpy as np # for numerical operations
from sklearn.model_selection import train_test_split # reduces data leakage
import logging 
import yaml


# Ensure the "logs" directory exists
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True) # exist_ok=True --> check the directory exists, if not create it


# logging configuration
logger = logging.getLogger('data_ingestion') # data logger setup
# set the logging level to DEBUG --> from very basic to very detailed
logger.setLevel('DEBUG') # set the logging level to DEBUG which is equivalent to logging.DEBUG 
# by setting it to 'DEBUG', we can capture all levels of logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# create handlers for console and file logging
# console_handler will log messages to the console
console_handler = logging.StreamHandler() # StreamHandler --> logs messages to the console in real-time
console_handler.setLevel('DEBUG') 

# file_handler will log messages to a file
# FileHandler --> logs messages to a file, which is useful for persistent logging
log_file_path = os.path.join(log_dir, 'data_ingestion.log') # create a log file in the logs directory such that it can be easily accessed
file_handler = logging.FileHandler(log_file_path) # logs messages to a file
file_handler.setLevel('DEBUG') # set the logging level to DEBUG for file handler


# formatter is used to format the log messages 
# it is used to format the log messages in a specific way
# here we are using a simple format that includes the timestamp, logger name, log level,
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
console_handler.setFormatter(formatter) # set the formatter for console handler
file_handler.setFormatter(formatter) # set the formatter for file handler


# add the handlers to the logger object
# handlers are responsible for sending the log messages to the appropriate destination
# in this case, we are adding both console_handler and file_handler to the logger object
# this will allow the logger to log messages to both console and file
logger.addHandler(console_handler)
logger.addHandler(file_handler)


#Function definitions for data ingestion and preprocessing
def load_params(params_path: str) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logger.debug('Parameters retrieved from %s', params_path)
        return params
    except FileNotFoundError:
        logger.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logger.error('YAML error: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error: %s', e)
        raise


def load_data(data_url: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(data_url)
        logger.debug('Data loaded from %s', data_url)
        return df
    except pd.errors.ParserError as e:
        logger.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error occurred while loading the data: %s', e)
        raise

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data."""
    try:
        df.drop(columns = ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace = True)
        df.rename(columns = {'v1': 'target', 'v2': 'text'}, inplace = True)
        logger.debug('Data preprocessing completed')
        return df
    except KeyError as e:
        logger.error('Missing column in the dataframe: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error during preprocessing: %s', e)
        raise

def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str) -> None:
    """Save the train and test datasets."""
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path, "train.csv"), index=False)
        test_data.to_csv(os.path.join(raw_data_path, "test.csv"), index=False)
        logger.debug('Train and test data saved to %s', raw_data_path)
    except Exception as e:
        logger.error('Unexpected error occurred while saving the data: %s', e)
        raise

def main():
    try:
        params = load_params(params_path='params.yaml')
        test_size = params['data_ingestion']['test_size']
        # test_size = 0.2
        data_path = 'https://raw.githubusercontent.com/vikashishere/Datasets/main/spam.csv'
        df = load_data(data_url=data_path)
        final_df = preprocess_data(df)
        train_data, test_data = train_test_split(final_df, test_size=test_size, random_state=2)
        save_data(train_data, test_data, data_path='./data')
    except Exception as e:
        logger.error('Failed to complete the data ingestion process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()