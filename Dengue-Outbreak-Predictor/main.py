"""
Main execution script for Dengue Outbreak Predictor
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append('src')

from data_collection import DataCollector
from data_wrangling import DataWrangler
from feature_engineering import FeatureEngineer
from ml_models import MLModelTrainer
from anomaly_detection import AnomalyDetector

def main():
    print("🦟 Dengue Outbreak Predictor")
    print("=" * 50)
    
    # Initialize components
    data_collector = DataCollector()
    data_wrangler = DataWrangler()
    feature_engineer = FeatureEngineer()
    ml_trainer = MLModelTrainer()
    anomaly_detector = AnomalyDetector()
    
    # Step 1: Data Collection
    print("\n1. Data Collection and Database Setup")
    print("-" * 40)
    
    # Load raw data
    train_features, train_labels, test_features = data_collector.load_raw_data()
    print(f"Training features shape: {train_features.shape}")
    print(f"Training labels shape: {train_labels.shape}")
    print(f"Test features shape: {test_features.shape}")
    
    # Merge training data
    merged_data = data_collector.merge_training_data(train_features, train_labels)
    print(f"Merged training data shape: {merged_data.shape}")
    
    # Create database and store data
    data_collector.create_database_schema()
    data_collector.store_data_to_db(merged_data)
    print("Data stored in SQLite database: dengue_data.db")
    
    # Step 2: Data Wrangling
    print("\n2. Data Wrangling")
    print("-" * 40)
    
    clean_data = data_wrangler.clean_data_pipeline(merged_data)
    print(f"Clean data shape: {clean_data.shape}")
    
    # Step 3: Feature Engineering
    print("\n3. Feature Engineering")
    print("-" * 40)
    
    engineered_data = feature_engineer.feature_engineering_pipeline(clean_data)
    print(f"Engineered data shape: {engineered_data.shape}")
    
    # Step 4: Machine Learning Models
    print("\n4. Machine Learning Models")
    print("-" * 40)
    
    models = ml_trainer.train_all_models(engineered_data)
    performance_df = ml_trainer.compare_model_performance()
    ml_trainer.save_models()
    
    # Step 5: Anomaly Detection
    print("\n5. Anomaly Detection")
    print("-" * 40)
    
    anomaly_data = anomaly_detector.comprehensive_anomaly_detection(engineered_data)
    anomaly_summary = anomaly_detector.get_anomaly_summary(anomaly_data)
    top_anomalies = anomaly_detector.get_top_anomalies(anomaly_data)
    
    # Step 6: Generate Predictions for Test Data
    print("\n6. Test Data Predictions")
    print("-" * 40)
    
    # Process test data
    test_clean = data_wrangler.clean_data_pipeline(test_features)
    test_engineered = feature_engineer.feature_engineering_pipeline(test_clean, is_training=False)
    
    # Prepare test data for prediction
    exclude_cols = ['city', 'year', 'weekofyear', 'week_start_date']
    feature_cols = [col for col in test_engineered.columns if col not in exclude_cols]
    
    X_test_df = test_engineered[feature_cols].select_dtypes(include=[np.number])
    
    # Align features with training data
    training_features = ml_trainer.feature_names
    missing_features = set(training_features) - set(X_test_df.columns)
    
    # Add missing features with zeros
    for feature in missing_features:
        X_test_df[feature] = 0
    
    X_test_df = X_test_df[training_features]
    X_test = X_test_df.values.astype(np.float64)
    X_test = np.nan_to_num(X_test, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Make predictions
    predictions = ml_trainer.predict(X_test, model_name='random_forest')
    
    # Create submission format
    submission = test_features[['city', 'year', 'weekofyear']].copy()
    submission['total_cases'] = predictions.astype(int)
    submission.to_csv('dengue_predictions.csv', index=False)
    
    print(f"Predictions saved to dengue_predictions.csv")
    print(f"Sample predictions:\n{submission.head(10)}")
    
    # Step 7: Summary Report
    print("\n7. Summary Report")
    print("-" * 40)
    
    print(f"📊 Data Processing Complete!")
    print(f"   • Total records processed: {len(engineered_data):,}")
    print(f"   • Features created: {len(ml_trainer.feature_names)}")
    print(f"   • Models trained: {len(models)}")
    print(f"   • Anomalies detected: {anomaly_summary['combined_anomalies']}")
    print(f"   • Test predictions generated: {len(predictions)}")
    
    print(f"\n🎯 Best Model Performance:")
    if not performance_df.empty:
        best_model = performance_df['MAE'].idxmin()
        best_mae = performance_df.loc[best_model, 'MAE']
        print(f"   • Best model: {best_model}")
        print(f"   • Mean Absolute Error: {best_mae:.4f}")
    
    print(f"\n🎉 Project completed successfully!")
    print(f"   • Database: dengue_data.db")
    print(f"   • Models: models/ directory")
    print(f"   • Predictions: dengue_predictions.csv")
    print(f"   • Dashboard: Run 'streamlit run src/dashboard.py'")
    
    data_collector.close_db()

if __name__ == "__main__":
    main()