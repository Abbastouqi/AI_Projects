# 🦟 Dengue Outbreak Predictor

A comprehensive machine learning project for predicting dengue fever outbreaks using climate data and advanced anomaly detection techniques.

## 📋 Project Overview

This project implements a complete pipeline for dengue outbreak prediction including:

- **Data Collection**: Merge climate data with case reports and store in SQLite database
- **Data Wrangling**: Handle missing values, outliers, and inconsistent date formats
- **Feature Engineering**: Create lag features, rolling averages, and seasonal indicators
- **ML Models**: Train and compare k-NN, Naive Bayes, and Random Forest models
- **Anomaly Detection**: Flag unusual spikes that might indicate outbreaks
- **Dashboard**: Interactive Streamlit app with risk maps and predictions

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone and setup environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

2. **Run the complete pipeline:**
```bash
python main.py
```

3. **Launch the dashboard:**
```bash
streamlit run src/dashboard.py
```

## 📁 Project Structure

```
Dengue-Outbreak-Predictor/
├── archive (4)/                    # Raw dataset files
│   ├── DengAI_Predicting_Disease_Spread_-_Training_Data_Features.csv
│   ├── DengAI_Predicting_Disease_Spread_-_Training_Data_Labels.csv
│   ├── DengAI_Predicting_Disease_Spread_-_Test_Data_Features.csv
│   └── DengAI_Predicting_Disease_Spread_-_Submission_Format.csv
├── src/                           # Source code modules
│   ├── __init__.py
│   ├── data_collection.py         # Data loading and database operations
│   ├── data_wrangling.py          # Data cleaning and preprocessing
│   ├── feature_engineering.py     # Feature creation and transformation
│   ├── ml_models.py               # Machine learning models
│   ├── anomaly_detection.py       # Outbreak anomaly detection
│   └── dashboard.py               # Streamlit dashboard
├── main.py                        # Main execution script
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## 🎯 Key Results

- **Random Forest**: 99.14% R² accuracy (best model)
- **320 anomalies detected** across multiple methods
- **Interactive dashboard** with risk maps and visualizations
- **69 engineered features** including lag and seasonal patterns

## 🔧 Components

### 1. Data Collection (`data_collection.py`)
- Loads raw CSV files from DengAI competition
- Merges climate features with dengue case reports
- Creates SQLite database with proper schema
- Provides SQL queries for feature extraction by region/month

### 2. Data Wrangling (`data_wrangling.py`)
- Handles missing values using KNN imputation
- Detects and handles outliers using IQR method
- Standardizes date formats and creates date features
- Validates data consistency

### 3. Feature Engineering (`feature_engineering.py`)
- Creates lag features from previous weeks' cases
- Generates rolling averages and statistical features
- Adds seasonal and cyclical features
- Creates interaction features between climate variables
- Encodes categorical variables

### 4. ML Models (`ml_models.py`)
- **k-Nearest Neighbors**: Distance-based regression with hyperparameter tuning
- **Naive Bayes**: Gaussian NB adapted for regression through binning
- **Random Forest**: Ensemble method with feature importance analysis
- Cross-validation and performance comparison
- Model persistence and loading

### 5. Anomaly Detection (`anomaly_detection.py`)
- Statistical anomaly detection (IQR, Z-score, Modified Z-score)
- Seasonal anomaly detection based on historical patterns
- ML-based anomaly detection using Isolation Forest
- Outbreak pattern detection for sustained increases
- Comprehensive anomaly scoring and visualization

### 6. Dashboard (`dashboard.py`)
- Interactive Streamlit web application
- Time series visualizations with anomaly highlighting
- Model performance comparison and feature importance
- Real-time prediction capabilities

## 📊 Dashboard Features

### Overview Tab
- Key metrics and summary statistics
- Total cases, anomaly rates, city comparisons

### Time Series Tab
- Interactive time series plots
- Anomaly highlighting
- Seasonal pattern analysis

### Anomalies Tab
- Anomaly detection summary
- Top anomalies table with scores
- Multiple detection method results

### Data Tab
- Dataset overview and raw data viewer
- Data exploration tools

## 🎯 Model Performance

The project trains and compares three models:

1. **Random Forest** (best performer)
   - MAE: 0.9957, R²: 0.9914 (99.14% variance explained)
   - Handles non-linear relationships
   - Provides feature importance

2. **k-Nearest Neighbors**
   - MAE: 4.5610, R²: 0.8901 (89.01% variance explained)
   - Good for local patterns
   - Distance-based similarity

3. **Naive Bayes**
   - MAE: 5.8870, R²: 0.8218 (82.18% variance explained)
   - Fast training and prediction
   - Baseline comparison

## 🚨 Anomaly Detection Results

- **218 statistical anomalies** (IQR and Z-score based)
- **67 seasonal anomalies** (deviation from historical patterns)
- **146 ML-based anomalies** (Isolation Forest)
- **4 outbreak patterns** (sustained case increases)

## 🔍 Usage Examples

### Running Individual Components

```python
from src.data_collection import DataCollector
from src.ml_models import MLModelTrainer

# Load and process data
collector = DataCollector()
train_features, train_labels, test_features = collector.load_raw_data()
merged_data = collector.merge_training_data(train_features, train_labels)

# Train models
trainer = MLModelTrainer()
models = trainer.train_all_models(merged_data)
performance = trainer.compare_model_performance()
```

### Custom Anomaly Detection

```python
from src.anomaly_detection import AnomalyDetector

detector = AnomalyDetector()
anomaly_data = detector.comprehensive_anomaly_detection(data)
top_anomalies = detector.get_top_anomalies(anomaly_data, top_n=10)
```

## 📈 Results

After running the complete pipeline, you'll get:

- **Database**: SQLite database with structured climate and case data
- **Models**: Trained ML models with 99.14% accuracy
- **Predictions**: Test set predictions for competition submission
- **Dashboard**: Interactive web app for exploration and monitoring
- **Anomaly Reports**: Detected outbreaks and unusual patterns

## 🛠️ Customization

### Adding New Features
Extend `feature_engineering.py` to add custom features:

```python
def create_custom_features(self, df):
    # Add your custom feature engineering logic
    df['custom_feature'] = df['temperature'] * df['humidity']
    return df
```

### New Models
Add models to `ml_models.py`:

```python
def train_custom_model(self, X_train, y_train):
    from sklearn.svm import SVR
    model = SVR()
    model.fit(X_train, y_train)
    return model
```

## 🙏 Acknowledgments

- DengAI competition dataset from DrivenData
- Climate data from NOAA and other meteorological sources
- Open source libraries: scikit-learn, pandas, streamlit, plotly

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for public health and disease prevention**