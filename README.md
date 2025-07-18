# ML Pipeline with DVC and AWS Integration

## Project Overview
This project implements an end-to-end machine learning pipeline for text classification using Data Version Control (DVC) for experiment tracking and AWS S3 for remote storage. The pipeline includes data ingestion, preprocessing, feature engineering, model training, and evaluation.

## Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────────────┐
│                           ML Pipeline Architecture                       │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Local Development Environment                  │
├─────────────────┬─────────────────┬─────────────────┬──────────────────┤
│  Data Ingestion  │  Preprocessing   │    Feature      │    Model         │
│                 │                 │   Engineering    │   Training       │
└─────────────────┴─────────────────┴─────────────────┴──────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                             DVC Pipeline                                 │
├─────────────────────────────┬───────────────────────────────────────────┤
│     Experiment Tracking     │           Parameter Management             │
└─────────────────────────────┴───────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                AWS Cloud                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────┐                                                   │
│   │     AWS S3      │                                                   │
│   │                 │                                                   │
│   │  Remote Storage │                                                   │
│   │  for DVC Data   │                                                   │
│   └─────────────────┘                                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Details

#### 1. Data Pipeline Components
- **Data Ingestion** (`src/data_ingestion.py`): Loads data from a URL, preprocesses it, and splits it into training and testing sets.
- **Data Preprocessing** (`src/data_preprocessing.py`): Handles text cleaning and transformation.
- **Feature Engineering** (`src/feature_engineering.py`): Applies TF-IDF vectorization to transform text data into numerical features.
- **Model Training** (`src/model_training.py`): Trains a machine learning model using the processed features.
- **Model Evaluation** (`src/model_evaluation.py`): Evaluates model performance using metrics like accuracy, precision, and recall.

#### 2. DVC Integration
- **Experiment Tracking**: Uses DVCLive to track experiments and visualize metrics.
- **Parameter Management**: Centralizes hyperparameters in `params.yaml` for reproducible experiments.
- **Pipeline Automation**: Defines the ML pipeline stages in `dvc.yaml` for automated execution.

#### 3. AWS Integration
- **S3 Bucket**: Remote storage for model artifacts, datasets, and experiment results.
- **IAM User**: Provides secure access to AWS resources with appropriate permissions.
- **AWS CLI**: Command-line interface for interacting with AWS services.

## Setup and Installation

### Prerequisites
- Python 3.7+
- Git
- AWS Account
- AWS CLI

### Installation Steps
1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure AWS CLI:
   ```
   pip install awscli
   aws configure
   ```

4. Initialize DVC:
   ```
   dvc init
   ```

5. Add remote storage:
   ```
   dvc remote add -d dvcstore s3://your-bucket-name
   ```

## Running the Pipeline

### Execute the Complete Pipeline
```
dvc repro
```

### Run Experiments
```
dvc exp run
```

### View Experiment Results
```
dvc exp show
```

### Push to Remote Storage
```
dvc push
```

## Project Structure
```
├── .dvc/                  # DVC configuration
├── dvclive/               # Experiment tracking data
│   ├── metrics.json       # Tracked metrics
│   ├── params.yaml        # Parameters used in experiments
│   └── plots/             # Metric visualizations
├── experiments/           # Jupyter notebooks for exploration
├── src/                   # Source code
│   ├── data_ingestion.py  # Data loading and splitting
│   ├── data_preprocessing.py # Text preprocessing
│   ├── feature_engineering.py # Feature extraction
│   ├── model_training.py  # Model training
│   └── model_evaluation.py # Model evaluation
├── dvc.yaml               # DVC pipeline definition
├── params.yaml            # Hyperparameters
└── README.md              # Project documentation
```

## AWS Architecture Details

### S3 Storage Configuration
The project uses AWS S3 for storing:
- Raw datasets
- Processed features
- Trained models
- Experiment metrics and results

### Security and Access Control
- IAM user with specific permissions for S3 access
- Credentials managed via AWS CLI configuration
- Bucket policies to control access to stored data

### Data Flow with AWS
1. Local code execution processes data and trains models
2. DVC tracks changes and manages versioning
3. Model artifacts and data are pushed to S3 using `dvc push`
4. Experiments can be reproduced by pulling specific versions from S3 using `dvc pull`

## Best Practices
- Keep sensitive information out of version control
- Use `.dvcignore` to exclude large files from DVC tracking
- Regularly push to remote storage to back up experiments
- Document parameter changes for each experiment

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request